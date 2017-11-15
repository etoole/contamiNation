import csv, json, re, os

all_pbcu = []


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
        'PWS ID' : pws_id,
        'Result' : result,
        'Contaminant' : contaminant,
        'End Date' : end_date,
        'Service Connections' : service_connections,
        }
        all_pbcu.append(pbcu)


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



json.dump(all_pbcu, open('pbcu_results.json', 'w'), indent= 4)
