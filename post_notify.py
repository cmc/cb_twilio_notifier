import json
import requests
import sys

payload = {
    "sid": sys.argv[1],
    "hostname": sys.argv[2],
    "requestor": "cmc",
    "cell": "+16505186084", 
    "method": "add"
}
r = requests.post('http://54.218.185.95:12287/monitor', json=payload, verify=False)
if r.status_code == 200:
    print("great success!")
    print(r.text)
else:
    print("there appears to have been a problem.")
    print(r.text)
