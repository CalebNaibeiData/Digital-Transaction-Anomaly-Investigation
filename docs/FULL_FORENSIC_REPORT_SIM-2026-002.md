# Full Forensic Investigation Report — SIM-2026-002

**Prepared by:** Caleb Naibei  
**Report type:** Digital transaction and authentication event correlation  
**Case classification:** SYNTHETIC EDUCATIONAL SIMULATION — NOT A REAL INCIDENT  
**Evidence period:** 12 October 2026, 08:00–08:25 UTC  
**Report status:** Reproducible analytical exercise; no criminal or disciplinary finding

---

## 1. Executive summary

This simulated investigation assesses a hypothetical concern involving account **A100**. Three synthetic source files—account metadata, authentication events and transaction records—were reviewed for indications of anomalous access, rapid transfers, shared-device activity and potential onward transfer paths.

The provided dataset contains **7 accounts**, **7 authentication/activity events**, and **11 transaction records** (**10 successful**, **1 failed**). The ten successful transactions total **KES 377,000** in gross transfer value; this is the sum of transaction amounts, **not net loss** and **not unique money**. A100 sent two successful transfers totaling **KES 95,000** to A200 after two failed login attempts, a successful login and a beneficiary-add event on device D9. A200 subsequently sent KES 90,000 to A400 and A500; those accounts later sent KES 82,000 in aggregate to A600.

The sequence merits further investigation **within the fictional scenario**. It does not establish account takeover, common ownership, the movement of identical funds, or fraud. The dataset intentionally includes payroll-like transactions from A300 as a plausible benign comparator.

## 2. Mandate, questions and boundaries

**Mandate:** Evaluate the records supplied for a simulated account-access concern and prepare evidence-referenced observations. No authority to access external systems or real personal data is implied.

**Investigative questions:**
1. Did A100 experience failed and successful access events before the transfers?
2. Were the transfers made using a device identifier also present in authentication records?
3. What are the amounts, timing, and counterparties of the transfers?
4. Which onward transfer paths are consistent with chronological order?
5. Which benign explanations remain plausible?
6. Can another analyst regenerate the dataset, verify file integrity, and reproduce the analytical exhibits?

**Out of scope:** Determining criminal intent, identity of a human operator, true beneficial ownership, exact fund provenance, actual loss, regulatory breach or legal admissibility.

## 3. Evidence inventory and provenance

| Evidence ID | File | Description | Records |
|---|---|---|---:|
| E01 | `data/case_002/accounts.csv` | Fictional account types and contextual notes | 7 |
| E02 | `data/case_002/auth_events.csv` | Authentication and beneficiary-change activity | 7 |
| E03 | `data/case_002/transactions.csv` | Timestamped fictional transfers and device labels | 11 |

All files are generated from the committed Python source `src/forensic_pipeline.py`. The exact CSV files are also committed so a reviewer can inspect them without executing code. The program produces `reports/case_002/manifest.json` containing SHA-256 digests and byte counts. Hash verification detects byte-level changes **relative to a recorded digest**; it does not prove original source authenticity. No genuine acquisition, preservation warrant, evidence seal, custody transfer or forensic imaging occurred.

**Dataset dictionary:** `timestamp_utc` is ISO-8601 UTC; `amount_kes` is an integer Kenyan-shilling amount; `status` distinguishes SUCCESS from FAILED; `session_device_id` and `device_id` are synthetic labels; `ip_address` uses documentation-only address ranges and is not geolocation evidence.

## 4. Validation and analytical methodology

1. Verify unique record IDs and cross-reference every account ID against E01.
2. Parse timezone-aware event timestamps and require positive transaction amounts.
3. Preserve the original synthetic CSV bytes and compute their SHA-256 digests.
4. Query the transactions and authentication records in in-memory SQLite with read-only `SELECT` statements in `sql/case_002.sql`.
5. Correlate login failures with a subsequent successful login on the same device and outgoing transfers within the specified time window.
6. Flag repeated high-value transfers to a common recipient within ten minutes. This rule is illustrative and is **not** statistically validated.
7. Traverse only successful transactions in chronological order, with cycle avoidance and a maximum four-hop depth. Graph paths are **potential routing sequences**, not money-laundering determinations.
8. Export `findings.json`, `paths.json`, `timeline.csv`, `sql_exhibits.json`, `manifest.json` and `summary.json` for independent review.

The source implementation is intentionally transparent and uses Python's standard library. It does not claim to be a validated forensic suite.

## 5. Reconstructed chronology

All times are UTC on 12 October 2026.

| Time | Evidence | Observation | Analytical significance |
|---|---|---|---|
| 08:00 | L001 | Successful A100 login on D1 | Baseline observed device |
| 08:02 | L002 | Failed A100 login on D9 | First unsuccessful attempt |
| 08:03 | L003 | Failed A100 login on D9 | Second unsuccessful attempt |
| 08:04 | L004 | Successful A100 login on D9 | Device-access sequence |
| 08:05 | L005 | Beneficiary-add event for A100 on D9 | Relevant account change |
| 08:06 | T001 | A100 → A200, KES 48,000, success, D9 | First successful transfer |
| 08:07 | L006 | Successful A200 login on D9 | Shared device label across accounts |
| 08:08 | T002 | A100 → A200, KES 47,000, success, D9 | Second successful transfer |
| 08:10 | T003 | A200 → A400, KES 60,000, success, D9 | First onward transfer |
| 08:11 | T004 | A200 → A500, KES 30,000, success, D9 | Second onward transfer |
| 08:13 | T005 | A400 → A600, KES 55,000, success, D4 | Later transfer to A600 |
| 08:14 | T006 | A500 → A600, KES 27,000, success, D5 | Later transfer to A600 |
| 08:15 | T007 | A100 → A200, KES 12,000, **FAILED** | Excluded from successful totals |
| 08:20 | L007 | Successful A300 login on D3 | Benign comparison context |
| 08:22 | T008–T010 | A300 → A400/A500/A600, KES 10,000 each | Payroll-like batch |
| 08:25 | T011 | A700 → A300, KES 80,000 | Additional business transfer |

