import http.client
import json

# https://api.fda.gov/drug/event.json?search=salycilic

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/event.json?search=salycilic", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repo = json.loads(repos_raw)

repo = repo['results']

for element in repo:
    print('These are the manufacturers that produce aspirin:', repo[0]['patient']['drug'][1]['openfda']['manufacturer_name'])