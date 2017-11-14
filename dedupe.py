import json

detail_id = []
detail_dictionary = []

with open('detail_violations2.json') as dv2:
    detail_violations2 = json.load(dv2)

    for violation in detail_violations2:
        if violation['PWS ID'] not in detail_id:
            detail_dictionary.append(violation)
        detail_id.append(violation['PWS ID'])

print(detail_dictionary)
json.dump(detail_dictionary, open('test_dedupe.json', 'w'), indent=4)
