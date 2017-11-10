import csv

all_pbcu = []

with open('copper_samples.csv') as copper:
    copper_samples = csv.DictReader(copper)

    for dictionary in copper_samples:
        pws_id = dictionary['PWS ID']
        result = dictionary['Sample Measure (mg/L)']
        contaminant = dictionary['Contaminant Name']
        start_date = dictionary['Sampling Start Date']
        service_connections = dictionary['Service Connections Count']

        pbcu = {
        'PWS ID' : pws_id,
        'Result' : result,
        'Contaminant' : contaminant,
        'Start Date' : start_date,
        'Service Connections' : service_connections,
        }
        all_pbcu.append(pbcu)

with open('lead_samples.csv') as lead:
    lead_samples = csv.DictReader(lead)

    for dictionary in lead_samples:
        pws_id = dictionary['PWS ID']
        result = dictionary['Sample Measure (mg/L)']
        contaminant = dictionary['Contaminant Name']
        start_date = dictionary['Sampling Start Date']
        service_connections = dictionary['Service Connections Count']

        pbcu = {
        'PWS ID' : pws_id,
        'Result' : result,
        'Contaminant' : contaminant,
        'Start Date' : start_date,
        'Service Connections' : service_connections,
        }
        all_pbcu.append(pbcu)

print(all_pbcu)
