# PWS NAME - CITY, STATE - COMPLIANCE STATUS
# CONTACT FIRST, CONTACT LAST - CONTACT PHONE - CONTACT EMAIL
# ANALYTE | CONCENTRATION | SAMPLING END DATE
# LEAD    | 24 PPB        | 06/30/2016

import json, re, os

result_dict = {}
result_dict_list = {}
state_init = re.compile('\w{2}')

# initial_dict = {
# 'AK': 'Alaska',
# 'AR': 'Arkansas',
# 'AL': 'Alabama',
# 'AZ': 'Arizona',
# 'CA': 'California',
# 'CO': 'Colorado',
# 'CT': 'Connecticut',
# 'DE': 'Delaware',
# 'FL': 'Florida',
# 'GA': 'Georgia',
# 'HI': 'Hawaii',
# 'ID': 'Idaho',
# 'IL': 'Illinois',
# 'IN': 'Indiana',
# 'IA': 'Iowa',
# 'KS': 'Kansas',
# 'KY': 'Kentucky',
# 'LA': 'Louisiana',
# 'ME': 'Maine',
# 'MS': 'Mississippi',
# 'MD': 'Maryland',
# 'MA': 'Massachusetts',
# 'MI': 'Michigan',
# 'MO': 'Missouri',
# 'MN': 'Minnesota',
# 'MT': 'Montana',
# 'ND': 'North Dakota',
# 'NE': 'Nebraska',
# 'NV': 'Nevada',
# 'NH': 'New Hampshire',
# 'NJ': 'New Jersey',
# 'NM': 'New Mexico',
# 'NY': 'New York',
# 'NC': 'North Carolina',
# 'OH': 'Ohio',
# 'OK': 'Oklahoma',
# 'OR': 'Oregon',
# 'PA': 'Pennsylvania',
# 'RI': 'Rhode Island',
# 'SC': 'South Carolina',
# 'SD': 'South Dakota',
# 'TN': 'Tennessee',
# 'TX': 'Texas',
# 'UT': 'Utah',
# 'VA': 'Virginia',
# 'VT': 'Vermont',
# 'WI': 'Wisconsin',
# 'WY': 'Wyoming',
# 'WA': 'Washington',
# 'WV': 'West Virginia'
# }



with open(os.path.join(os.path.abspath('../contamiNation'),'detail_results_comp_updated.json')) as input_data:
    detail_result = json.load(input_data)

    for result in detail_result:
        result_key_list = []

        result_dict = {
        'PWS ID' : result['PWS ID'],
        'Compliance Status' : result['Compliance Status'],

        }

        for key in result:
            if 'Result' in key:
                result_dict['Service Connections'] = result['Result no.1']['Service Connections']
                result_key_list.append(key)

                for result_key in result_key_list:
                    result_dict[result_key] = result[result_key]


        json.dump(result_dict, open(os.path.join('chemical_analysis_data/{0}'.format(result['State/EPA Region']),'{0}.json'.format(result['PWS ID'])), 'w'), indent=4)


# "Result no.1": {
# "Contaminant":
# "Concentration":
# "End Date":
# "Service Connections":
# },
# "Result no.2": {
# "Contaminant":
# "Concentration":
# "End Date":
# "Service Connections":
# }
        # for key in result:
        #     if 'Result' in key:
        #         result_key_list.append(key)
        #
        # for result_key in result_key_list:























# 'PWS Name' :
# 'City' :
# 'State' :
# 'Compliance Status' :
# "Result no.1": {
# "Contaminant":
# "Concentration":
# "End Date":
# "Service Connections":
# },
# "Result no.2": {
# "Contaminant":
# "Concentration":
# "End Date":
# "Service Connections":
# }
