/**
 * OpenFDA Veterinary Adverse Events SDK
 * ======================================
 * TypeScript client for the openFDA Animal & Veterinary Adverse Events API.
 * Part of the VetClaw open veterinary AI skill library.
 *
 * Usage:
 *   import { OpenFDAVet } from "./openfda-vet";
 *
 *   const client = new OpenFDAVet("YOUR_API_KEY"); // or omit for unauth'd
 *
 *   const events = await client.search({ species: "Dog", drug: "Carprofen", limit: 10 });
 *   const counts = await client.count("reaction.veddra_term_name", { species: "Cat" });
 *   const topDrugs = await client.topDrugs("Dog");
 *
 * API Reference: https://open.fda.gov/apis/animalandveterinary/event/
 * Get API Key:   https://open.fda.gov/apis/authentication/
 */

// --- Types ---

export interface AdverseEvent {
  safetyreportid: string;
  transmissiondate?: string;
  original_receive_date?: string;
  animal?: {
    species?: string;
    breed?: { breed_component?: string };
    weight?: string;
    age?: string;
    sex?: string;
  };
  drug?: Array<{
    name?: string;
    dose?: string;
    dose_unit?: string;
    route?: string;
    active_ingredients?: Array<{ name: string }>;
  }>;
  reaction?: Array<{
    veddra_term_name?: string;
    veddra_code?: string;
  }>;
}

export interface SearchResponse {
  meta: {
    disclaimer: string;
    license: string;
    last_updated: string;
    results: {
      skip: number;
      limit: number;
      total: number;
    };
  };
  results: AdverseEvent[];
}

export interface CountResult {
  term: string;
  count: number;
}

export interface SearchParams {
  species?: string;
  breed?: string;
  drug?: string;
  reaction?: string;
  dateFrom?: string;
  dateTo?: string;
  rawQuery?: string;
  limit?: number;
  skip?: number;
  sort?: string;
}

// --- Errors ---

export class OpenFDAVetError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "OpenFDAVetError";
  }
}

export class RateLimitError extends OpenFDAVetError {
  constructor() {
    super(
      "Rate limit exceeded. With API key: 240/min, 120K/day. Without: 240/min, 1K/day."
    );
    this.name = "RateLimitError";
  }
}

// --- Client ---

export class OpenFDAVet {
  private readonly baseUrl =
    "https://api.fda.gov/animalandveterinary/event.json";
  private readonly apiKey?: string;

  static readonly MAX_LIMIT = 1000;
  static readonly MAX_SKIP = 25000;

  /**
   * Create a new client.
   * @param apiKey - Free API key from https://open.fda.gov/apis/authentication/
   *                 Without key: 1,000 requests/day. With key: 120,000/day.
   */
  constructor(apiKey?: string) {
    this.apiKey = apiKey;
  }

  private buildSearchQuery(params: SearchParams): string | undefined {
    const parts: string[] = [];

    if (params.rawQuery) parts.push(params.rawQuery);
    if (params.species)
      parts.push(`animal.species:"${params.species.toUpperCase()}"`);
    if (params.breed)
      parts.push(`animal.breed.breed_component:"${params.breed}"`);
    if (params.drug) parts.push(`drug.name:"${params.drug.toUpperCase()}"`);
    if (params.reaction)
      parts.push(`reaction.veddra_term_name:"${params.reaction}"`);

    if (params.dateFrom && params.dateTo) {
      const from = params.dateFrom.replace(/-/g, "");
      const to = params.dateTo.replace(/-/g, "");
      parts.push(`original_receive_date:[${from} TO ${to}]`);
    } else if (params.dateFrom) {
      const from = params.dateFrom.replace(/-/g, "");
      parts.push(`original_receive_date:[${from} TO 20991231]`);
    } else if (params.dateTo) {
      const to = params.dateTo.replace(/-/g, "");
      parts.push(`original_receive_date:[20040101 TO ${to}]`);
    }

    return parts.length > 0 ? parts.join("+AND+") : undefined;
  }

