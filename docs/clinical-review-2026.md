# VetClaw Clinical Accuracy Review — 2026

## Purpose and disclaimer

This document provides a **citable source for every dosing and safety value** in the VetClaw
clinical skills. Each value is verified against primary literature (PubMed) and authoritative
references (FDA/EMA drug labels, FDA CVM, IRIS/AAHA/ISFM guidance, the NASPHV *Chlamydia
psittaci* Compendium, and the Merck Veterinary Manual). We publish it **for transparency**, so
that anyone using the repository can see the evidence behind each value — and we welcome review
and correction from board-certified specialists.

**This review is not a substitute for a licensed veterinarian.** It is a documentation and
sourcing exercise, not clinical advice. Dosing must always be individualized to the patient,
and product labels vary by country and formulation. If you find an error here or in any
skill, please open a **Clinical Correction** issue (label `clinical-accuracy`) — corrections
are welcome and are our highest priority.

A note on citations: articles marked **[PubMed]** are indexed in PubMed; DOI links are given
where the record provided one (per PubMed's attribution requirements). Some older primary
papers (pre-2000 JAVMA/AJVR) have no registered DOI and are cited by PMID. Non-PubMed
sources (labels, guidelines, textbooks) are cited by URL or edition.

---

## Summary of verdicts

| # | Item | Verdict |
|---|------|---------|
| 1 | IV potassium ceiling 0.5 mEq/kg/hr + KCl sliding scale | **Confirmed.** Ceiling correct; sliding-scale concentrations aligned to the canonical DiBartola scale during this review |
| 2 | Hyponatremia correction ≤10–12 mEq/L/24h; 3% NaCl ≈0.51 mEq Na/mL | **Confirmed** |
| 3 | Maintenance fluids ~50 mL/kg/day (40–60) or (30×kg)+70 | **Confirmed** (note internal divergence at low body weight) |
| 4 | Feline meloxicam: FDA black-box; US single 0.3 mg/kg SC; EU chronic 0.05 mg/kg/day | **Confirmed** |
| 5 | Equine firocoxib 0.1 mg/kg PO (Equioxx), not 5 mg/kg | **Confirmed** |
| 6 | Canine carprofen 4.4 mg/kg/day (2.2 BID or 4.4 SID); not TID | **Confirmed** |
| 7 | Feline morphine 0.1–0.3 mg/kg; feline gabapentin ~5–10 mg/kg | **Confirmed** (gabapentin: 10 mg/kg is the usual analgesic dose; up to 20 mg/kg used) |
| 8 | Sighthounds tolerate isoflurane; sensitivity is thiopental/barbiturates; atropine 0.02–0.04 mg/kg | **Confirmed** |
| 9 | MDR1/ABCB1 homozygotes ivermectin-sensitive; prevention (6–12 mcg/kg) tolerated; mange (300–600 mcg/kg) dangerous | **Confirmed** |
| 10 | Enrofloxacin prohibited in US food poultry (2005); flunixin cattle meat 4 d, milk 36 h, IV-only | **Confirmed** |
| 11 | Feline systolic BP ~120–140; IRIS hypertension >160; PTU not used in cats | **Confirmed** |
| 12 | Psittacosis: doxycycline 45 d; oral ~25–50 mg/kg q24h OR Vibravenos ~75–100 mg/kg IM q5–7d | **Confirmed** |
| 13 | Onions/garlic toxic to horses (Heinz-body anemia); feline meloxicam black-box | **Confirmed** |
| 14 | Canine BRAF V595E ortholog; ~80% of canine urothelial/TCC, not human V600E/melanoma | **Confirmed** |

**Bottom line:** all 14 corrections are confirmed. Item 1's *maximum infusion rate* (the
load-bearing safety number) is correct; its KCl **sliding-scale concentrations** were the one
item flagged — they had sat one step below the canonical DiBartola/Greene scale and were
mislabeled "classic" — and they have now been **aligned to the canonical scale** with per-band
maximum fluid rates. Details and the canonical values are below.

---

## Item 1 — IV potassium: maximum infusion rate and KCl sliding scale
**File:** `skills/clinical/fluid-therapy/SKILL.md`

