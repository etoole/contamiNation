import requests, json
#
#
# payload = {'PWS_ID' : 'MI4120932'}
# r = requests.get('https://ofmpub.epa.gov/apex/sfdw/f?p=108:35:::NO::P35_REPORT2:LCR', params=payload)
# print(r.text)

with open('detail_violations.json') as detail_violations:
    violations = json.load(detail_violations)
    print(violations)
