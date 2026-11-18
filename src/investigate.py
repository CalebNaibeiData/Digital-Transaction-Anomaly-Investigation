"""Reproducible synthetic transaction investigation. No real customer data."""
import csv
import hashlib
import json
import random
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["transaction_id", "timestamp_utc", "sender_id", "recipient_id", "amount_kes", "status", "channel"]

def generate():
    rng = random.Random(20261113)
    base = datetime(2026, 10, 1, tzinfo=timezone.utc)
    rows = []
    for i in range(500):
        stamp = base + timedelta(minutes=rng.randrange(14 * 24 * 60))
        rows.append([f"TX{i+1:05}", stamp.isoformat(), f"U{rng.randrange(1,81):03}",
                     f"U{rng.randrange(81,150):03}", rng.randrange(100,20000), "SUCCESS", "APP"])
    for i in range(12):
        rows.append([f"BURST{i+1:03}", (base+timedelta(days=3,hours=9,seconds=45*i)).isoformat(),
                     "U007", "U099", 9500, "SUCCESS", "APP"])
    for i in range(9):
        rows.append([f"SPLIT{i+1:03}", (base+timedelta(days=6,hours=13,minutes=4*i)).isoformat(),
                     f"U{i+20:03}", "U140", 9900, "SUCCESS", "USSD"])
    rows.sort(key=lambda r: (r[1], r[0]))
    target = ROOT / "data" / "transactions.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(FIELDS)
        writer.writerows(rows)
    return target

def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

def analyze(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        records = list(csv.DictReader(f))
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("""CREATE TABLE transactions(
            transaction_id TEXT PRIMARY KEY, timestamp_utc TEXT, sender_id TEXT,
            recipient_id TEXT, amount_kes INTEGER, status TEXT, channel TEXT)""")
        conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?)",
            [(r["transaction_id"],r["timestamp_utc"],r["sender_id"],r["recipient_id"],
              int(r["amount_kes"]),r["status"],r["channel"]) for r in records])
        sql_results = []
        sql = (ROOT / "sql" / "investigation.sql").read_text(encoding="utf-8")
        for statement in sql.split(";"):
            statement = "\n".join(line for line in statement.splitlines()
                                   if not line.lstrip().startswith("--")).strip()
            if not statement:
                continue
            if not statement.lower().startswith("select"):
                raise ValueError("Only SELECT investigation queries are allowed")
            cur = conn.execute(statement)
            sql_results.append({"query": statement, "columns": [c[0] for c in cur.description],
                                "rows": cur.fetchall()})
    finally:
        conn.close()
    grouped = defaultdict(list)
    for record in records:
        if record["status"] == "SUCCESS":
            grouped[(record["sender_id"],record["recipient_id"])].append(record)
    flags = []
    for (sender,recipient), group in sorted(grouped.items()):
        group.sort(key=lambda r:r["timestamp_utc"])
        for i,record in enumerate(group):
            start = datetime.fromisoformat(record["timestamp_utc"])
            window = []
            for candidate in group[i:]:
                if datetime.fromisoformat(candidate["timestamp_utc"]) - start <= timedelta(minutes=10):
                    window.append(candidate)
                else:
                    break
            if len(window) >= 8:
                flags.append({"rule":"burst_8_in_10m","sender_id":sender,"recipient_id":recipient,
                              "count":len(window),"first_timestamp_utc":record["timestamp_utc"],
                              "transaction_ids":[r["transaction_id"] for r in window]})
                break
    recipients = defaultdict(list)
    for r in records:
        if r["status"] == "SUCCESS":
            recipients[r["recipient_id"]].append(r)
    for recipient, group in sorted(recipients.items()):
        distinct = {r["sender_id"] for r in group}
        if len(distinct) >= 8:
            flags.append({"rule":"many_to_one_8_senders","recipient_id":recipient,
                          "distinct_senders":len(distinct),"transaction_count":len(group)})
    return records, flags, sql_results

def run():
    path = generate()
    records, flags, sql_results = analyze(path)
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    manifest = {"case_id":"SIM-2026-001","source":"Deterministic synthetic generator",
                "file":"data/transactions.csv","sha256":sha256(path),
                "record_count":len(records),"classification":"SIMULATION"}
    for name, obj in [("evidence_manifest.json",manifest),("flags.json",flags),
                      ("sql_results.json",sql_results)]:
        (out/name).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
    with (out/"flagged_transactions.csv").open("w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rule","sender_id","recipient_id","count","first_timestamp_utc","transaction_ids"])
        for flag in flags:
            writer.writerow([flag["rule"],flag.get("sender_id",""),flag.get("recipient_id",""),
                flag.get("count",flag.get("transaction_count","")),flag.get("first_timestamp_utc",""),
                "|".join(flag.get("transaction_ids",[]))])
    report = f"""# Case SIM-2026-001 — Synthetic Transaction Investigation

**Scope:** Identify patterns for human review; no real accounts or fraud allegations.

## Method
Deterministic dataset generation, SHA-256 source hashing, read-only SQLite queries,
rolling ten-minute burst analysis, many-to-one recipient analysis, and CSV export.

## Results
- Transactions analyzed: **{len(records)}**
- Rule-based flags: **{len(flags)}** (not unique incidents; may overlap)
- Planted burst: U007 to U099; planted many-to-one pattern: U140.
- Evidence SHA-256: `{manifest['sha256']}`

## Interpretation
These indicators justify further review, not a fraud conclusion. Legitimate bulk
payments and shared collection accounts can generate similar patterns.

## Limitations
Synthetic data; no validated precision/recall, interviews, source-system verification,
customer consent records or real chain of custody. A hash does not prove authenticity.

## Recommendations
Preserve authorized source exports, document access and transfers, validate against
additional records, review false positives, and escalate only under approved procedures.
"""
    (out/"case_report.md").write_text(report,encoding="utf-8")
    print(f"Analyzed {len(records)} synthetic transactions; generated {len(flags)} flags.")

if __name__ == "__main__":
    run()
