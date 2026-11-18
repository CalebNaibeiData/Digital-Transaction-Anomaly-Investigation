# Case SIM-2026-002 | The 14-minute transfer chain

**A simulated digital-payments investigation by Caleb Naibei**

At 08:02 UTC, account **A100** records an unsuccessful login from device **D9**. Another fails one minute later. At 08:04, D9 successfully accesses A100. A beneficiary-add event follows, then two transfers totaling **KES 95,000** leave A100 for A200.

Within minutes, A200 distributes **KES 90,000** to two accounts. Both later transfer value to A600. The same device identifier D9 also appears in A200's access records.

**Investigative question:** Is this an unauthorized access and coordinated transfer sequence—or a legitimate series of payments whose context is absent from the export?

> **This is a deliberately constructed, fictional case.** The timestamps, account labels and transactions are synthetic. The evidence supports a sequence of events, not a finding of fraud, actual loss or human attribution.

## Case at a glance

| Case detail | Observed in synthetic records |
|---|---|
| Case reference | SIM-2026-002 |
| Event window | 12 October 2026, 08:00–08:25 UTC |
| Evidence sources | Account register, authentication log, transaction ledger |
| Source records | 7 accounts · 7 authentication/activity events · 11 transactions |
| Transaction outcomes | 10 successful · 1 failed |
| A100 → A200 | T001 + T002 = KES 95,000 |
| A200 → A400 / A500 | T003 + T004 = KES 90,000 |
| A400 / A500 → A600 | T005 + T006 = KES 82,000 |
| Important caveat | Multi-hop graph paths do not prove the same funds were relayed |

## The sequence under examination

```text
08:02  L002  A100 login FAILED on D9
08:03  L003  A100 login FAILED on D9
08:04  L004  A100 login SUCCESS on D9
08:05  L005  A100 beneficiary added on D9
08:06  T001  A100 ── KES 48,000 ──► A200
08:07  L006  A200 login SUCCESS on D9
08:08  T002  A100 ── KES 47,000 ──► A200
08:10  T003  A200 ── KES 60,000 ──► A400
08:11  T004  A200 ── KES 30,000 ──► A500
08:13  T005  A400 ── KES 55,000 ──► A600
08:14  T006  A500 ── KES 27,000 ──► A600
08:15  T007  A100 ── KES 12,000 ──► A200  FAILED
```

The graph shows **chronologically possible routes**, not a proven tracing of specific funds. Transfers from a separate merchant account (A300) provide a benign batch-payment counterexample.

## Read the investigation, not just the code

- **[Full forensic investigation report](docs/FULL_FORENSIC_REPORT_SIM-2026-002.md)** — methodology, evidence register, chronological exhibits, financial reconstruction, alternative hypotheses and next investigative steps
- **[Analyst's decision log](docs/ANALYST_DECISION_LOG.md)** — why each analytic decision was made, what could mislead the analyst, and what corroboration is missing
- **[Evidence: transactions.csv](data/case_002/transactions.csv)** — inspect T001–T011
- **[Evidence: auth_events.csv](data/case_002/auth_events.csv)** — inspect L001–L007
- **[Evidence: accounts.csv](data/case_002/accounts.csv)** — account types and scenario context
- **[SQL investigation exhibits](sql/case_002.sql)** — source-level queries
- **[Python investigation engine](src/forensic_pipeline.py)** — validation, correlation, chronological graph traversal and report exports

## Reproduce the findings

Python 3.9+ is sufficient; there are no third-party dependencies.

```bash
git clone https://github.com/CalebNaibeiData/Digital-Transaction-Anomaly-Investigation.git
cd Digital-Transaction-Anomaly-Investigation
python -m pip install -r requirements.txt
python src/forensic_pipeline.py
python -m unittest discover -s tests -v
```

The run generates `reports/case_002/summary.json`, `manifest.json`, `findings.json`, `paths.json`, `timeline.csv` and `sql_exhibits.json`. The manifest contains SHA-256 hashes for the three source CSVs. Those hashes confirm byte consistency only, not independent provenance.

**Important reproducibility detail:** The generator deliberately rewrites the three committed CSVs with identical deterministic content. If the source files are modified for an experiment, save a copy first. The analysis uses the synthetic case generator, not a general-purpose ingestion system for arbitrary bank exports.

## What this project does—and does not—demonstrate

**Demonstrates:** Joining transaction and authentication evidence; constructing a minute-by-minute event chronology; separating successful from failed payments; time-respecting transfer-path analysis; read-only SQL exhibits; source hashing; evidence-referenced investigative writing; explicit alternative hypotheses.

**Does not demonstrate:** Real evidence acquisition, actual chain of custody, proven identity, account takeover attribution, calibrated fraud classification, customer loss, regulatory compliance certification or admissibility in court.

The older introductory rule-based exercise remains at `src/investigate.py` for comparison; **SIM-2026-002 is the featured investigation**.

---

**Investigator / developer:** Caleb Naibei · Python, SQL, database administration and secure systems.
