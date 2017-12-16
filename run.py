import csv, json, os, re, operator, time, datetime, requests

## create empty lists/vars
non_comp_wsid_list = []
comp_wsid_list = []
non_comp_detail_dict = []
comp_detail_dict = []
rtc_date_list = []
detail_id = []
detail_dictionary = []
detail_dictionary_deduped = []
result_key_list = []
concentration_list = []
detail_dict_list_nc = []
detail_dict_list_c = []
geojson_list = []
geocode_list = []
all_pbcu = []
failure_counter = 0
success_counter = 0

## compile regex
first_name = re.compile("(?<=, )\w+")
last_name = re.compile("\w+(?=,)")
zip_pattern = re.compile('[0-9]{5}(?!.)')
day = re.compile('(?<=on\s)\w+')
month = re.compile('(?<=\d-)[A-Z]{3}')
year = re.compile('[0-9]{4}')
concentration_digit = re.compile('[0-9]+')

## create constants
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
API_KEY = ## enter your api key here
MONTH_TABLE = {
'JAN': '01',
'FEB': '02',
'MAR': '03',
'APR': '04',
'MAY': '05',
'JUN': '06',
'JUL': '07',
'AUG': '08',
'SEP': '09',
'OCT': '10',
'NOV': '11',
'DEC': '12'
}

## define functions
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
                    contact_name = violation_detail['Admin Name']
                    contact_email = violation_detail['Email Address']
                    contact_phone = violation_detail['Phone Number']

                    first_name_result = first_name.search(contact_name)
                    if first_name_result != None:
                        first_name_result = first_name_result[0].title()
                    else:
                        first_name_result = " "

                    last_name_result = last_name.search(contact_name)
                    if last_name_result != None:
                        last_name_result = last_name_result[0].title()
                    else:
                        last_name_result = " "

                    contact_name = "{0} {1}".format(first_name_result, last_name_result)

                    detail_dict = ({
                    'pwsid' : pws_id,
                    'name' : pws_name,
                    'compliancestatus' : 'Not Compliant',
                    'populationserved' : population_count,
                    'city' : city,
                    'state/region' : state_region,
                    'zipcode' : zip_code,
                    'contactname' : contact_name,
                    'contactemail' : contact_email,
                    'contactphone' : contact_phone
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
                    'pwsid' : pws_id,
                    'name' : pws_name,
                    'compliancestatus' : 'Returned to Compliance on {0}'.format(compliance_date),
                    'populationserved' : population_count,
                    'city' : city,
                    'state/region' : state_region,
                    'zipcode' : zip_code,
                    'Owner Type' : owner_type,
                    'contactname' : contact_name,
                    'contactemail' : contact_email,
                    'contactphone' : contact_phone
                    })

                    comp_detail_dict.append(detail_dict)


def csv_to_dict(x):
    for dictionary in x:
        pws_id = dictionary['PWS ID']
        result = dictionary['Sample Measure (mg/L)']
        contaminant = dictionary['Contaminant Name']
        end_date = dictionary['Sampling End Date']
        service_connections = dictionary['Service Connections Count']

        result = float(result) * 1000
        result = int(result)
        result = str(result) + ' ppb'

        contaminant = contaminant.split(' ', 1)[0]

        pbcu = {
        'pwsid' : pws_id,
        'result' : result,
        'contaminant' : contaminant,
        'enddate' : end_date
        }
        all_pbcu.append(pbcu)



## split pws's into compliant and not compliant lists
with open (os.path.join('pws_data','all_national_violations_2017Q3_medium.csv')) as all_violations:
    all_violations = csv.DictReader(all_violations)
    non_compliant_list(all_violations)

non_comp_wsid_set = set(non_comp_wsid_list)
comp_wsid_set = set(comp_wsid_list)


## create list of dictionaries from pws data
with open(os.path.join('pws_data','all_national_violations_detail_2017Q3.csv'), encoding="latin-1") as all_violations_detail:
    all_violations_detail  = csv.DictReader(all_violations_detail)
    get_non_comp_detail(all_violations_detail, non_comp_wsid_set, comp_wsid_set)

