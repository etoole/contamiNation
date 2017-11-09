import requests, json


payload = {'PWSID' : 'CA3500550'}
r = requests.get('https://ofmpub.epa.gov/apex/sfdw/f?p=108:50:::NO:RP,RIR::', params=payload)
print(r.status_code)

# with open('detail_violations.json') as detail_violations:
#     violations = json.load(detail_violations)
#     print(violations)
