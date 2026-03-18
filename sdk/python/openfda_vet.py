"""
OpenFDA Veterinary Adverse Events SDK
======================================
Python client for the openFDA Animal & Veterinary Adverse Events API.
Part of the VetClaw open veterinary AI skill library.

Usage:
    from openfda_vet import OpenFDAVet

    client = OpenFDAVet(api_key="YOUR_KEY")  # or omit for unauthenticated (1K/day limit)

    # Search adverse events for dogs
    events = client.search(species="Dog", limit=10)

    # Search by drug and species
    events = client.search(species="Cat", drug="Amoxicillin", limit=5)

    # Search by reaction
    events = client.search(species="Dog", reaction="Seizure")

    # Date range search
    events = client.search(
        species="Dog",
        date_from="2023-01-01",
        date_to="2024-12-31",
        limit=100
    )

    # Count adverse events by species
    counts = client.count(field="animal.species")

    # Count reactions for a specific drug
    counts = client.count(
        field="reaction.veddra_term_name",
        drug="Ivermectin",
        species="Dog"
    )

    # Paginate through results
    for page in client.paginate(species="Dog", drug="NSAID", page_size=100):
        for event in page:
            print(event["safetyreportid"])

API Reference: https://open.fda.gov/apis/animalandveterinary/event/
Get API Key:   https://open.fda.gov/apis/authentication/
"""

import time
from typing import Any, Generator, Optional
from urllib.parse import quote

try:
    import requests
except ImportError:
    raise ImportError("Install requests: pip install requests")


class OpenFDAVetError(Exception):
    """Raised when the openFDA API returns an error."""
    pass


class RateLimitError(OpenFDAVetError):
    """Raised when API rate limit is exceeded."""
    pass