## print preliminary compliant/non-compliant breakdown and report on pws's lacking details
print("\nThere are {0} unique, non-compliant id's.\n".format(len(non_comp_wsid_set)))

for dictionary in non_comp_detail_dict:
    detail_dict_list_nc.append(dictionary['pwsid'])
    detail_dictionary.append(dictionary)
detail_dict_set_nc = set(detail_dict_list_nc)
missing_ids_nc = non_comp_wsid_set - detail_dict_set_nc

## print id numbers of pws's missing details
print("Complete information was not found for the following {0} non-compliant id's:\n".format(len(missing_ids_nc)))
# for id_number in missing_ids_nc:
#     print(id_number)

print("\n\nThere are {0} unique, compliant id's.\n".format(len(comp_wsid_set)))

for dictionary in comp_detail_dict:
    detail_dict_list_c.append(dictionary['pwsid'])
    detail_dictionary.append(dictionary)
detail_dict_set_c = set(detail_dict_list_c)
missing_ids_c = comp_wsid_set - detail_dict_set_c

## print it numbers of pws's missing details
print("Complete information was not found for the following {0} compliant id's:\n".format(len(missing_ids_c)))
# for id_number in missing_ids_c:
#     print(id_number)

## record number of records before deduping
before_dedupe = len(detail_dictionary)

## dedupe list of dictionaries with pws data
for violation in detail_dictionary:
    if violation['pwsid'] not in detail_id:
        detail_dictionary_deduped.append(violation)
    detail_id.append(violation['pwsid'])

## calculate number of duplicate records removed and print
after_dedupe = len(detail_dictionary)
details_removed = before_dedupe - after_dedupe
print("\n{0} duplicate records were removed.\n".format(details_removed))

## make list of dictionaries from chemical analysis data
with open(os.path.join('chemical_analysis_data','copper_samples_2015_to_present_2017Q1.csv'), encoding='latin-1') as copper1:
    copper_q1 = csv.DictReader(copper1)
    csv_to_dict(copper_q1)

with open(os.path.join('chemical_analysis_data','copper_samples_2015_to_present_2017Q2.csv'), encoding='latin-1') as copper2:
    copper_q2 = csv.DictReader(copper2)
    csv_to_dict(copper_q2)

with open(os.path.join('chemical_analysis_data','copper_samples_2015_to_present_2017Q3.csv'), encoding='latin-1') as copper3:
    copper_q3 = csv.DictReader(copper3)
    csv_to_dict(copper_q3)

with open(os.path.join('chemical_analysis_data','lead_samples_2015_2017Q3.csv'), encoding='latin-1') as lead1:
    lead1 = csv.DictReader(lead1)
    csv_to_dict(lead1)

with open(os.path.join('chemical_analysis_data','lead_samples_2015_to_present_2017Q1.csv'), encoding='latin-1') as lead2:
    lead2 = csv.DictReader(lead2)
    csv_to_dict(lead2)

with open(os.path.join('chemical_analysis_data','lead_samples_2015_to_present_2017Q2.csv'), encoding='latin-1') as lead3:
    lead3 = csv.DictReader(lead3)
    csv_to_dict(lead3)

with open(os.path.join('chemical_analysis_data','lead_samples_2016_2017Q3.csv'), encoding='latin-1') as lead4:
    lead4 = csv.DictReader(lead4)
    csv_to_dict(lead4)

with open(os.path.join('chemical_analysis_data','lead_samples_2017_2017Q3.csv'), encoding='latin-1') as lead5:
    lead5 = csv.DictReader(lead5)
    csv_to_dict(lead5)

## sort pws data list and chemical analysis data list to make merge go faster
detail_dictionary_deduped.sort(key=operator.itemgetter('pwsid'))
all_pbcu.sort(key=operator.itemgetter('pwsid'))

## reformat end date as unix timestamp
for result in all_pbcu:
    end_date = result['enddate']
    dt = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    ts = time.mktime(dt.timetuple())
    result.update({'enddate': ts})

## join pws data and chemical analysis data by pwsid.
for result in detail_dictionary_deduped:
    detail_id = result['pwsid']
    result_dict_list = []
    for chem_result in all_pbcu:
        if chem_result['pwsid'] == detail_id:

