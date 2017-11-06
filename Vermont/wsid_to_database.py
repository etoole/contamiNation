import csv, json, requests, os, tabula


with open('sdwis_violations.json') as violations:
    violations = json.load(violations)
    for dictionary in violations:
        r = requests.get('https://anrweb.vt.gov/DEC/DWGWP/license.aspx?GrpCode=CL90&sWSID={0} &TYPE=pbcu'.format(dictionary['WSID']))
        with open(os.path.join('tables', '{0}.pdf'.format(dictionary['WSID'])), 'wb') as f:
            f.write(r.content)
        tabula.convert_into(os.path.join('tables', '{0}.pdf'.format(dictionary['WSID'])), os.path.join('tables', '{0}.csv'.format(dictionary['WSID'])), output_format="csv")
        os.remove(os.path.join('tables', '{0}.pdf'.format(dictionary['WSID'])))
