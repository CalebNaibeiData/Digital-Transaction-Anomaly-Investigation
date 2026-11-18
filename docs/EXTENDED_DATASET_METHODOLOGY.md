# Extended synthetic dataset — methodology and cautions

The extended dataset is intended to test whether an analyst can find a small set of conspicuous patterns **within ordinary-looking payment activity**, rather than merely read a hand-picked eleven-row example.

## Dataset design

Run `python src/generate_extended_dataset.py`. The script generates **2,440 transaction records** over a seven-day interval:
- **2,400 background transactions**, across 180 personal accounts and 20 merchant accounts, with varied payment amounts, timestamps, channels, device labels, recipients and a small proportion of failures.
- **12 rapid sender transactions** from AC0001 to AC0170, deliberately planted.
- **4 subsequent transfers** through AC0170, AC0171 and AC0172 toward AC0173.
- **16 scheduled-payroll-like payments** from MC001.
- **8 recipient-concentration transfers** into AC0160.

The `scenario_tag` column is **generator metadata for demonstration and tests**, not an externally verified fraud label. Investigators should hide this field when performing blind analysis. There is no independent ground truth, and precision/recall claims would be misleading.

## Reproducibility

The generator uses a fixed seed (`20261012`), stable sorting and UTF-8 CSV output. `data/extended/generation_manifest.json` records counts and the SHA-256 digest of the generated CSV. Running it twice with the same parameters should produce byte-identical output.

The generated CSV is deliberately not checked into Git: it is reproducible source data, and this avoids bloating diffs. The smaller Case SIM-2026-002 source CSVs **are** checked in for direct inspection.

## Investigation workbench

Open `dashboard/index.html` in a modern browser, then select `data/extended/transactions.csv`. No server or external library is required; the file is read locally. The dashboard offers:
- account filter, status filter, scenario metadata filter;
- successful value and failed-transfer counts;
- top transaction relationships as a clickable network;
- per-day activity chart;
- evidence table and filtered CSV export.

**Analytical caveats:** The dashboard is a training visualization, not a validated anomaly classifier. Its network ranks edges by aggregate value and does not claim fund identity. The dataset's synthetic merchant and device assignments do not replicate a real provider's operational controls. Avoid using this workbench with confidential customer data without a proper security and privacy review.