## reformat and append each chemical analysis dictionary to a list
            result_dict = {
            'contaminant': chem_result['contaminant'],
            'concentration': chem_result['result'],
            'enddate': chem_result['enddate']
            }
            result_dict_list.append(result_dict)

## remove chemical analysis duplicates from each list, sort list chronologically & attach to pws dictionary for matching public water system
    result_dict_list = [dict(t) for t in set([tuple(d.items()) for d in result_dict_list])]
    result_dict_list.sort(key=operator.itemgetter('enddate'), reverse=True)
    result['results'] = result_dict_list

## create and empty list each time loop goes through
    end_date = []
    result['markercolor'] = 'green-drinking-water-15.svg'
    concentration_list = []
    result_key_list = []
    lead_concentration_list = []
    copper_concentration_list = []

## begin markercolor evaluation

## for those pws's that have returned to compliance in the past but had contaminated water
## more recently, compare the date of chemical analysis results with the return to compliance date
    if 'Returned' in result['compliancestatus']:
        status = result['compliancestatus']

## separate return to compliance date with regex
        result_day = day.findall(status)
        result_month = month.findall(status)
        result_year = year.findall(status)

        result_day = result_day[0]
        result_month = result_month[0]
        result_year = result_year[0]

## match abbreviated name of month (key) to ordinal (value)
        for month_abrv in MONTH_TABLE:
            if str(month_abrv) == result_month:
                result_month = MONTH_TABLE[result_month]

## reformat return to compliance as date and create separate unix time stamp for comparison
        date_format = '{0}/{1}/{2}'.format(result_month, result_day, result_year)
        dt = datetime.datetime.strptime(date_format, '%m/%d/%Y')
        rtc = time.mktime(dt.timetuple())

## compare each chem analysis result for a given pws site with that site's return to compliance date
        results_key = result['results']
        if results_key != None:
            for results_data in results_key:
                end_date = results_data['enddate']

## create list of concentrations occuring after return to compliance date
                if end_date > rtc:
                    concentration = results_data['concentration']
                    concentration = concentration_digit.findall(concentration)
                    concentration = int(concentration[0])
                    concentration_list.append(concentration)

## sort concentration list from lowest to highest contamination value
                concentration_list = sorted(concentration_list)

## check if any detections were found after return to compliance date
                if len(concentration_list) > 0:

## change compliance status if highest value in post-return to compliance result is a non-zero detection
                    if concentration_list[-1] > 0:
                        result['compliancestatus'] = 'Not Compliant'

## continue for pws where detection was found after return to compliance
                if result['compliancestatus'] == 'Not Compliant':
                    contaminant = results_data['contaminant']

## create separate lists for positive detections of lead and copper occuring after return to compliance date
                    if contaminant == 'LEAD':
                        lead_concentration = results_data['concentration']
                        lead_concentration = concentration_digit.findall(lead_concentration)
                        lead_concentration = int(lead_concentration[0])
                        lead_concentration_list.append(lead_concentration)

                    lead_concentration_list = sorted(lead_concentration_list)

                    if contaminant == 'COPPER':
                        copper_concentration = results_data['concentration']
                        copper_concentration = concentration_digit.findall(copper_concentration)
                        copper_concentration = int(copper_concentration[0])
                        copper_concentration_list.append(copper_concentration)

                    copper_concentration_list = sorted(copper_concentration_list)

