import json
import operator
import time
import datetime

detail_results = []


with open('detail_violations_deduped.json') as detail_violations:
    with open('pbcu_results.json') as pbcu_results:
        detail_violations = json.load(detail_violations)
        pbcu_results = json.load(pbcu_results)

        detail_violations.sort(key=operator.itemgetter('PWS ID'))
        pbcu_results.sort(key=operator.itemgetter('PWS ID'))

        for result in pbcu_results:
            end_date = result['End Date']
            dt = datetime.datetime.strptime(end_date, '%m/%d/%Y')
            ts = time.mktime(dt.timetuple())
            result.update({'End Date': ts})

        pbcu_results.sort(key=operator.itemgetter('End Date'), reverse=True)


        for detail in detail_violations:
            detail_id = detail['PWS ID']

            counter = 1

            for result in pbcu_results:
                if result['PWS ID'] == detail_id:

                    detail.update({'Result no.{0}'.format(counter) : {
                    "Contaminant": result['Contaminant'],
                    "Concentration": result['Result'],
                    "End Date": result['End Date'],
                    "Service Connections": result['Service Connections']
                    }})

                    counter = counter + 1


            detail_results.append(detail)


print(len(detail_results))
json.dump(detail_results, open('detail_results.json', 'w'), indent=4)
