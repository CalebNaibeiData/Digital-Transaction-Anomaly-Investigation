"""Evidence-led simulated digital transaction investigation; stdlib only."""
from __future__ import annotations
import csv
import hashlib
import json
import sqlite3
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "case_002"
OUT = ROOT / "reports" / "case_002"
START = datetime(2026, 10, 12, 8, 0, tzinfo=timezone.utc)

def stamp(minutes):
    return (START + timedelta(minutes=minutes)).isoformat()

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def generate():
    """Fixed, declared scenarios; no personal or real transaction records."""
    accounts = [
        {"account_id":"A100","type":"PERSONAL","risk_note":"reported access concern"},
        {"account_id":"A200","type":"PERSONAL","risk_note":"unknown"},
        {"account_id":"A300","type":"MERCHANT","risk_note":"legitimate payroll aggregator"},
        {"account_id":"A400","type":"PERSONAL","risk_note":"unknown"},
        {"account_id":"A500","type":"PERSONAL","risk_note":"unknown"},
        {"account_id":"A600","type":"PERSONAL","risk_note":"unknown"},
        {"account_id":"A700","type":"BUSINESS","risk_note":"scheduled supplier payments"},
    ]
    logins = [
        {"event_id":"L001","timestamp_utc":stamp(0),"account_id":"A100","device_id":"D1","ip_address":"198.51.100.10","result":"SUCCESS","event_type":"LOGIN"},
        {"event_id":"L002","timestamp_utc":stamp(2),"account_id":"A100","device_id":"D9","ip_address":"203.0.113.50","result":"FAILED","event_type":"LOGIN"},
        {"event_id":"L003","timestamp_utc":stamp(3),"account_id":"A100","device_id":"D9","ip_address":"203.0.113.50","result":"FAILED","event_type":"LOGIN"},
        {"event_id":"L004","timestamp_utc":stamp(4),"account_id":"A100","device_id":"D9","ip_address":"203.0.113.50","result":"SUCCESS","event_type":"LOGIN"},
        {"event_id":"L005","timestamp_utc":stamp(5),"account_id":"A100","device_id":"D9","ip_address":"203.0.113.50","result":"SUCCESS","event_type":"BENEFICIARY_ADD"},
        {"event_id":"L006","timestamp_utc":stamp(7),"account_id":"A200","device_id":"D9","ip_address":"203.0.113.50","result":"SUCCESS","event_type":"LOGIN"},
        {"event_id":"L007","timestamp_utc":stamp(20),"account_id":"A300","device_id":"D3","ip_address":"198.51.100.30","result":"SUCCESS","event_type":"LOGIN"},
    ]
    transactions = [
        {"transaction_id":"T001","timestamp_utc":stamp(6),"sender_id":"A100","recipient_id":"A200","amount_kes":"48000","status":"SUCCESS","channel":"APP","session_device_id":"D9"},
        {"transaction_id":"T002","timestamp_utc":stamp(8),"sender_id":"A100","recipient_id":"A200","amount_kes":"47000","status":"SUCCESS","channel":"APP","session_device_id":"D9"},
        {"transaction_id":"T003","timestamp_utc":stamp(10),"sender_id":"A200","recipient_id":"A400","amount_kes":"60000","status":"SUCCESS","channel":"APP","session_device_id":"D9"},
        {"transaction_id":"T004","timestamp_utc":stamp(11),"sender_id":"A200","recipient_id":"A500","amount_kes":"30000","status":"SUCCESS","channel":"APP","session_device_id":"D9"},
        {"transaction_id":"T005","timestamp_utc":stamp(13),"sender_id":"A400","recipient_id":"A600","amount_kes":"55000","status":"SUCCESS","channel":"USSD","session_device_id":"D4"},
        {"transaction_id":"T006","timestamp_utc":stamp(14),"sender_id":"A500","recipient_id":"A600","amount_kes":"27000","status":"SUCCESS","channel":"USSD","session_device_id":"D5"},
        {"transaction_id":"T007","timestamp_utc":stamp(15),"sender_id":"A100","recipient_id":"A200","amount_kes":"12000","status":"FAILED","channel":"APP","session_device_id":"D9"},
        {"transaction_id":"T008","timestamp_utc":stamp(22),"sender_id":"A300","recipient_id":"A400","amount_kes":"10000","status":"SUCCESS","channel":"API","session_device_id":"D3"},
        {"transaction_id":"T009","timestamp_utc":stamp(22),"sender_id":"A300","recipient_id":"A500","amount_kes":"10000","status":"SUCCESS","channel":"API","session_device_id":"D3"},
        {"transaction_id":"T010","timestamp_utc":stamp(22),"sender_id":"A300","recipient_id":"A600","amount_kes":"10000","status":"SUCCESS","channel":"API","session_device_id":"D3"},
        {"transaction_id":"T011","timestamp_utc":stamp(25),"sender_id":"A700","recipient_id":"A300","amount_kes":"80000","status":"SUCCESS","channel":"API","session_device_id":"D7"},
    ]
    DATA.mkdir(parents=True, exist_ok=True)
    write_csv(DATA/"accounts.csv", ["account_id","type","risk_note"], accounts)
    write_csv(DATA/"auth_events.csv", ["event_id","timestamp_utc","account_id","device_id","ip_address","result","event_type"], logins)
    write_csv(DATA/"transactions.csv", ["transaction_id","timestamp_utc","sender_id","recipient_id","amount_kes","status","channel","session_device_id"], transactions)
    return accounts, logins, transactions

