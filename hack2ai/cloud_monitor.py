"""
Cloud Resource Monitor - Research Project
Author: Pankaj Kumar
Team: mr-robot
Challenge: National Research & Innovation Challenge Season 3 by 3SVK
"""

import json
import random
import datetime
from typing import Dict, List

def generate_ec2_instances() -> List[Dict]:
    instance_types = ["t2.micro", "t2.small", "t3.medium", "m5.large", "c5.xlarge"]
    regions = ["us-east-1", "us-west-2", "ap-south-1", "eu-west-1"]
    states = ["running", "running", "running", "stopped", "idle"]
    instances = []
    for i in range(1, 8):
        cpu = random.randint(2, 95)
        instances.append({
            "instance_id": f"i-0{random.randint(1000000,9999999)}abcd",
            "type": random.choice(instance_types),
            "region": random.choice(regions),
            "state": random.choice(states),
            "cpu_utilization": cpu,
            "monthly_cost_usd": round(random.uniform(8.5, 180.0), 2),
            "is_underutilized": cpu < 20
        })
    return instances

def generate_s3_buckets() -> List[Dict]:
    names = ["project-data","backup-storage","logs-archive","ml-datasets","static-assets","research-outputs"]
    return [{"bucket_name": n, "size_gb": round(random.uniform(0.5,500.0),2),
             "object_count": random.randint(10,50000),
             "monthly_cost_usd": round(random.uniform(0.02,12.0),2),
             "public_access": random.choice([True,False,False,False])} for n in names]

def analyze_cost(instances, buckets):
    ec2 = sum(i["monthly_cost_usd"] for i in instances)
    s3 = sum(b["monthly_cost_usd"] for b in buckets)
    total = ec2 + s3
    waste = sum(i["monthly_cost_usd"] for i in instances
                if i["is_underutilized"] or i["state"] in ["stopped","idle"])
    return {"ec2_monthly_cost": round(ec2,2), "s3_monthly_cost": round(s3,2),
            "total_monthly_cost": round(total,2), "estimated_waste_usd": round(waste,2),
            "savings_potential_percent": round((waste/total)*100,1) if total > 0 else 0}

def security_audit(buckets):
    alerts = [f"⚠️ ALERT: Bucket '{b['bucket_name']}' is PUBLIC!" for b in buckets if b["public_access"]]
    return alerts if alerts else ["✅ No public buckets. Good security posture!"]

def recommendations(instances):
    recs = []
    for i in instances:
        if i["state"] == "stopped":
            recs.append(f"💡 {i['instance_id']} STOPPED — terminate to save ${i['monthly_cost_usd']}/mo")
        elif i["is_underutilized"]:
            recs.append(f"📉 {i['instance_id']} CPU at {i['cpu_utilization']}% — downsize {i['type']}")
        elif i["state"] == "idle":
            recs.append(f"⏸️ {i['instance_id']} IDLE — schedule auto-shutdown")
    return recs if recs else ["✅ All instances optimally utilized."]

if __name__ == "__main__":
    print("🔄 Scanning cloud resources...\n")
    instances = generate_ec2_instances()
    buckets = generate_s3_buckets()
    cost = analyze_cost(instances, buckets)
    print(f"💰 Total Cost: ${cost['total_monthly_cost']}/month")
    print(f"🗑️  Waste: ${cost['estimated_waste_usd']}/month ({cost['savings_potential_percent']}% savings possible)")
    print("\n🔒 Security:")
    for a in security_audit(buckets): print(f"  {a}")
    print("\n💡 Recommendations:")
    for r in recommendations(instances): print(f"  {r}")
    print("\n✅ Scan complete!")
