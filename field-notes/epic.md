# Two papers, one population of dogs

A journal club finds two papers on pimobendan in dogs with heart disease. Both are indexed in PubMed. Both carry “EPIC Study” in the title. How many independent trials do they represent?

## Read the pair

| Paper | What the authors examined | Open the source |
| --- | --- | --- |
| Boswood and colleagues, 2016 | In dogs with preclinical myxomatous mitral valve disease and an enlarged heart, how did time to congestive heart failure, cardiac-related death, or cardiac euthanasia compare between treatment groups? | [PubMed](https://pubmed.ncbi.nlm.nih.gov/27678080/) · [VetEvidence](https://vetevidence.com/?pmid=27678080) |
| Boswood and colleagues, 2018 | Within the EPIC study, how did clinical measurements change over time, and how did changes in heart size relate to later outcomes? | [PubMed](https://pubmed.ncbi.nlm.nih.gov/29214723/) · [VetEvidence](https://vetevidence.com/?pmid=29214723) |

The second paper follows dogs from the same trial. It adds observations about how the disease and measurements changed. Counting it as an independent replication would give this research group’s findings too much weight in a review.

## Try it with a colleague

1. Open the first paper and find its enrollment criteria. Would the findings directly answer a question about a dog with a murmur whose heart size is unknown?
2. Open the second paper and find its animal population and measurement schedule. Which question could you answer from this paper that the primary endpoint alone would leave open?
3. Check each source in VetEvidence. Record its returned tier, source verification, and species note. Alongside those results, record the shared trial once. A source-by-source grade cannot establish that two papers are independent.

To check the pair from the repository root:

```sh
python3 scripts/check_references.py 27678080 29214723
```

A journal club can finish with a single sentence: “In dogs meeting these enrollment criteria, these two reports from the EPIC trial examined ___ and ___.” The two blanks make the distinction between the questions visible.

Have another pair that readers often mistake for independent evidence? [Contribute a field note](../CONTRIBUTING.md#contribute-a-field-note).
