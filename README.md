# Digital Transaction Anomaly Investigation

**Forensic investigation portfolio | Synthetic mobile-money transaction data**

A reproducible case study demonstrating SQL-based transaction review, Python anomaly detection, SHA-256 evidence integrity checks, investigative reporting, and chain-of-custody documentation.

**Case ID:** SIM-2026-001. All account IDs and transactions are fictional. A flagged pattern is **not proof of fraud**.

## Run
Requires Python 3.9+; no third-party packages.

```bash
python src/investigate.py
python -m unittest discover -s tests -v
```

Review `reports/case_report.md`, `reports/flags.json`, `reports/sql_results.json`, and `reports/flagged_transactions.csv` in Excel.

## Investigation process
1. Generate deterministic synthetic transaction records.
2. Hash the source CSV with SHA-256 and document provenance.
3. Run read-only SQLite queries from `sql/investigation.sql`.
4. Apply transparent anomaly-detection rules.
5. Export reproducible results and prepare a written case study.
6. Use the custody template for a simulated exercise only.

## Caveats
This is a training simulation, not a real investigation. SHA-256 establishes file consistency, not authenticity or an unbroken custody chain. Rule thresholds are illustrative and have not been validated on labeled fraud cases. Do not upload actual customer data.

## Portfolio author
Caleb Naibei — SQL, Python, database administration and systems security.
