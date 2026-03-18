# VetClaw SDKs

API client libraries for veterinary data sources referenced by VetClaw skills.

## openFDA Animal & Veterinary Adverse Events

Query the FDA's adverse event reporting database for veterinary drugs and products. Covers dogs, cats, horses, cattle, and other species.

### Python

```python
from openfda_vet import OpenFDAVet

client = OpenFDAVet(api_key="YOUR_KEY")  # omit for unauthenticated (1K/day)

# Search adverse events
events = client.search(species="Dog", drug="Carprofen", limit=10)

# Count top reactions for a drug
reactions = client.top_reactions("Dog", drug="Ivermectin")

# Count top drugs by species
drugs = client.top_drugs("Cat")

# Paginate through all results
for page in client.paginate(species="Dog", reaction="Seizure", page_size=100):
    for event in page:
        print(event["safetyreportid"], event.get("drug", []))
```

**Requirements:** `pip install requests`

### TypeScript

```typescript
import { OpenFDAVet } from "./openfda-vet";

const client = new OpenFDAVet("YOUR_KEY"); // omit for unauthenticated

// Search adverse events
const events = await client.search({ species: "Dog", drug: "Carprofen", limit: 10 });

// Count top reactions for a drug
const reactions = await client.topReactions("Dog", "Ivermectin");

// Count top drugs by species
const drugs = await client.topDrugs("Cat");

// Paginate through all results
for await (const page of client.paginate({ species: "Dog", reaction: "Seizure" })) {
  for (const event of page) {
    console.log(event.safetyreportid, event.drug);
  }
}
```

**Requirements:** Node 18+ (uses native `fetch`)

### API Details

| Parameter | Value |
| --- | --- |
| Base URL | `https://api.fda.gov/animalandveterinary/event.json` |
| Auth | Free API key from [open.fda.gov](https://open.fda.gov/apis/authentication/) |
| Rate limit (no key) | 240/min, 1,000/day |
| Rate limit (with key) | 240/min, 120,000/day |
| Max results per request | 1,000 |
| Max skip (pagination) | 25,000 |
| Data updated | Quarterly |

### Common Fields

| Field | Description |
| --- | --- |
| `animal.species` | Species (DOG, CAT, HORSE, CATTLE, etc.) |
| `animal.breed.breed_component` | Breed name |
| `drug.name` | Drug product name |
| `reaction.veddra_term_name` | Adverse reaction (VeDDRA standardized) |
| `original_receive_date` | Date FDA received the report |

Full field reference: [open.fda.gov/apis/animalandveterinary/event/searchable-fields](https://open.fda.gov/apis/animalandveterinary/event/searchable-fields/)