**Value in repo:** Maximum potassium infusion rate is a hard ceiling of
**0.5 mEq/kg/hr** (ECG monitoring at/near the ceiling); KCl added to fluids by a sliding
scale of **20 / 28–30 / 40 / 60 / 80 mEq/L** for serum K⁺ of 3.6–5.0 / 3.1–3.5 / 2.6–3.0 / 2.1–2.5 / <2.0
mEq/L; peripheral concentration limit 40 mEq/L (60–80 via central line).

**Verdict: Confirmed.** The 0.5 mEq/kg/hr ceiling is correct; the sliding-scale concentrations
were aligned to the canonical DiBartola scale during this review (they had been one step lower).

- The **0.5 mEq/kg/hr hard ceiling is correct and is the critical safety value.** Standard
  critical-care teaching: do not exceed 0.5 mEq/kg/hr; ECG monitoring and q4h K⁺ checks are
  advised above ~0.4 mEq/kg/hr; peripheral concentrations should generally stay ≤60 mEq/L.
- The **sliding-scale concentrations are a conservative variant**, not the canonical scale,
  and calling it "the classic sliding scale" is inaccurate. The widely published
  DiBartola/Greene scale pairs each concentration with a maximum drip rate so that delivery
  never exceeds ~0.5 mEq/kg/hr:

  | Serum K⁺ (mEq/L) | KCl added per L | Max fluid rate (mL/kg/hr) |
  |---|---|---|
  | 3.6–5.0 | 20 mEq/L | 25 |
  | 3.1–3.5 | 28–30 mEq/L | 18 |
  | 2.6–3.0 | 40 mEq/L | 12 |
  | 2.1–2.5 | 60 mEq/L | 8 |
  | <2.0 | 80 mEq/L | 6 |

  (Each row: concentration × max rate ÷ 1000 ≈ 0.5 mEq/kg/hr.) The repo's table assigns a
  **lower** concentration to each band (e.g., 30 mEq/L at K⁺ 2.5–3.0 where the standard is
  40; 40 mEq/L at 2.0–2.5 where the standard is 60). Using it under-supplements slightly
  relative to the reference — safe, but not the "classic" scale.

**Resolution:** the concentrations were aligned to the canonical values above (each paired with
a maximum fluid rate), and the "classic" label corrected. The 0.5 mEq/kg/hr ceiling was already
correct and unchanged.

**Sources:**
- Today's Veterinary Practice, *Evaluation and Management of the Hypokalemic Patient* — https://todaysveterinarypractice.com/internal-medicine/evaluation-and-management-of-the-hypokalemic-patient/
- VETEMCRIT, *Approach to Hypokalemia* (0.5 mEq/kg/hr ceiling; ≤60 mEq/L peripheral; ECG >0.4 mEq/kg/hr) — https://vetemcrit.com/approach-to-hypokalemia-diagnosis-and-treatment/
- DiBartola SP. *Fluid, Electrolyte, and Acid-Base Disorders in Small Animal Practice* (current ed.) — origin of the canonical sliding scale (no PubMed record; standard reference).

---

## Item 2 — Hyponatremia correction limit and 3% NaCl sodium content
**File:** `skills/clinical/fluid-therapy/SKILL.md`

**Value in repo:** Raise serum Na⁺ by **no more than ~10–12 mEq/L per 24 h**
(slower for chronic) to avoid osmotic demyelination; Na deficit = (target − current) × 0.6 ×
BW = **mEq of Na**; **3% NaCl ≈ 0.51 mEq Na/mL**.

**Verdict: Confirmed.**

- The ≤10–12 mEq/L/24h limit (many sources use ≤10, or ≤0.5 mEq/L/hr) to prevent osmotic
  demyelination syndrome is standard in both veterinary and human medicine. Chronic
  hyponatremia warrants the slower end.
- **3% NaCl sodium content checks out by calculation:** 3% = 30 g NaCl/L; molar mass 58.44
  g/mol → 30 / 58.44 = 0.513 mol/L = **513 mEq Na/L = 0.513 mEq/mL**. The repo's ~0.51
  mEq/mL is correct, so "divide mEq by ~0.5 to get mL of 3% NaCl" is a valid approximation.
