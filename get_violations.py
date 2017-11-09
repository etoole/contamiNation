import csv, json

wsid_list = []
all_detail_dict = []

with open ('all_national_violations_2017Q3.csv') as all_violations:
    all_violations = csv.DictReader(all_violations)

    for violation in all_violations:
        if violation['Compliance Status'] != 'Returned to Compliance':
            wsid_list.append(violation['PWS ID'])
wsid_set = set(wsid_list)

with open('all_national_violations_detail_2017Q3.csv', encoding="latin-1") as all_violations_detail:
    all_violations_detail  = csv.DictReader(all_violations_detail)

    for violation_detail in all_violations_detail:
        if violation_detail['PWS ID'] in wsid_set:
            pws_id = violation_detail['PWS ID']
            pws_name = violation_detail['PWS Name']
            population_count = violation_detail['Population Served Count']
            city = violation_detail['City Name']
            state_region = violation_detail['Primacy Agency']
            zip_code = violation_detail['Zip Code']
            owner_type = violation_detail['Owner Type']
            contact_name = violation_detail['Admin Name']
            contact_email = violation_detail['Email Address']
            contact_phone = violation_detail['Phone Number']

            detail_dict = ({
            'PWS ID' : pws_id,
            'PWS Name' : pws_name,
            'Population Count' : population_count,
            'City' : city,
            'State/EPA Region' : state_region,
            'Zip Code' : zip_code,
            'Owner Type' : owner_type,
            'Contact Name' : contact_name,
            'Contact Email' : contact_email,
            'Contact Phone' : contact_phone
            })

            all_detail_dict.append(detail_dict)

print(all_detail_dict)
print(len(all_detail_dict))
json.dump(all_detail_dict, open('detail_violations.json','w'), indent=4)
