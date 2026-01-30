import sys
import csv
import requests

# ONOS REST API Configuration
HOST = "localhost"
PORT = "8181"
USER = "karaf"
PASS = "karaf"
URL  = f"http://{HOST}:{PORT}/onos/v1/acl/rules"
HEADERS = {'Content-type': 'application/json'}

# 1. Load security policies from CSV
policy_file = "firewall-policies.csv"
firewall_rules = []

with open(policy_file, 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    next(rows) # Skip header row
    for row in rows:
        # Append (Source MAC, Destination MAC)
        firewall_rules.append((row[1], row[2]))

# 2. Push rules to ONOS via REST API
for src_mac, dst_mac in firewall_rules:
    payload = {
        "srcIp": "10.0.0.0/24",
        "srcMac": src_mac,
        "dstMac": dst_mac
    }
    
    response = requests.post(
        URL, 
        json=payload, 
        auth=(USER, PASS), 
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code} - Applied rule for {src_mac} -> {dst_mac}")