def validate(accounts, logins, transactions):
    ids = {a["account_id"] for a in accounts}
    issues = []
    for kind, records, key in [("auth",logins,"event_id"),("transactions",transactions,"transaction_id")]:
        values = [r[key] for r in records]
        if len(values) != len(set(values)):
            issues.append(kind+": duplicate identifiers")
        for r in records:
            try:
                t = datetime.fromisoformat(r["timestamp_utc"])
                if t.tzinfo is None:
                    issues.append(kind+": naive timestamp "+r[key])
            except ValueError:
                issues.append(kind+": invalid timestamp "+r[key])
            for field in (["account_id"] if kind=="auth" else ["sender_id","recipient_id"]):
                if r[field] not in ids:
                    issues.append(kind+": unknown account "+r[key])
            if kind=="transactions":
                try:
                    if int(r["amount_kes"]) <= 0:
                        issues.append("nonpositive amount "+r[key])
                except ValueError:
                    issues.append("invalid amount "+r[key])
    return issues

def analyze(accounts, logins, transactions):
    """Deterministic hypotheses and transaction tracing; no guilt classification."""
    events = sorted(logins, key=lambda r:(r["timestamp_utc"],r["event_id"]))
    txs = sorted([t for t in transactions if t["status"]=="SUCCESS"],
                 key=lambda r:(r["timestamp_utc"],r["transaction_id"]))
    findings = []
    for account in sorted(a["account_id"] for a in accounts):
        login = [e for e in events if e["account_id"]==account and e["event_type"]=="LOGIN" and e["result"]=="SUCCESS"]
        for event in login:
            preceding = [e for e in events if e["account_id"]==account and e["device_id"]==event["device_id"]
                         and e["event_type"]=="LOGIN" and e["result"]=="FAILED"
                         and timedelta(0) <= datetime.fromisoformat(event["timestamp_utc"])-datetime.fromisoformat(e["timestamp_utc"]) <= timedelta(minutes=10)]
            outgoing = [t for t in txs if t["sender_id"]==account and t["session_device_id"]==event["device_id"]
                        and timedelta(0) <= datetime.fromisoformat(t["timestamp_utc"])-datetime.fromisoformat(event["timestamp_utc"]) <= timedelta(minutes=15)]
            if len(preceding)>=2 and outgoing:
                findings.append({"id":"F-AUTH-"+account,"hypothesis":"failed logins followed by successful access and transfers",
                    "account_id":account,"evidence_ids":[e["event_id"] for e in preceding]+[event["event_id"]]+[t["transaction_id"] for t in outgoing],
                    "interpretation":"Potential account-access anomaly; requires corroboration"})
    grouped = defaultdict(list)
    for t in txs:
        grouped[(t["sender_id"],t["recipient_id"])].append(t)
    for (sender,recipient), group in sorted(grouped.items()):
        for i,t in enumerate(group):
            t0 = datetime.fromisoformat(t["timestamp_utc"])
            window = [x for x in group[i:] if datetime.fromisoformat(x["timestamp_utc"])-t0 <= timedelta(minutes=10)]
            if len(window)>=2 and sum(int(x["amount_kes"]) for x in window)>=90000:
                findings.append({"id":"F-BURST-"+sender+"-"+recipient,"hypothesis":"high-value rapid transfers",
                    "account_id":sender,"evidence_ids":[x["transaction_id"] for x in window],
                    "interpretation":"Repeated large payments; purpose and authorization unknown"})
                break
    # Trace transfers forward through time, with depth and cycle controls.
    def trace(origin, max_hops=4):
        queue = deque([(origin, START, [], {origin})])
        paths = []
        while queue:
            account, after, path, visited = queue.popleft()
            if len(path)>=max_hops:
                continue
            for t in txs:
                when = datetime.fromisoformat(t["timestamp_utc"])
                if t["sender_id"]!=account or when<after or t["recipient_id"] in visited:
                    continue
                newpath = path+[t["transaction_id"]]
                paths.append({"destination":t["recipient_id"],"transaction_ids":newpath,"hops":len(newpath)})
                queue.append((t["recipient_id"],when,newpath,visited|{t["recipient_id"]}))
        return sorted(paths,key=lambda x:(x["hops"],x["transaction_ids"]))
    paths = trace("A100")
    # Correlation is not proof that the same money was forwarded; no balance ledger exists.
    return findings, paths, events, txs