- The deficit formula (target − current) × 0.6 × BW yields mEq of Na, which is standard.

**Sources:**
- Burton AG, Hopper K. *Hyponatremia in dogs and cats.* J Vet Emerg Crit Care. 2019. **[PubMed]** DOI: [10.1111/vec.12881](https://doi.org/10.1111/vec.12881)
- AAHA 2024 Fluid Therapy Guidelines for Dogs and Cats, Section 5 (Ill Patients) — https://www.aaha.org/resources/2024-aaha-fluid-therapy-guidelines-for-dogs-and-cats/section-5-fluid-therapy-in-ill-patients/
- Clinician's Brief, *Clinical Approach to Hyponatremia* — https://www.cliniciansbrief.com/article/hyponatremia

---

## Item 3 — Maintenance fluid rate
**File:** `skills/clinical/fluid-therapy/SKILL.md`

**Value in repo:** ~50 mL/kg/day (typical range 40–60), or the linear estimate
**(30 × BW_kg) + 70 = mL/day**; larger patients trend to the lower mL/kg end.

**Verdict: Confirmed** (with a transparency note on internal consistency).

- The allometric linear formula **(30 × BW) + 70 mL/day is the Merck Veterinary Manual
  standard for dogs and cats weighing ~2–70 kg**; outside that range, use 132 × BW^0.75
  (dogs) or 80 × BW^0.75 (cats). Broad maintenance ranges of 40–60 (some sources up to ~75)
  mL/kg/day are all in accepted use.
- **Note:** the two methods diverge at low body weight. For a 10 kg dog, "50 mL/kg/day" =
  500 mL/day, but (30×10)+70 = 370 mL/day. The repo's worked examples use the per-kg method
  for the 10 kg dog (~500 mL) and the allometric formula for the 30 kg dog (~970 mL). Both
  endpoint values are clinically acceptable, and the skill correctly notes that small patients
  scale toward the higher mL/kg end — but the two formulas are **not interchangeable** and
  should not be presented as equivalent for small patients. No dose is unsafe; this is a
  presentation caveat only.

**Sources:**
- Merck Veterinary Manual, *Maintenance Fluid Plan in Animals* — https://www.merckvetmanual.com/therapeutics/fluid-therapy/maintenance-fluid-plan-in-animals
- AAHA Fluid Therapy tip sheet — https://www.aaha.org/wp-content/uploads/globalassets/02-guidelines/fluid-therapy/fluidtherapy_tipsheet.pdf

---

## Item 4 — Feline meloxicam: black-box warning and dosing
**Files:** `skills/safety/nsaid-safety/SKILL.md`, `skills/clinical/pain-assessment/SKILL.md`

**Value in repo:** FDA **black-box warning** (repeated dosing → fatal renal
failure in cats); US label = a **single, one-time 0.3 mg/kg SC** dose; chronic use (EU
label / off-label US) = **0.05 mg/kg once daily** (lowest effective) with mandatory renal
monitoring; the **0.3–0.5 mg/kg q48h regimen is not an established safe protocol** and should
be avoided.

**Verdict: Confirmed.**

- The FDA boxed warning is real and applies to all approved meloxicam products: *repeated
  use of meloxicam in cats can cause acute renal failure and death.*
- The **US-approved use in cats is a single one-time SC dose of 0.3 mg/kg** for postoperative
  pain (orthopedic surgery, ovariohysterectomy, castration); no repeat injection is approved.
- The **EU/UK Metacam oral label supports chronic use at a 0.05 mg/kg/day maintenance dose**
  (0.1 mg/kg on day 1, then 0.05 mg/kg once daily) with renal screening — exactly as stated.
- Renal injury has been documented in cats **even at the labeled 0.3 mg/kg SC dose**,
  reinforcing the caution and the rejection of the older repeated-dose (0.3–0.5 mg/kg q48h)
  approach.

**Sources:**
- FDA, *Information About the Boxed Warning on Meloxicam Labels Regarding Safety Risks in Cats* — https://www.fda.gov/animal-veterinary/product-safety-information/information-about-boxed-warning-meloxicam-labels-regarding-safety-risks-cats
- Metacam (meloxicam) 5 mg/mL Solution for Injection, feline label (single 0.3 mg/kg SC) — https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=ca78caf5-2b47-46c1-abec-0f925b39f455
- EU/UK Metacam 0.5 mg/mL oral suspension for cats SPC (0.1 mg/kg day 1 → 0.05 mg/kg/day maintenance).
- Wun MK, Leister E, King T, Korman R, Malik R. *Acute kidney injury in 18 cats after subcutaneous meloxicam…* Aust Vet J. 2022. **[PubMed]** DOI: [10.1111/avj.13222](https://doi.org/10.1111/avj.13222) — AKI at the label 0.3 mg/kg SC dose.

---

## Item 5 — Equine firocoxib (Equioxx) dose
**File:** `skills/safety/nsaid-safety/SKILL.md`

**Value in repo:** Equine firocoxib label dose is **0.1 mg/kg PO** (Equioxx;
~0.09 mg/kg IV), **not 5 mg/kg** (5 mg/kg is the canine Previcox dose; ~50× overdose in a
horse).

**Verdict: Confirmed.**

- FDA-approved Equioxx oral dose in horses is **0.045 mg/lb (0.1 mg/kg) once daily, up to 14
  days**; the tablet is one 57 mg tablet for an 800–1300 lb horse. The Equioxx injectable
  label dose is 0.09 mg/kg IV. The canine Previcox dose is indeed 5 mg/kg, so cross-applying
  it to a horse is roughly a 50× overdose. The correction is accurate.

**Sources:**
- Equioxx (firocoxib) FDA label / DailyMed — https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=3f891a61-ce58-4cc1-97e2-a161907ea8eb
- FDA Freedom of Information Summary, Equioxx (NADA 141-253) — https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadLabeling/523

---

## Item 6 — Canine carprofen dose
**Files:** `skills/safety/nsaid-safety/SKILL.md`, `skills/clinical/pain-assessment/SKILL.md`

**Value in repo:** Canine carprofen **4.4 mg/kg/day**, given as **2.2 mg/kg BID
or 4.4 mg/kg SID**; do not exceed 4.4 mg/kg/day; **not dosed TID**.

**Verdict: Confirmed.**

- The FDA Rimadyl label is **2 mg/lb (4.4 mg/kg) once daily, or divided as 1 mg/lb (2.2
  mg/kg) twice daily.** 4.4 mg/kg/day is the maximum; there is no TID regimen. The correction
  matches the label exactly.

**Sources:**
- Rimadyl (carprofen) FDA label — https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadLabeling/403
- FDA Freedom of Information Summary, Rimadyl Caplets (NADA 141-053) — https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/586

---

## Item 7 — Feline morphine and gabapentin dosing
**File:** `skills/clinical/pain-assessment/SKILL.md`

**Value in repo:** Feline morphine **0.1–0.3 mg/kg** (lower than canine
0.5–1 mg/kg; higher doses risk excitation/hyperthermia); feline gabapentin **~5–10 mg/kg**.

**Verdict: Confirmed** (with a note that 10 mg/kg is the usual feline analgesic gabapentin dose).

- **Feline morphine 0.1–0.3 mg/kg is correct and appropriately lower than the canine
  0.5–1 mg/kg.** The 2022 ISFM Consensus Guidelines on the Management of Acute Pain in Cats
  cite morphine 0.1–0.3 mg/kg and note the low end of the opioid range is the starting point
  in cats (mid-range in dogs).
- **Feline gabapentin:** the repo's 5–10 mg/kg is acceptable. The definitive feline PK study
  dosed 10 mg/kg PO (and 5 mg/kg IV); clinical analgesic dosing is commonly **10 mg/kg PO
  q8–12h, and up to ~20 mg/kg** in refractory chronic pain. The repo's "5–10 mg/kg… start
  low" is conservative and reasonable; consider stating 10 mg/kg as the typical analgesic
  target with an upper bound near 20 mg/kg.

**Sources:**
- Steagall PV, Robertson S, Simon B, et al. *2022 ISFM Consensus Guidelines on the Management of Acute Pain in Cats.* J Feline Med Surg. 2022. **[PubMed]** PMC10845386 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10845386/
- Adrian D, Papich MG, Baynes R, Stafford E, Lascelles BDX. *The pharmacokinetics of gabapentin in cats.* J Vet Intern Med. 2018;32(6):1996–2002. **[PubMed]** DOI: [10.1111/jvim.15313](https://doi.org/10.1111/jvim.15313) — 10 mg/kg PO regimen.

---

## Item 8 — Sighthound anesthesia and atropine dose
**File:** `skills/safety/anesthesia-safety/SKILL.md`

**Value in repo:** Sighthounds tolerate modern inhalants (**isoflurane,
sevoflurane**); the key sensitivity is to **thiopental/barbiturates**, not isoflurane;
atropine for bradycardia **0.02–0.04 mg/kg**.

**Verdict: Confirmed.**

- Greyhounds/sighthounds have markedly **prolonged recovery from thiobarbiturates**
  (thiopental, thiamylal) — recumbency-to-standing 3–4× longer than mixed-breed dogs, some >8
  hours — due to low body fat **and** a deficiency in the hepatic enzyme (CYP2B11) that
  performs the first metabolic step. Thiobarbiturates should be avoided; methohexital,
  propofol, or ketamine/diazepam are alternatives.
- **Isoflurane (and sevoflurane) are appropriate** — isoflurane is minimally metabolized and
  is specifically preferred over halothane in these breeds. The correction is sound.
- **Atropine 0.02–0.04 mg/kg IV** for anesthetic bradycardia is the standard reference dose
  (Plumb's; matches glycopyrrolate 0.005–0.01 mg/kg listed alongside).

**Sources:**
- Robinson EP, Sams RA, Muir WW. *Barbiturate anesthesia in greyhound and mixed-breed dogs: comparative cardiopulmonary effects, anesthetic effects, and recovery rates.* Am J Vet Res. 1986;47(10):2105–12. **[PubMed]** PMID: 3777630.
- WSAVA 2019, *Breed-Specific Anesthesia* (thiobarbiturate avoidance; isoflurane preferred over halothane) — https://www.vin.com/apputil/content/defaultadv1.aspx?pId=24437&id=9382671
- Plumb's Veterinary Drug Handbook (current ed.), atropine — standard reference.

---

## Item 9 — MDR1/ABCB1 ivermectin sensitivity by dose
**File:** `skills/safety/lethal-variance-detection/SKILL.md`

**Value in repo:** Homozygous-affected (mutant/mutant) MDR1/ABCB1 dogs are
neurotoxically sensitive **across a range of doses** (no single "safe threshold"); heartworm
**prevention doses (6–12 mcg/kg) are generally tolerated** even by mutants, but higher doses —
microfilaricidal (~50 mcg/kg) and especially **mange/demodicosis doses (300–600 mcg/kg) — can
cause severe neurotoxicity or death.**

**Verdict: Confirmed.**

- The founding work established that the **4-bp deletion in MDR1 (ABCB1)** causes ivermectin
  sensitivity: **homozygous** dogs show the sensitive phenotype, while homozygous-normal and
  **heterozygous** dogs do not show increased sensitivity at standard ivermectin exposure.
  Affected breeds: Collies, Australian Shepherds, Shelties, and crosses.
- Dose gradient is accurate: monthly **heartworm prevention (~6 mcg/kg, up to ~12)** is
  tolerated even by affected dogs, whereas high-dose macrocyclic lactone therapy is dangerous.
  A homozygous-mutant Australian Shepherd developed neurotoxicity after a single **400 mcg/kg**
  dose of moxidectin — squarely within the "mange dose" danger range the skill flags.
- The framing "sensitive across a range — do not rely on a single safe threshold" is the
  correct, nuanced position.

**Sources (all [PubMed]):**
- Mealey KL, Bentjen SA, Gay JM, Cantor GH. *Ivermectin sensitivity in collies is associated with a deletion mutation of the mdr1 gene.* Pharmacogenetics. 2001;11(8):727–33. DOI: [10.1097/00008571-200111000-00012](https://doi.org/10.1097/00008571-200111000-00012)
- Mealey KL. *Therapeutic implications of the MDR-1 gene.* J Vet Pharmacol Ther. 2004;27(5):257–64. DOI: [10.1111/j.1365-2885.2004.00607.x](https://doi.org/10.1111/j.1365-2885.2004.00607.x)
- Geyer J, Döring B, Godoy JR, Moritz A, Petzinger E. *…moxidectin-sensitive Australian Shepherd* (neurotoxicity at 400 mcg/kg in a homozygous MDR1 mutant). J Vet Pharmacol Ther. 2005;28(1):95–9. DOI: [10.1111/j.1365-2885.2004.00625.x](https://doi.org/10.1111/j.1365-2885.2004.00625.x)

---

## Item 10 — Enrofloxacin in poultry (prohibited) and flunixin cattle withdrawal
**File:** `skills/pharma/withdrawal-times/SKILL.md`

**Value in repo:** Extralabel **fluoroquinolone/enrofloxacin use in
food-producing poultry is illegal in the US** (FDA withdrew poultry enrofloxacin approval in
2005; no lawful withdrawal time exists). Flunixin in cattle: **meat 4 days, milk 36 h, IV
only** (IM/SC markedly prolongs residues; a leading cause of violative NSAID residues).

**Verdict: Confirmed.**

- FDA's final decision (July 27, 2005) **withdrew approval of enrofloxacin for poultry,
  effective September 12, 2005** — the first time FDA withdrew an agricultural antibiotic over
  antimicrobial-resistance (fluoroquinolone-resistant *Campylobacter*) concerns. Extralabel
  fluoroquinolone use in food-producing poultry is therefore prohibited; there is no lawful
  withdrawal interval. Correct.
- Flunixin meglumine (Banamine) in cattle: label is **4-day meat and 36-hour milk withdrawal,
  intravenous administration only.** IM/SC administration produces prolonged, violative tissue
  residues — flunixin is one of the most common violative-residue NSAIDs in cattle at
  slaughter. Correct.

**Sources:**
- FDA, *Withdrawal of Enrofloxacin for Poultry* — https://www.fda.gov/animal-veterinary/recalls-withdrawals/withdrawal-enrofloxacin-poultry
- Federal Register, *Enrofloxacin for Poultry; Final Decision on Withdrawal…* (Aug 1, 2005) — https://www.federalregister.gov/documents/2005/08/01/05-15224/
- Banamine (flunixin meglumine) label, Merck Animal Health — https://www.merck-animal-health-usa.com/channel-content/species/cattle/banamine
- dvm360, *Flunixin Meglumine* (IV-only; IM/SC → violative residues) — https://www.dvm360.com/view/flunixin-meglumine-0

---

## Item 11 — Feline blood pressure, IRIS hypertension, and propylthiouracil
**File:** `skills/species/feline-medicine/SKILL.md`

**Value in repo:** Normal feline systolic BP **~120–140 mmHg** awake; **IRIS
hypertension >160 mmHg** (Doppler preferred; allow for situational/"white-coat" elevation);
**propylthiouracil is NOT used in cats** (methimazole/carbimazole are; PTU causes
immune-mediated hemolytic anemia/thrombocytopenia).

**Verdict: Confirmed.**

- Normal awake feline systolic BP of ~120–140 mmHg is consistent with IRIS substaging, which
  classifies <140 mmHg as normotensive, 140–159 as prehypertensive, **160–179 as hypertensive
  (moderate target-organ-damage risk)**, and ≥180 as severely hypertensive. Treatment is
  generally initiated for systolic pressures consistently **>160 mmHg** (or lower if
  target-organ damage is present). The "white-coat"/situational caveat is appropriate.
- **PTU is contraindicated for routine feline hyperthyroidism:** in the classic case series,
  **9 of 105 PTU-treated hyperthyroid cats** developed serious immune-mediated reactions
  (Coombs'-positive hemolytic anemia, thrombocytopenia, antinuclear antibodies) after 19–37
  days. Methimazole and carbimazole are the thioureylene drugs of choice. Correct.

**Sources:**
- IRIS hypertension guidance / substaging by target-organ-damage risk — https://www.iris-kidney.com/ (see also treatment threshold discussion, Today's Veterinary Practice CKD guidelines).
- Peterson ME, Hurvitz AI, Leib MS, Cavanagh PG, Dutton RE. *Propylthiouracil-associated hemolytic anemia, thrombocytopenia, and antinuclear antibodies in cats with hyperthyroidism.* J Am Vet Med Assoc. 1984;184(7):806–8. **[PubMed]** PMID: 6609915.
- Merck Veterinary Manual, *Hyperthyroidism in Animals* (methimazole/carbimazole first-line; PTU reserved/avoided).

---

## Item 12 — Psittacosis (Chlamydia psittaci) doxycycline regimen
**File:** `skills/species/avian-medicine/SKILL.md`

**Value in repo:** Doxycycline for **45 days**; **oral ~25–50 mg/kg once daily**
(species-dependent) **OR long-acting injectable doxycycline (Vibravenos) ~75–100 mg/kg IM
every 5–7 days** — do **not** give the injectable daily.

**Verdict: Confirmed.**

- The standard treatment for avian chlamydiosis is doxycycline for a **full 45-day course**,
  as oral doxycycline or long-acting injectable, per the NASPHV *Compendium of Measures to
  Control Chlamydia psittaci* (2017) and the Merck Veterinary Manual.
- **Oral doxycycline in the ~25–50 mg/kg once-daily range is correct and species-dependent;**
  a controlled cockatiel study used 35 mg/kg PO q24h and eliminated infection.
- **Vibravenös (the specific EU long-acting doxycycline for IM use) is dosed 75–100 mg/kg IM
  every 5–7 days** (per the Compendium: every 5–7 days for the first 4 weeks, then every 5
  days) — emphatically **not daily.** The correction (dose, route, and interval) is accurate,
  and the "not daily" warning is an important safety point (some other injectable/compounded
  doxycycline formulations cause tissue reactions or sudden death).

**Sources:**
- Balsamo G, et al. *Compendium of Measures to Control Chlamydia psittaci Infection Among Humans (Psittacosis) and Pet Birds (Avian Chlamydiosis), 2017.* J Avian Med Surg. 2017;31(3):217–265 — https://bioone.org/journals/journal-of-avian-medicine-and-surgery/volume-31/issue-3/217-265/
- Merck Veterinary Manual, *Avian Chlamydiosis* — https://www.merckvetmanual.com/poultry/avian-chlamydiosis/avian-chlamydiosis
- Guzman DS-M, et al. *Evaluating 21-day doxycycline and azithromycin treatments for experimental Chlamydophila psittaci infection in cockatiels.* J Avian Med Surg. 2010;24(1):35–45. **[PubMed]** DOI: [10.1647/2009-009R.1](https://doi.org/10.1647/2009-009R.1) — 35 mg/kg PO q24h; 45-day arm.

---

## Item 13 — Onions/garlic toxic to horses (Heinz-body anemia); feline meloxicam black-box
**File:** `assets/species-drug-safety-matrix.md`

**Value in repo:** Onions/garlic (Allium spp.) are **toxic to horses** (Heinz
body anemia; horses are susceptible); feline meloxicam carries the **FDA black-box** (repeat
dosing → fatal renal failure; single-dose US label).

**Verdict: Confirmed.**

- Allium spp. (onion, garlic, leek, chive) are toxic to horses: **n-propyl disulfide causes
  oxidative red-cell damage → Heinz-body hemolytic anemia.** Experimental/clinical toxicity in
  horses occurs above ~0.4 g/kg/day, and acute hemolytic anemia from wild-onion poisoning in
  horses is a documented, decades-old entity. The matrix's "Toxic (Heinz body anemia; horses
  are susceptible)" is correct.
- The feline meloxicam black-box entry is consistent with Item 4 (FDA boxed warning;
  single-dose US label). Correct.

**Sources:**
- Merck Veterinary Manual, *Garlic and Onion (Allium spp) Toxicosis in Animals* — https://www.merckvetmanual.com/toxicology/food-hazards/garlic-and-onion-allium-spp-toxicosis-in-animals
- Pierce KR, Joyce JR, England RB, Jones LP. *Acute hemolytic anemia caused by wild onion poisoning in horses.* J Am Vet Med Assoc. 1972;160(3):323–7. **[PubMed]** PMID: 5061884.
- FDA boxed-warning page (feline meloxicam) — see Item 4.

---

## Item 14 — Canine BRAF V595E (not human V600E/melanoma)
**File:** `skills/pharma/precision-medicine-mrna-design/SKILL.md`

**Value in repo:** The canine **BRAF ortholog is V595E** (orthologous to human
V600E), characteristic of **canine urothelial/transitional cell carcinoma (~80%)** and
prostatic carcinoma — **not** the human V600E/melanoma association; canine oral/mucosal
melanoma is generally **not** BRAF-driven.

**Verdict: Confirmed.**

- The activating canine **BRAF V595E** mutation is the ortholog of human **V600E**, and is
  reported in a large majority of canine urothelial (transitional cell) carcinomas: whole-exome
  work cites **85%**, and independent studies cite **up to 80%**; it is also found in canine
  prostatic carcinoma and is used as a diagnostic/therapeutic marker. The repo's "~80%" is
  well within the published range.
- The distinction from human disease is correct: **canine oral/mucosal melanoma is generally
  not BRAF-driven**, so human cutaneous-melanoma BRAF response rates should not be assumed to
  transfer to dogs — exactly the caveat the skill makes (BRAF-pathway inhibitors remain
  investigational in dogs).

**Sources (all [PubMed]):**
- Thomas R, et al. *Whole exome sequencing analysis of canine urothelial carcinomas without BRAF V595E mutation…* PLoS Genet. 2023;19(4):e1010575 ("85% of canine UC harbor an activating BRAF V595E mutation…orthologous to V600E"). DOI: [10.1371/journal.pgen.1010575](https://doi.org/10.1371/journal.pgen.1010575)
- Jung H, et al. *Establishment of Canine Transitional Cell Carcinoma Cell Lines Harboring BRAF V595E…* Int J Mol Sci. 2021;22(17):9151 ("up to 80%…homologous to human V600E"). DOI: [10.3390/ijms22179151](https://doi.org/10.3390/ijms22179151)
- Maeda S, et al. *BRAF Mutation Associates CCL17 Expression and Regulatory T Cell Recruitment in Urothelial Carcinoma of Dogs.* Vet Pathol. 2020;58(5):971–980. DOI: [10.1177/0300985820967449](https://doi.org/10.1177/0300985820967449)
- Aupperle-Lellbach H, et al. *Diagnostic value of the BRAF variant V595E in…canine transitional cell carcinoma.* Tierarztl Prax Ausg K. 2018;46(5):289–295. DOI: [10.15654/TPK-180554](https://doi.org/10.15654/TPK-180554)

---

## Methodology and limitations

- **Sources consulted, in priority order:** PubMed (primary studies, consensus statements,
  reviews); FDA/EMA drug labels and FDA CVM (Equioxx, Metacam/meloxicam, Rimadyl/carprofen,
  Banamine/flunixin, Baytril/enrofloxacin); IRIS, AAHA, ISFM, and NASPHV guidance; and the
  Merck Veterinary Manual. Where a value rests on a textbook standard rather than an indexed
  paper (e.g., the DiBartola KCl sliding scale, Plumb's atropine dose), that is stated
  honestly rather than dressed up with an unrelated citation.
- **PubMed attribution:** citations labeled **[PubMed]** are drawn from records retrieved via
  PubMed; DOI links are included where the record supplied one.
- **This is a literature and label verification.** It complements — and does not replace —
  examination and judgment by a licensed veterinarian. Country- and formulation-specific label
  differences (notably US vs. EU meloxicam in cats) are real and are called out where relevant.
  Report any error via the Clinical Correction issue template (`clinical-accuracy`).

*Review compiled 2026-07-13.*
