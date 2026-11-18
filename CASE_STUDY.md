# Case study: Digital Transaction Anomaly Investigation

**Analyst:** Caleb Naibei  
**Case reference:** SIM-2026-001  
**Classification:** Educational simulation — fictional transactions and accounts

## Executive summary
This project investigates whether a synthetic mobile-money export contains transaction patterns requiring review. It demonstrates a reproducible workflow using Python, SQL, evidence hashing, and documented findings. No identified pattern is treated as proof of wrongdoing.

## Investigative questions
- Are there unusually rapid transfers between the same two accounts?
- Do recipients collect transfers from unusually many distinct senders?
- Can an analyst reproduce the results and verify the original file has not changed?

## Evidence and preservation
A deterministic Python generator creates 521 fictional records with UTC timestamps, sender and recipient identifiers, amounts in KES, statuses, and channels. A SHA-256 hash is recorded in `reports/evidence_manifest.json`. The manifest documents a simulated export, not a real acquisition. Hashes verify byte-for-byte consistency, not the authenticity of an original source. The chain-of-custody template is intentionally blank.

## Analysis
SQL queries summarize recipient concentration, repeated sender-recipient transfers, and the chronological transaction sequence. Python applies two transparent rules: at least eight transfers between the same parties within ten minutes, and at least eight distinct senders paying one recipient. The synthetic generator deliberately includes a rapid burst between U007 and U099 and many-to-one activity toward U140.

## Findings and interpretation
The planted patterns are detected by the rules. The full number of rule flags is calculated at runtime and can include incidental hits in the randomized background data. One recipient may generate a concentration flag without any fraudulent activity. A burst could also reflect a legitimate automated payout. Flags are leads for review, not adjudications.

## Limitations
The dataset is synthetic, no rule thresholds were calibrated against labeled real cases, and no interviews, device records, legal authorizations, or independent corroborating sources exist. There is no genuine chain of custody. The exercise does not establish guilt, identity, loss, or financial crime.

## Recommendations
Verify provenance and lawful authority before analyzing real records; retain read-only originals and record each authorized access; compare patterns against business context and corroborating records; document false positives; escalate only when independently supported.

## Reproduce
```bash
python src/investigate.py
python -m unittest discover -s tests -v
```
Review `reports/case_report.md`, `reports/flags.json`, `reports/sql_results.json`, and the Excel-compatible CSV. Compare the manifest SHA-256 against a fresh digest of `data/transactions.csv`.

**Skills demonstrated:** SQL investigation, Python analysis, reproducible evidence handling, analytical reporting, and cautious interpretation.
