# Digital Transaction Forensics & Fraud Investigation Platform

**Portfolio by Caleb Naibei | SQL • Python • Digital evidence analysis**

A reproducible, evidence-led **simulation** of digital transaction investigations. It correlates authentication events with transfers, traces time-respecting transaction paths, validates data quality, and produces hashed evidence inventories and auditable exhibits.

> **Ethics:** All records are fictional. Anomaly flags, shared device labels and transfer paths are **not evidence of criminal guilt**. No real customer data or real chain of custody is claimed.

## Featured investigation — SIM-2026-002
**Scenario:** A hypothetical account-access complaint followed by rapid transfers, onward movements through intermediaries, and a legitimate payroll-like counterexample.

**Sources:** `accounts.csv`, `auth_events.csv`, `transactions.csv` (generated deterministically).

**Investigation workflow:** source generation → validation → SHA-256 manifest → SQL exhibits → authentication correlation → temporal transaction graph → timeline → evidence-linked case findings.

**Read the complete forensic report:** [Full forensic report, evidence matrix and timeline](docs/FULL_FORENSIC_REPORT_SIM-2026-002.md).\n\n**Inspect the exact synthetic datasets:** [Accounts](data/case_002/accounts.csv) · [Authentication events](data/case_002/auth_events.csv) · [Transactions](data/case_002/transactions.csv).\n\n**Short case study:** [SIM-2026-002 investigation](docs/CASE_002_INVESTIGATION.md).

## Run in VS Code (Python 3.9+; no external dependencies)
```bash
python src/forensic_pipeline.py
python -m unittest discover -s tests -v
```
Windows alternative: use `py` instead of `python`.

**Review generated exhibits** in `reports/case_002/`:
- `summary.json` — counts and validation outcome
- `manifest.json` — source file hashes and byte sizes
- `findings.json` — hypotheses linked to record identifiers
- `paths.json` — directed, chronological transaction paths
- `timeline.csv` — Excel-compatible event reconstruction
- `sql_exhibits.json` — read-only query results

## Architecture
```text
Deterministic synthetic sources (3 CSVs)
    ├── data-quality and referential checks
    ├── SHA-256 evidence inventory
    ├── SQLite read-only analytical exhibits
    ├── login / device / transfer correlation
    └── temporal transfer-graph traversal
            ↓
      JSON + CSV investigation exhibits
            ↓
      documented findings and limitations
```

## Scope and caveats
This is a training portfolio, not a production fraud detection system. There is no authentication to a real payments API, no customer PII, no calibrated fraud model, no real legal authorization and no true forensic acquisition. The graph demonstrates plausible transfer *paths*, not tracing of identical money units. A file hash checks consistency, not provenance.

## Legacy exercise
The earlier, smaller demonstration remains available at `src/investigate.py` and `CASE_STUDY.md`; SIM-2026-002 is the featured, more detailed investigation.

## Author
Caleb Naibei — database administration, SQL analysis, Python automation and systems security.