class OpenFDAVet:
    """Client for the openFDA Animal & Veterinary Adverse Events API."""

    BASE_URL = "https://api.fda.gov/animalandveterinary/event.json"

    # Rate limits
    RATE_LIMIT_PER_MINUTE = 240
    DAILY_LIMIT_NO_KEY = 1_000
    DAILY_LIMIT_WITH_KEY = 120_000
    MAX_SKIP = 25_000
    MAX_LIMIT = 1_000

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            api_key: openFDA API key (free from https://open.fda.gov/apis/authentication/).
                     Without a key, rate limit is 1,000 requests/day.
                     With a key, rate limit is 120,000 requests/day.
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _build_search_query(
        self,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        drug: Optional[str] = None,
        reaction: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        raw_query: Optional[str] = None,
    ) -> Optional[str]:
        """Build an openFDA search query string from structured parameters."""
        parts = []

        if raw_query:
            parts.append(raw_query)
        if species:
            parts.append(f'animal.species:"{species.upper()}"')
        if breed:
            parts.append(f'animal.breed.breed_component:"{breed}"')
        if drug:
            parts.append(f'drug.name:"{drug.upper()}"')
        if reaction:
            parts.append(f'reaction.veddra_term_name:"{reaction}"')
        if date_from and date_to:
            parts.append(
                f"original_receive_date:[{date_from.replace('-', '')} TO {date_to.replace('-', '')}]"
            )
        elif date_from:
            parts.append(
                f"original_receive_date:[{date_from.replace('-', '')} TO 20991231]"
            )
        elif date_to:
            parts.append(
                f"original_receive_date:[20040101 TO {date_to.replace('-', '')}]"
            )

        return "+AND+".join(parts) if parts else None

    def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        """Make a request to the openFDA API with error handling."""
        if self.api_key:
            params["api_key"] = self.api_key

        response = self.session.get(self.BASE_URL, params=params)

        if response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded. With an API key: 240/min, 120K/day. "
                "Without: 240/min, 1K/day."
            )

        if response.status_code == 404:
            # openFDA returns 404 when no results match
            return {"meta": {"results": {"total": 0}}, "results": []}

        if response.status_code != 200:
            raise OpenFDAVetError(
                f"API returned HTTP {response.status_code}: {response.text[:500]}"
            )

        data = response.json()

        if "error" in data:
            raise OpenFDAVetError(f"API error: {data['error'].get('message', str(data['error']))}")

        return data

    def search(
        self,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        drug: Optional[str] = None,
        reaction: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        raw_query: Optional[str] = None,
        limit: int = 10,
        skip: int = 0,
        sort: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Search adverse event reports.

        Args:
            species: Animal species (e.g., "Dog", "Cat", "Horse")
            breed: Breed name (e.g., "Labrador Retriever")
            drug: Drug name (e.g., "Amoxicillin", "Ivermectin")
            reaction: Adverse reaction (e.g., "Seizure", "Vomiting")
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            raw_query: Raw openFDA search syntax (advanced)
            limit: Max results to return (1-1000)
            skip: Number of results to skip (max 25000)
            sort: Sort field and direction (e.g., "original_receive_date:desc")

        Returns:
            dict with "meta" and "results" keys

        Example:
            >>> client.search(species="Dog", drug="Carprofen", limit=5)
        """
        params: dict[str, Any] = {}

        query = self._build_search_query(
            species=species, breed=breed, drug=drug,
            reaction=reaction, date_from=date_from, date_to=date_to,
            raw_query=raw_query,
        )
        if query:
            params["search"] = query

        params["limit"] = min(limit, self.MAX_LIMIT)

        if skip > 0:
            if skip > self.MAX_SKIP:
                raise OpenFDAVetError(f"skip cannot exceed {self.MAX_SKIP}")
            params["skip"] = skip

        if sort:
            params["sort"] = sort

        return self._request(params)

    def count(
        self,
        field: str,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        drug: Optional[str] = None,
        reaction: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        raw_query: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Count adverse events grouped by a field.

        Args:
            field: Field to count by. Common fields:
                   "animal.species", "animal.breed.breed_component",
                   "drug.name", "reaction.veddra_term_name",
                   "original_receive_date"
            species: Filter by species
            drug: Filter by drug name
            reaction: Filter by reaction
            (other search params also accepted)

        Returns:
            List of {"term": str, "count": int} dicts

        Example:
            >>> client.count("reaction.veddra_term_name", species="Cat", drug="Ivermectin")
        """
        params: dict[str, Any] = {"count": field}

        query = self._build_search_query(
            species=species, breed=breed, drug=drug,
            reaction=reaction, date_from=date_from, date_to=date_to,
            raw_query=raw_query,
        )
        if query:
            params["search"] = query

        data = self._request(params)
        return data.get("results", [])

    def paginate(
        self,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        drug: Optional[str] = None,
        reaction: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        raw_query: Optional[str] = None,
        page_size: int = 100,
        max_results: int = 25_000,
        delay: float = 0.3,
    ) -> Generator[list[dict[str, Any]], None, None]:
        """
        Paginate through adverse event results.

        Yields pages of results up to max_results or the API skip limit (25,000).

        Args:
            page_size: Results per page (max 1000)
            max_results: Stop after this many total results
            delay: Seconds between requests (respect rate limits)
            (other search params also accepted)

        Yields:
            List of adverse event dicts per page

        Example:
            >>> for page in client.paginate(species="Dog", drug="NSAID", page_size=100):
            ...     for event in page:
            ...         print(event["safetyreportid"])
        """
        skip = 0
        fetched = 0
        page_size = min(page_size, self.MAX_LIMIT)

        while skip <= self.MAX_SKIP and fetched < max_results:
            remaining = max_results - fetched
            current_limit = min(page_size, remaining)

            data = self.search(
                species=species, breed=breed, drug=drug,
                reaction=reaction, date_from=date_from, date_to=date_to,
                raw_query=raw_query, limit=current_limit, skip=skip,
            )

            results = data.get("results", [])
            if not results:
                break

            yield results
            fetched += len(results)
            skip += len(results)

            total = data.get("meta", {}).get("results", {}).get("total", 0)
            if fetched >= total:
                break

            if delay > 0:
                time.sleep(delay)

    def get_total(
        self,
        species: Optional[str] = None,
        drug: Optional[str] = None,
        reaction: Optional[str] = None,
        raw_query: Optional[str] = None,
    ) -> int:
        """Get total count of matching adverse events."""
        data = self.search(
            species=species, drug=drug, reaction=reaction,
            raw_query=raw_query, limit=1,
        )
        return data.get("meta", {}).get("results", {}).get("total", 0)

    # --- Convenience methods ---

    def dog_events(self, drug: Optional[str] = None, limit: int = 10) -> dict:
        """Shortcut: search adverse events for dogs."""
        return self.search(species="Dog", drug=drug, limit=limit)

    def cat_events(self, drug: Optional[str] = None, limit: int = 10) -> dict:
        """Shortcut: search adverse events for cats."""
        return self.search(species="Cat", drug=drug, limit=limit)

    def horse_events(self, drug: Optional[str] = None, limit: int = 10) -> dict:
        """Shortcut: search adverse events for horses."""
        return self.search(species="Horse", drug=drug, limit=limit)

    def top_reactions(self, species: str, drug: Optional[str] = None) -> list[dict]:
        """Get top adverse reactions for a species (optionally filtered by drug)."""
        return self.count("reaction.veddra_term_name", species=species, drug=drug)

    def top_drugs(self, species: str) -> list[dict]:
        """Get most-reported drugs for a species."""
        return self.count("drug.name", species=species)

    def top_breeds(self, species: str) -> list[dict]:
        """Get breeds with most adverse event reports for a species."""
        return self.count("animal.breed.breed_component", species=species)


# --- Quick test ---
if __name__ == "__main__":
    client = OpenFDAVet()
    print("Top 5 species by adverse events:")
    for item in client.count("animal.species")[:5]:
        print(f"  {item['term']}: {item['count']:,}")

    print("\nTop 5 drugs reported for dogs:")
    for item in client.top_drugs("Dog")[:5]:
        print(f"  {item['term']}: {item['count']:,}")

    print("\nTop 5 reactions for cats:")
    for item in client.top_reactions("Cat")[:5]:
        print(f"  {item['term']}: {item['count']:,}")
