# PWS NAME - CITY, STATE - COMPLIANCE STATUS
# CONTACT FIRST, CONTACT LAST - CONTACT PHONE - CONTACT EMAIL
# ANALYTE | CONCENTRATION | SAMPLING END DATE
# LEAD    | 24 PPB        | 06/30/2016

import json, re, os

site_dict_list = []
pwsid_list = []

with open(os.path.join(os.path.abspath('../geocoding'),'all_markers.json')) as input_data:
    pwsids = json.load(input_data)

    for result in pwsids:
        pwsid_list.append(result['properties']['pwsid'])

with open(os.path.join(os.path.abspath('..'),'detail_results_comp_updated.json')) as detail_data:
    detail_result = json.load(detail_data)

    for result in detail_result:
        if result['PWS ID'] in pwsid_list:

            result_key_list = []
            result_dict_list = []

            site_dict = {
            'PWS ID' : result['PWS ID'],
            'Compliance Status' : result['Compliance Status'],
            'Population Served' : result['Population Count'],
            'Contact Name': result['Contact Name'],
            'Contact Phone': result['Contact Phone'],
            'Contact Email': result['Contact Email']
            }

            for key in result:
                if 'Result' in key:
                    result_key_list.append(key)

                for result_key in result_key_list:
                    result_dict = {
                    'Contaminant': result[result_key]['Contaminant'],
                    'Concentration': result[result_key]['Concentration'],
                    'End Date': result[result_key]['End Date']
                    }
                    result_dict_list.append(result_dict)
                    result_dict_list = [dict(t) for t in set([tuple(d.items()) for d in result_dict_list])]

            site_dict['Results'] = result_dict_list
            site_dict_list.append(site_dict)


        json.dump(site_dict, open(os.path.join('../chemical_analysis_data/individual_results/{0}.json'.format(result['PWS ID'])), 'w'))
        #
        #




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
