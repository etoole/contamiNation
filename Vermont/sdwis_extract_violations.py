import csv, json

all_violations = []

pws_id = []
pws_type = []
population_served = []
violation_type = []
compliance_status = []


with open('sdwis_report_clean.csv') as report:
    report_data = csv.DictReader(report)
    for dictionary in report_data:
        if dictionary['Compliance Status'] != 'System Inactive':
            pws_id = dictionary['PWS ID']
            pws_type = dictionary['PWS Type']
            population_served = dictionary['Population Served Count']
            violation_type = dictionary['Violation Type']
            compliance_status = dictionary['Compliance Status']

            # insert wsid_to database.py code using pws_id variable instead of dictionary['WSID']
            # read pdfs, save locally as csv, extract vars date, analyte, concentration & sampling location
            # fix sampling location text


            violation = ({
            'WSID' : pws_id,
            'Compliance Status' : compliance_status,
            'Population Served' : population_served,
            'Water System Type' : pws_type,
            'Violation Type' : violation_type
            })

            all_violations.append(violation)

json.dump(all_violations, open('sdwis_violations.json','w'), indent=4)
