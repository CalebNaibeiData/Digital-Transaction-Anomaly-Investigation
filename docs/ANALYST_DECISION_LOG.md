# Analyst decision log — SIM-2026-002

This document records *why* each investigative step was chosen. It is a simulated analyst workpaper, not a real custody record.

| Decision | Supporting record(s) | Reasoning | Risk of a misleading conclusion |
|---|---|---|---|
| Start with access chronology, not transfer amount | L001–L005 | Two failed attempts on D9 precede a successful A100 login and beneficiary event | Device label might represent a shared terminal, testing or inaccurate instrumentation |
| Include T001 and T002 in successful outgoing value | T001, T002 | Both have SUCCESS status; total KES 95,000 | No proof the transfers were unauthorized |
| Exclude T007 from transferred value | T007 | Status is FAILED | An attempted transfer is not completed movement |
| Examine A200 as a possible intermediary | T001–T004 | Receives KES 95,000; subsequently sends KES 90,000 | Missing balances, fees, reversals and other activity prohibit exact fund tracing |
| Follow two branches to A600 | T003–T006 | Timestamp order permits A200→A400/A500→A600 | Graph reachability is not evidence of beneficial ownership or identical funds |
| Examine shared device D9 | L004, L006, T001–T004 | Device identifier appears across A100 and A200 events | Shared device does not establish a shared human operator |
| Retain A300 batch-payment comparator | E01, T008–T010 | Three equal API transfers could look suspicious without context | Account metadata is a synthetic scenario assertion, not verified business documentation |
| Do not label any account fraudulent | All records | The dataset lacks corroboration, owner testimony and independent source verification | Overstating evidence would undermine the report |

## Working hypotheses

**H1 — Unauthorized access:** Supported as an *investigative lead* by L002–L005 and T001–T002. Falsification requires verified account-holder confirmation, device enrollment, and independent session records.

**H2 — Coordinated onward transfers:** Supported as a *chronological routing hypothesis* by T001–T006. Falsification requires full ledgers, opening balances, reversals, settlement details and authorized counterparty context.

**H3 — Legitimate transactions with coincidental indicators:** Remains plausible. A300's payroll-like batch is a deliberate negative-control example showing why a rule match alone is insufficient.

## Known analytical constraints

- All account IDs, device labels, timestamps and payments are fictional.
- Source data was created to contain these patterns; detecting them is **not** independent validation of model performance.
- The rules do not report sensitivity, specificity or false-positive rates.
- The case covers only 25 minutes and cannot establish historical behavioral baselines.
- The file manifest records digest values, not actual chain-of-custody events.
- An investigative report should preserve exculpatory explanations and avoid implying criminal responsibility.

## Reviewer challenge questions

1. Why is KES 95,000 an observed transfer amount rather than a confirmed loss?
2. What additional evidence would distinguish account takeover from authorized access?
3. Why is it incorrect to add every hop and call the sum stolen funds?
4. Could A300's API payments trigger a simplistic concentration rule?
5. Which parts of this workflow would need redesign before handling real customer data?

A defensible answer to each question is part of the portfolio's intended assessment.
