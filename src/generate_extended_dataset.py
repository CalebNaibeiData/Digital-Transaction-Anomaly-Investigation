"""Reproducible mixed-behavior synthetic payment dataset; not a real-world benchmark."""
from __future__ import annotations
import csv
import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"extended"
START=datetime(2026,10,12,0,0,tzinfo=timezone.utc)
FIELDS=["transaction_id","timestamp_utc","sender_id","recipient_id","amount_kes","status","channel","session_device_id","scenario_tag"]

def generate(seed=20261012, normal_count=2400):
    if normal_count<100:
        raise ValueError("normal_count must be at least 100")
    rng=random.Random(seed)
    accounts=[f"AC{i:04d}" for i in range(1,181)]
    merchants=[f"MC{i:03d}" for i in range(1,21)]
    rows=[]
    for i in range(normal_count):
        sender=rng.choice(accounts+merchants)
        recipient=rng.choice(merchants if rng.random()<0.58 else accounts)
        if recipient==sender:
            recipient=merchants[0] if sender!=merchants[0] else accounts[0]
        ts=START+timedelta(seconds=rng.randrange(0,86400*7))
        amount=round(rng.lognormvariate(7.4,0.9))
        rows.append({"transaction_id":f"N{i+1:06d}","timestamp_utc":ts.isoformat(),
            "sender_id":sender,"recipient_id":recipient,"amount_kes":str(max(50,min(amount,150000))),
            "status":"FAILED" if rng.random()<0.025 else "SUCCESS",
            "channel":rng.choice(["APP","USSD","API","AGENT"]),
            "session_device_id":f"DEV{rng.randrange(1,251):03d}","scenario_tag":"background"})
    def add(txid,minute,sender,recipient,amount,device,tag,status="SUCCESS"):
        rows.append({"transaction_id":txid,"timestamp_utc":(START+timedelta(days=2,minutes=minute)).isoformat(),
          "sender_id":sender,"recipient_id":recipient,"amount_kes":str(amount),"status":status,
          "channel":"APP","session_device_id":device,"scenario_tag":tag})
    # Scenario labels describe planted behavior, not actual confirmed fraud.
    for i in range(12):
        add(f"S{i+1:03d}",500+i,"AC0001","AC0170",49000-i*150,"DEV900","rapid_sender")
    for i,(s,r,a) in enumerate([("AC0170","AC0171",160000),("AC0170","AC0172",145000),
        ("AC0171","AC0173",125000),("AC0172","AC0173",110000)],13):
        add(f"S{i:03d}",520+i,""+s,r,a,"DEV901","onward_path")
    for i in range(16):
        add(f"P{i+1:03d}",800+i,"MC001",f"AC{i+30:04d}",12500,"DEV300","scheduled_payroll")
    for i in range(8):
        add(f"C{i+1:03d}",1000+i,f"AC{i+60:04d}","AC0160",8000+i*250,"DEV400","recipient_concentration")
    rows.sort(key=lambda r:(r["timestamp_utc"],r["transaction_id"]))
    OUT.mkdir(parents=True,exist_ok=True)
    file=OUT/"transactions.csv"
    with file.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
        writer.writeheader();writer.writerows(rows)
    digest=hashlib.sha256(file.read_bytes()).hexdigest()
    manifest={"description":"Synthetic seven-day mixed-behavior payments dataset",
      "seed":seed,"background_count":normal_count,"planted_scenarios":{
       "rapid_sender":12,"onward_path":4,"scheduled_payroll":16,"recipient_concentration":8},
      "total_records":len(rows),"sha256":digest,
      "important":"scenario_tag is synthetic generator metadata, not an investigator-accessible fraud label"}
    (OUT/"generation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return manifest

if __name__=="__main__":
    print(json.dumps(generate(),indent=2))