## evalute post-rtc detections of lead and copper by relevant EPA 'action level' Lead: 15ppb; Copper: 1300ppb
                    if len(lead_concentration_list) > 0:
                        if lead_concentration_list[-1] == 0:
                            if len(copper_concentration_list) > 0:
                                if copper_concentration_list[-1] == 0:
                                    result['markercolor'] = 'green-drinking-water-15.svg'
                                elif 0 > copper_concentration_list[-1] > 1300:
                                    result['markercolor'] = 'yellow-drinking-water-15.svg'
                                elif copper_concentration_list[-1] > 1300:
                                        result['markercolor'] = 'red-drinking-water-15.svg'

                        elif 0 < lead_concentration_list[-1] < 15:
                            result['markercolor'] = 'yellow-drinking-water-15.svg'
                            if len(copper_concentration_list) > 0:
                                if copper_concentration_list[-1] > 1300:
                                    result['markercolor'] = 'red-drinking-water-15.svg'

                        elif lead_concentration_list[-1] > 15:
                            result['markercolor'] = 'red-drinking-water-15.svg'

                    if len(copper_concentration_list) > 0:
                        if copper_concentration_list[-1] == 0:
                            if len(lead_concentration_list) > 0:
                                if lead_concentration_list[-1] == 0:
                                    result['markercolor'] = 'green-drinking-water-15.svg'
                                elif 0 > lead_concentration_list[-1] > 15:
                                    result['markercolor'] = 'yellow-drinking-water-15.svg'
                                elif lead_concentration_list[-1] > 15:
                                        result['markercolor'] = 'red-drinking-water-15.svg'

                        elif 0 < copper_concentration_list[-1] < 1300:
                            result['markercolor'] = 'yellow-drinking-water-15.svg'
                            if len(lead_concentration_list) > 0:
                                if lead_concentration_list[-1] > 15:
                                    result['markercolor'] = 'red-drinking-water-15.svg'

                        elif copper_concentration_list[-1] > 1300:
                            result['markercolor'] = 'red-drinking-water-15.svg'

## evaluate markercolor for pws's that are originally labeled by EPA as'Not Compliant'
    elif 'Not' in result['compliancestatus']:

## give base-level yellow marker color to not compliant pws's
        result['markercolor'] = 'yellow-drinking-water-15.svg'

## reformat unix timestamp as datetime
        results_key = result['results']
        if results_key != None:
            for results_data in results_key:

## identify contaminant
                contaminant = results_data['contaminant']

## create separate lists for lead & copper concentrations
                if contaminant == 'LEAD':
                    lead_concentration = results_data['concentration']
                    lead_concentration = concentration_digit.findall(lead_concentration)
                    lead_concentration = int(lead_concentration[0])
                    lead_concentration_list.append(lead_concentration)

                lead_concentration_list = sorted(lead_concentration_list)

                if contaminant == 'COPPER':
                    copper_concentration = results_data['concentration']
                    copper_concentration = concentration_digit.findall(copper_concentration)
                    copper_concentration = int(copper_concentration[0])
                    copper_concentration_list.append(copper_concentration)

                copper_concentration_list = sorted(copper_concentration_list)

## determine if marker color should be changed from yellow to red
                if len(lead_concentration_list) > 0:
                    if lead_concentration_list[-1] > 15:
                        result['markercolor'] = 'red-drinking-water-15.svg'

                if len(copper_concentration_list) > 0:
                    if copper_concentration_list[-1] > 1300:
                        result['markercolor'] = 'red-drinking-water-15.svg'

## reformat enddate from unix timestamp to datetime for pws with original compliance status of "Returned to compliance on...."
    for result_data in results_key:
        end_date = result_data['enddate']
        end_date = datetime.date.fromtimestamp(end_date)
        result_data['enddate'] = end_date.strftime("%m/%d/%y")

## reformat date in "Returned to compliance on ..."
    if 'Returned' in result['compliancestatus']:
        rtc = datetime.date.fromtimestamp(rtc)
        result['compliancestatus'] = 'Returned to Compliance on {0}'.format(rtc.strftime("%m/%d/%y"))

## begin geocoding
## disregard pws's for which no zipcode is present as these are too difficult to locate with certainty and
## zip code is required for geocoding quality control
    if result['zipcode'] != '-':
        if results_key != None:

## format geocoding payload for googlemaps
            params = {'address': result['name'],
            'components' : {
                'locality':result['city'],
                'administrative_area':result['state/region'],
                'postal_code':result['zipcode'],
                'country':'us'
                },
            'key': API_KEY
            }

## make googlemaps API request
            req = requests.get(GOOGLE_MAPS_API_URL, params=params)
            res = req.json()

## check if results went through
            if res['status'] !='ZERO_RESULTS':
                if len(res['results']) > 0:

## identify address components as variable
                    address_components = res['results'][0]['address_components']

                    for components in address_components:

## check to make sure result in this position is zip code
                        if components['types'][0] == 'postal_code':