## 6. Financial and network exhibits

### Exhibit A — Account A100

T001 and T002 are two successful transfers to A200 totaling **KES 95,000** within two minutes. T007 is a separate failed attempt for KES 12,000 and **must not** be counted as successfully transferred value. The existence of a beneficiary-add event before T001 is relevant, but the export does not independently prove whether that change authorized the transfers.

### Exhibit B — A200 as intermediary

A200 receives KES 95,000 in the visible dataset and subsequently sends **KES 60,000** to A400 (T003) and **KES 30,000** to A500 (T004). The visible outgoing amount is KES 90,000. The KES 5,000 difference is not necessarily a fee, balance or retained proceeds; there is no full account ledger.

### Exhibit C — Paths toward A600

The time-respecting graph contains two three-hop paths:
- **A100 → A200 → A400 → A600** via T001/T002, T003 and T005.
- **A100 → A200 → A500 → A600** via T001/T002, T004 and T006.

A400 and A500 transfer KES 55,000 and KES 27,000 respectively to A600, totaling **KES 82,000**. The graph cannot determine whether the exact money received from A100 funded these later transfers. A600 also receives KES 10,000 from A300 as part of the benign comparison scenario.

### Exhibit D — Shared-device indicator

D9 appears on the A100 login and outgoing transfer sequence, and also on A200 login/transfer records. This may indicate a shared device, a test harness, delegated access, an inaccurate device identifier, or coordinated activity. **It does not identify a person.** The IP field is a synthetic documentation address and cannot substantiate geographic claims.

### Exhibit E — Benign comparison

A300 is designated a merchant payroll aggregator in the synthetic metadata and sends three equal KES 10,000 API transfers at 08:22. This scenario illustrates that concentration and synchronized payments can be legitimate. The contextual note is simulated, not independent proof of lawful purpose.

## 7. Findings matrix

| Finding | Supporting evidence | Observation | What remains unproven |
|---|---|---|---|
| F01 — access anomaly | L002, L003, L004, L005, T001, T002 | Failed attempts, success, account change and transfers on D9 | Unauthorized access, identity, intent |
| F02 — rapid transfers | T001, T002 | KES 95,000 to A200 in two minutes | Fraudulent purpose or actual loss |
| F03 — shared device | L004, L006, T001–T004 | D9 used in records for A100 and A200 | Same operator or collusion |
| F04 — onward routing | T001–T006 | Chronological multi-hop transfer paths | Movement of the identical funds |
| F05 — failed transaction | T007 | Attempt for KES 12,000 failed | Any successful value movement |
| F06 — plausible benign pattern | L007, T008–T010, E01 | Equal-value API batch from merchant account | Independent legitimacy verification |

**Overall assessment:** The *recorded synthetic chronology* supports a hypothesis warranting further review. Confidence in the underlying allegation cannot be rated from this simulation; a real case would require independently authenticated records and contextual corroboration.

## 8. Alternative explanations and falsification tests

**Authorized user activity:** Obtain authorized customer confirmation and device enrollment records.  
**Shared or delegated device:** Compare verified device enrollment and access-control policies.  
**Routine business transfers:** Obtain contracts, payroll instructions, recipient relationships and payment approvals.  
**Incomplete financial picture:** Reconcile opening/closing balances, reversals, fees, pending transactions and omitted channels.  
**Logging artifact:** Verify system clocks, event schemas, session-to-device mappings and export completeness.

A robust investigation should actively seek evidence that contradicts the suspicious hypothesis, rather than selecting only supporting records.

## 9. Evidence handling, confidentiality and limitations

- Treat original exports as read-only; work on documented copies and retain cryptographic digests.
- Restrict real investigations to authorized, necessary data and record every custody/access event.
- Do not infer identities from account IDs, IP labels or device IDs alone.
- Avoid claiming an unbroken custody chain for this synthetic exercise.
- Preserve exculpatory records and document all analytical thresholds.
- The dataset has **no labeled ground truth suitable for estimating precision or recall**; the rules are not production-grade.
- This exercise cannot demonstrate actual legal admissibility, customer loss or criminal responsibility.

## 10. Recommended next investigative actions

1. Secure authenticated transaction and access exports under proper authority.
2. Confirm whether the customer recognizes D9 and approved the beneficiary change.
3. Reconcile A100, A200, A400, A500 and A600 against full ledgers, fees and reversals.
4. Check source-system session identifiers and independently validated device records.
5. Review counterparty context and possible legitimate business relationships.
6. Prepare a balanced, reviewed escalation memo only if corroborating evidence supports it.

## 11. Reproducibility instructions

```bash
python src/forensic_pipeline.py
python -m unittest discover -s tests -v
```

Open `data/case_002/` to inspect the actual dataset. Open `reports/case_002/` after execution to inspect the hash manifest, SQL exhibits, trace paths, timeline and machine-readable findings. All code and evidence files are versioned in this repository.

**Disclosure:** This report describes fictional data and an educational exercise. It must not be presented as a real forensic engagement or verified allegation.
