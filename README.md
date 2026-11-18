# Investigation Workbench | Case SIM-2026-002

**Caleb Naibei · Digital transaction investigation · Python / SQL**

At 08:02 UTC, account A100 records a failed login on device D9. A second attempt fails. Two minutes later, D9 successfully accesses A100; a beneficiary is added and KES 95,000 moves to A200. Transfers from A200 to two other accounts follow, and both later transfer value to A600.

**Is this unauthorized access and coordinated transfer activity, or a legitimate series of payments with missing context?** This repository investigates the sequence rather than treating a rule match as a verdict.

> All evidence is synthetic. No real customer, loss, perpetrator, or verified chain of custody is represented.

## Explore the investigation

**[Open the interactive investigation dashboard](dashboard/index.html)** — download/open the HTML file locally, or view it through a static web server. It initially displays the 11-record case. Load the extended CSV for a seven-day dataset.

**[Full forensic report](docs/FULL_FORENSIC_REPORT_SIM-2026-002.md)** · **[Analyst decision log](docs/ANALYST_DECISION_LOG.md)** · **[Dataset methodology](docs/EXTENDED_DATASET_METHODOLOGY.md)**

### Case evidence (committed CSVs)
- [Transaction evidence T001–T011](data/case_002/transactions.csv)
- [Authentication evidence L001–L007](data/case_002/auth_events.csv)
- [Account reference](data/case_002/accounts.csv)

### Extended investigation dataset

The deterministic generator produces **2,440 synthetic payment records**: 2,400 background transfers, 12 rapid-sender transfers, four onward-path transfers, 16 payroll-like payments and eight recipient-concentration transfers. The scenario metadata is **not** verified fraud ground truth.

```bash
python src/generate_extended_dataset.py
```

The output is `data/extended/transactions.csv` with a SHA-256 generation manifest. Open `dashboard/index.html` and select the generated CSV to explore it. No package installation, web server or network connection is needed.

### Reproduce the case and run tests

```bash
python -m pip install -r requirements.txt
python src/forensic_pipeline.py
python src/generate_extended_dataset.py
python -m unittest discover -s tests -v
```

Python 3.9+; standard library only. The case pipeline writes evidence manifests, SQL exhibits, time-respecting paths and a timeline under `reports/case_002/`.

## Analytical boundaries

- Graph connections show possible chronological transfer routes, not tracing of identical funds.
- Successful transfer value is not the same as actual financial loss.
- A device label is not human attribution.
- Source-file SHA-256 digests establish consistency, not independent authenticity.
- The extended dataset was planted with test patterns; it cannot support precision/recall or production fraud-detection claims.
- The workbench is a local training interface, not a secured system for handling real personal data.

The legacy beginner exercise remains at `src/investigate.py` for comparison.
