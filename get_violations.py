import csv, json, os

#CREATE EMPTY LISTS

non_comp_wsid_list = []
comp_wsid_list = []
non_comp_detail_dict = []
comp_detail_dict = []
rtc_date_list = []

# DEFINE FUNCTIONS

def non_compliant_list(violation_data):
    for x in violation_data:
        rtc_date_dict = ({'PWS ID' : x['PWS ID'], 'RTC Date' : x['RTC Date']})
        rtc_date_list.append(rtc_date_dict)
        if x['Compliance Status'] != 'Returned to Compliance':
            non_comp_wsid_list.append(x['PWS ID'])
        elif x['Compliance Status'] == 'Returned to Compliance':
            comp_wsid_list.append(x['PWS ID'])

def get_non_comp_detail(detail_data, non_comp_id, comp_id):
    for violation_detail in detail_data:
        for rtc_date in rtc_date_list:
            if violation_detail['PWS ID'] == rtc_date['PWS ID']:
                compliance_date = rtc_date['RTC Date']
                if violation_detail['PWS ID'] in non_comp_id:
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
                    'Compliance Status' : 'Not Compliant',
                    'Population Count' : population_count,
                    'City' : city,
                    'State/EPA Region' : state_region,
                    'Zip Code' : zip_code,
                    'Owner Type' : owner_type,
                    'Contact Name' : contact_name,
                    'Contact Email' : contact_email,
                    'Contact Phone' : contact_phone
                    })

                    non_comp_detail_dict.append(detail_dict)

                elif violation_detail['PWS ID'] in comp_id:
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
                    'Compliance Status' : 'Returned to Compliance on {0}'.format(compliance_date),
                    'Population Count' : population_count,
                    'City' : city,
                    'State/EPA Region' : state_region,
                    'Zip Code' : zip_code,
                    'Owner Type' : owner_type,
                    'Contact Name' : contact_name,
                    'Contact Email' : contact_email,
                    'Contact Phone' : contact_phone
                    })

                    comp_detail_dict.append(detail_dict)


#CREATE SET OF PWSID'S FOR NON-COMPLIANT & COMPLIANT PWS

with open (os.path.join('pws_data','all_national_violations_2017Q3.csv')) as all_violations:
    all_violations = csv.DictReader(all_violations)
    non_compliant_list(all_violations)


non_comp_wsid_set = set(non_comp_wsid_list)
comp_wsid_set = set(comp_wsid_list)

#CREATE DICTIONARY WITH DETAILS FOR NON-COMPLIANT & COMPLIANT PWS

with open(os.path.join('pws_data','all_national_violations_detail_2017Q3.csv', encoding="latin-1")) as all_violations_detail:
    all_violations_detail  = csv.DictReader(all_violations_detail)
    get_non_comp_detail(all_violations_detail, non_comp_wsid_set, comp_wsid_set)


print("\nThere are {0} unique, non-compliant id's.\n".format(len(non_comp_wsid_set)))

detail_dict_list_nc = []
for dictionary in non_comp_detail_dict:
    detail_dict_list_nc.append(dictionary['PWS ID'])
detail_dict_set_nc = set(detail_dict_list_nc)
missing_ids_nc = non_comp_wsid_set - detail_dict_set_nc
print("Complete information was not found for the following {0} non-compliant id's:\n".format(len(missing_ids_nc)))
for id_number in missing_ids_nc:
    print(id_number)


print("\n\nThere are {0} unique, compliant id's.\n".format(len(comp_wsid_set)))

detail_dict_list_c = []
for dictionary in comp_detail_dict:
    detail_dict_list_c.append(dictionary['PWS ID'])
detail_dict_set_c = set(detail_dict_list_c)
missing_ids_c = comp_wsid_set - detail_dict_set_c
print("Complete information was not found for the following {0} compliant id's:\n".format(len(missing_ids_c)))
for id_number in missing_ids_c:
    print(id_number)

json.dump(non_comp_detail_dict, open('detail_violations2.json','w'), indent=4)
json.dump(comp_detail_dict, open('detail_violations2.json','a'), indent=4)
