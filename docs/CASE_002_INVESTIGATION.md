# Case SIM-2026-002 — Simulated Account Access and Transfer Investigation

**Prepared by:** Caleb Naibei  
**Scope:** Training-only forensic analysis of fictional digital transaction and authentication records.  
**Status:** Hypotheses evaluated; no finding of fraud or attribution to a real person.

## 1. Allegation and scope
A hypothetical customer reports concern about access to account A100. The investigation asks whether access records and subsequent transfers show a correlated sequence warranting escalation, and whether onward transfers can be traced through intermediate accounts. The investigation does not attempt to prove theft, identify a perpetrator, or claim actual loss.

## 2. Evidence register
- E01: `data/case_002/accounts.csv` — account reference and business context
- E02: `data/case_002/auth_events.csv` — login failures, successes and beneficiary event
- E03: `data/case_002/transactions.csv` — transfer identifiers, UTC timestamps, values and device labels

The records are generated deterministically by `src/forensic_pipeline.py`. `reports/case_002/manifest.json` records SHA-256 digests and byte lengths. These are *simulated* acquisition artifacts. A digest detects subsequent file changes but cannot prove provenance, consent, completeness, or an unbroken chain of custody.

## 3. Questions and hypotheses
**H1: Account access changed before outgoing transfers.** The sequence L002/L003 (failed attempts on D9), L004 (successful login on D9), L005 (beneficiary addition) and T001/T002 (transfers from A100 using D9) is temporally consistent with unusual access. The same device label also appears for A200 in L006. This is correlation, not proof of shared human control.

**H2: Value moved through intermediary accounts.** T001 and T002 transfer a combined KES 95,000 from A100 to A200. T003 and T004 then transfer KES 90,000 from A200 to A400 and A500; T005 and T006 later transfer KES 82,000 toward A600. The transfer graph supports a sequence of *possible* onward movement, but the dataset lacks account balances, fees, other flows and fund-level identifiers. It cannot establish that the exact same funds moved along every edge.

**H3: Some suspicious-looking patterns are legitimate.** A300 is designated a merchant payroll aggregator, and T008–T010 are scheduled equal-value API payments. The scenario explicitly includes this counterexample to demonstrate why pattern matches need contextual review.

## 4. Reproducible analytical method
1. Generate three CSV sources using a fixed, transparent scenario.
2. Validate identifiers, account references, positive amounts and timezone-aware timestamps.
3. Hash all three sources and retain their byte sizes.
4. Execute read-only SQL exhibits covering account activity, device correlation, outbound totals and recipient concentration.
5. Apply transparent correlation rules for failed logins followed by transfers and rapid high-value transfers.
6. Build a forward-in-time directed graph of successful transfers; prevent cycles and limit path depth to four.
7. Export chronological event exhibits, evidence-linked findings and trace paths as JSON/CSV.

## 5. Selected chronological exhibits
| UTC offset from scenario start | Record | Observation |
|---|---|---|
| +02m / +03m | L002 / L003 | Two failed login attempts for A100 on D9 |
| +04m | L004 | Successful A100 login on D9 |
| +05m | L005 | Beneficiary-add event on D9 |
| +06m / +08m | T001 / T002 | KES 48,000 and 47,000 from A100 to A200 |
| +10m / +11m | T003 / T004 | KES 60,000 and 30,000 from A200 to A400/A500 |
| +13m / +14m | T005 / T006 | KES 55,000 and 27,000 to A600 |
| +15m | T007 | Failed transfer; excluded from successful-value tracing |
| +22m | T008–T010 | Three payroll-style transfers by A300 |

The exact UTC timestamps are in `reports/case_002/timeline.csv`.

## 6. Findings and evidentiary strength
**Finding F-AUTH-A100:** Two failed logins precede a successful login and subsequent outgoing transfers on device D9. The conclusion is limited to a suspicious sequence in simulated logs. Confidence in the *recorded sequence* is high within the dataset; confidence in an account-takeover allegation is unassessed.

**Finding F-BURST-A100-A200:** Two successful transfers totaling KES 95,000 occurred within ten minutes. Thresholds are illustrative, not empirically calibrated.

**Network trace:** A100 → A200 → A400/A500 → A600 is a time-respecting transfer path. A graph path is not proof of beneficial ownership or of identical funds being relayed.

**Alternative explanation:** Legitimate access from a new device, authorized transfers, payroll batches, shared terminals, or incomplete export coverage could produce similar patterns.

## 7. Limitations and next actions
No real customer testimony, KYC verification, geolocation proof, balance ledger, fee data, source-system attestation, external corroboration or legal authority is available. No real custody record exists.

For a real authorized investigation, preserve original exports read-only, obtain authenticated source metadata and permission, confirm timezone and completeness, document custody events, obtain customer and account-owner explanations, reconcile ledger balances and fees, and have a qualified reviewer evaluate the evidence before escalation.

## 8. Reproduce
```bash
python src/forensic_pipeline.py
python -m unittest discover -s tests -v
```
Inspect `reports/case_002/summary.json`, `findings.json`, `paths.json`, `timeline.csv`, `sql_exhibits.json` and `manifest.json`.

**Professional competencies demonstrated:** SQL analysis, cross-source event correlation, transaction tracing, integrity verification, data quality assurance, structured investigative reporting and careful separation of observation from inference.