def sql_exhibits(accounts, logins, transactions):
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE transactions (transaction_id TEXT, timestamp_utc TEXT, sender_id TEXT, recipient_id TEXT, amount_kes INTEGER, status TEXT, session_device_id TEXT)")
        conn.execute("CREATE TABLE auth_events (event_id TEXT, timestamp_utc TEXT, account_id TEXT, device_id TEXT, result TEXT, event_type TEXT)")
        conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?)",
                         [(t["transaction_id"],t["timestamp_utc"],t["sender_id"],t["recipient_id"],int(t["amount_kes"]),t["status"],t["session_device_id"]) for t in transactions])
        conn.executemany("INSERT INTO auth_events VALUES (?,?,?,?,?,?)",
                         [(e["event_id"],e["timestamp_utc"],e["account_id"],e["device_id"],e["result"],e["event_type"]) for e in logins])
        queries = (ROOT/"sql"/"case_002.sql").read_text(encoding="utf-8")
        result = []
        for query in queries.split(";"):
            query = "\n".join(line for line in query.splitlines() if not line.lstrip().startswith("--")).strip()
            if not query:
                continue
            if not query.lower().startswith("select"):
                raise ValueError("Non-read-only exhibit query")
            cursor = conn.execute(query)
            result.append({"query":query,"columns":[x[0] for x in cursor.description],"rows":cursor.fetchall()})
        return result
    finally:
        conn.close()

def run():
    accounts,logins,transactions = generate()
    issues = validate(accounts,logins,transactions)
    if issues:
        raise ValueError("Evidence validation failed: "+"; ".join(issues))
    findings,paths,events,txs = analyze(accounts,logins,transactions)
    exhibits = sql_exhibits(accounts,logins,transactions)
    OUT.mkdir(parents=True,exist_ok=True)
    manifest = {"case_id":"SIM-2026-002","classification":"SYNTHETIC TRAINING DATA",
                "source":"Deterministic code generator; not acquired from a real system",
                "files":[{"path":str(p.relative_to(ROOT)).replace("\\","/"),"sha256":sha256(p),"bytes":p.stat().st_size}
                         for p in sorted(DATA.glob("*.csv"))]}
    timeline = [{"timestamp_utc":e["timestamp_utc"],"id":e["event_id"],"type":e["event_type"],"account":e["account_id"]} for e in events]
    timeline += [{"timestamp_utc":t["timestamp_utc"],"id":t["transaction_id"],"type":"TRANSFER","account":t["sender_id"]} for t in txs]
    timeline.sort(key=lambda e:(e["timestamp_utc"],e["id"]))
    for name,obj in [("manifest.json",manifest),("findings.json",findings),("paths.json",paths),
                     ("timeline.json",timeline),("sql_exhibits.json",exhibits)]:
        (OUT/name).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
    write_csv(OUT/"timeline.csv",["timestamp_utc","id","type","account"],timeline)
    summary = {"case_id":"SIM-2026-002","accounts":len(accounts),"authentication_events":len(logins),
               "transactions":len(transactions),"successful_transactions":len(txs),
               "findings":len(findings),"trace_paths":len(paths),"validation_issues":issues}
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return summary

if __name__=="__main__":
    run()