  private async request(
    queryParams: Record<string, string>
  ): Promise<SearchResponse> {
    const params = new URLSearchParams(queryParams);
    if (this.apiKey) params.set("api_key", this.apiKey);

    const url = `${this.baseUrl}?${params.toString()}`;
    const response = await fetch(url);

    if (response.status === 429) throw new RateLimitError();

    if (response.status === 404) {
      return {
        meta: {
          disclaimer: "",
          license: "",
          last_updated: "",
          results: { skip: 0, limit: 0, total: 0 },
        },
        results: [],
      };
    }

    if (!response.ok) {
      const text = await response.text();
      throw new OpenFDAVetError(
        `API returned HTTP ${response.status}: ${text.slice(0, 500)}`
      );
    }

    const data = await response.json();

    if (data.error) {
      throw new OpenFDAVetError(
        `API error: ${data.error.message || JSON.stringify(data.error)}`
      );
    }

    return data as SearchResponse;
  }

  /**
   * Search adverse event reports.
   *
   * @example
   * const events = await client.search({ species: "Dog", drug: "Carprofen", limit: 5 });
   */
  async search(params: SearchParams = {}): Promise<SearchResponse> {
    const queryParams: Record<string, string> = {};

    const query = this.buildSearchQuery(params);
    if (query) queryParams.search = query;

    queryParams.limit = String(
      Math.min(params.limit ?? 10, OpenFDAVet.MAX_LIMIT)
    );

    if (params.skip) {
      if (params.skip > OpenFDAVet.MAX_SKIP)
        throw new OpenFDAVetError(`skip cannot exceed ${OpenFDAVet.MAX_SKIP}`);
      queryParams.skip = String(params.skip);
    }

    if (params.sort) queryParams.sort = params.sort;

    return this.request(queryParams);
  }

  /**
   * Count adverse events grouped by a field.
   *
   * @param field - Field to count by (e.g., "animal.species", "drug.name",
   *                "reaction.veddra_term_name", "animal.breed.breed_component")
   *
   * @example
   * const counts = await client.count("reaction.veddra_term_name", { species: "Cat" });
   */
  async count(
    field: string,
    params: Omit<SearchParams, "limit" | "skip" | "sort"> = {}
  ): Promise<CountResult[]> {
    const queryParams: Record<string, string> = { count: field };

    const query = this.buildSearchQuery(params);
    if (query) queryParams.search = query;

    const data = await this.request(queryParams);
    return (data.results as unknown as CountResult[]) || [];
  }

  /**
   * Paginate through results. Yields pages up to maxResults or API limit (25,000).
   *
   * @example
   * for await (const page of client.paginate({ species: "Dog", drug: "NSAID" })) {
   *   for (const event of page) console.log(event.safetyreportid);
   * }
   */
  async *paginate(
    params: SearchParams & { pageSize?: number; maxResults?: number } = {}
  ): AsyncGenerator<AdverseEvent[]> {
    const pageSize = Math.min(params.pageSize ?? 100, OpenFDAVet.MAX_LIMIT);
    const maxResults = params.maxResults ?? OpenFDAVet.MAX_SKIP;
    let skip = 0;
    let fetched = 0;

    while (skip <= OpenFDAVet.MAX_SKIP && fetched < maxResults) {
      const remaining = maxResults - fetched;
      const currentLimit = Math.min(pageSize, remaining);

      const data = await this.search({ ...params, limit: currentLimit, skip });
      const results = data.results;

      if (!results.length) break;

      yield results;
      fetched += results.length;
      skip += results.length;

      const total = data.meta.results.total;
      if (fetched >= total) break;
    }
  }

  /**
   * Get total count of matching adverse events.
   */
  async getTotal(
    params: Omit<SearchParams, "limit" | "skip">
  ): Promise<number> {
    const data = await this.search({ ...params, limit: 1 });
    return data.meta.results.total;
  }

  // --- Convenience methods ---

  /** Search adverse events for dogs. */
  async dogEvents(drug?: string, limit = 10) {
    return this.search({ species: "Dog", drug, limit });
  }

  /** Search adverse events for cats. */
  async catEvents(drug?: string, limit = 10) {
    return this.search({ species: "Cat", drug, limit });
  }

  /** Search adverse events for horses. */
  async horseEvents(drug?: string, limit = 10) {
    return this.search({ species: "Horse", drug, limit });
  }

  /** Top adverse reactions for a species. */
  async topReactions(species: string, drug?: string) {
    return this.count("reaction.veddra_term_name", { species, drug });
  }

  /** Most-reported drugs for a species. */
  async topDrugs(species: string) {
    return this.count("drug.name", { species });
  }

  /** Breeds with most adverse event reports. */
  async topBreeds(species: string) {
    return this.count("animal.breed.breed_component", { species });
  }
}