## identify zip code and match from googlemaps response
                            m = re.match(zip_pattern, components['long_name'])
                            if m:
                                google_maps_zip_code = m.group()

## extract first three digits of google maps zip code
                                google_maps_zip_short = re.match('[0-9]{3}', google_maps_zip_code)

## obtain coordinates for googlemaps match
                                latitude = res['results'][0]['geometry']['location']['lat']
                                longitude = res['results'][0]['geometry']['location']['lng']
                                coordinates = [longitude, latitude]

## extract first three digits of EPA-supplied zip code
                                epa_zip_short = re.match('[0-9]{3}', result['zipcode'])
                                if epa_zip_short != None:
                                    if google_maps_zip_short != None:

## check to see if first three digits of EPA zip code and googlemaps zip code are a match and display on screen
                                        print(epa_zip_short.group())
                                        print(google_maps_zip_short.group())
                                        if epa_zip_short.group() == google_maps_zip_short.group():

## write geojson for marker assuming googlemaps match is good and using googlemaps coordinates
                                            geojson = {
                                                  "type": "Feature",
                                                  "geometry": {
                                                    "type": "Point",
                                                    "coordinates": coordinates
                                                  },
                                                  "properties": {
                                                    "pwsid": result['pwsid'],
                                                    "name": result['name'],
                                                    "address": res['results'][0]['formatted_address'],
                                                    "compliancestatus": result['compliancestatus'],
                                                    "populationserved": result['populationserved'],
                                                    "contactname": result['contactname'],
                                                    "contactphone": result['contactphone'],
                                                    "contactemail": result['contactemail'],
                                                    "results": result['results'],
                                                    "icon": {
                                                        "iconUrl": result['markercolor'],
                                                        "iconSize": [25, 25]
                                                            }
                                                        }
                                                    }
                                            geojson_list.append(geojson)
                                            print(geojson)
                                            success_counter += 1
## if zip codes do not match...
                                        else:
## create new payload for googlemaps request with EPA zipcode and get its coordinates
                                            zipcode_marker = {'address' : result['zipcode'],
                                            'key': API_KEY
                                            }

                                            zip_req = requests.get(GOOGLE_MAPS_API_URL, params=zipcode_marker)
                                            zip_res = zip_req.json()

## check to see if a result was returned
                                            if zip_res['status'] != 'ZERO_RESULTS':
                                                if len(zip_res['results']) > 0:

## compile coordinates for EPA zipcode
                                                    zip_latitude = zip_res['results'][0]['geometry']['location']['lat']
                                                    zip_longitude = zip_res['results'][0]['geometry']['location']['lng']
                                                    zip_coordinates = [zip_longitude, zip_latitude]

## create geojson object using coordinates for EPA zipcode and address supplied from googlemaps for EPA zipcode
                                                    geojson = {
                                                          "type": "Feature",
                                                          "geometry": {
                                                            "type": "Point",
                                                            "coordinates": zip_coordinates
                                                          },
                                                          "properties": {
                                                            "pwsid": result['pwsid'],
                                                            "name": result['name'],
                                                            "address": zip_res['results'][0]['formatted_address'],
                                                            "compliancestatus": result['compliancestatus'],
                                                            "populationserved": result['populationserved'],
                                                            "contactname": result['contactname'],
                                                            "contactphone": result['contactphone'],
                                                            "contactemail": result['contactemail'],
                                                            "results": result['results'],
                                                            "icon": {
                                                                "iconUrl": result['markercolor'],
                                                                "iconSize": [25, 25]
                                                                    }
                                                                }
                                                            }
                                                    print(geojson)
                                                    failure_counter += 1
## append geojson object to list
                                                    geojson_list.append(geojson)

## calculate how many markers were geocoded of the original set
total_detail_matches = len(non_comp_wsid_list) + len(comp_wsid_list)
print('\n\nOf the original {0} public water systems, {1} were successfully geocoded.\n\n{2} of the public water systems were correctly located by GoogleMaps.\n\n{3} of the public water systems were not located and instead were given the coordinates of their zipcode.\n'.format(total_detail_matches, len(geojson_list), success_counter, failure_counter))

## dump markers in a json file
json.dump(geojson_list, open('markers.json','w'))
