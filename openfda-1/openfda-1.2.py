import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repo = json.loads(repos_raw)

repo = repo['results']

for i in range(0,10):
    print("ID of the drug", i+1, "is", repo[i]['id'])