import re, os, json, datetime, time

result_key_list = []
concentration_list = []

day = re.compile('(?<=on\s)\w+')
month = re.compile('(?<=\d-)[A-Z]{3}')
year = re.compile('[0-9]{4}')
concentration_digit = re.compile('[0-9]+')

month_table = {
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


with open(os.path.join('detail_results.json')) as results:
    results = json.load(results)

    for result in results:

        if 'Returned' in result['Compliance Status']:
            status = result['Compliance Status']

            result_day = day.findall(status)
            result_month = month.findall(status)
            result_year = year.findall(status)

            result_day = result_day[0]
            result_month = result_month[0]
            result_year = result_year[0]

            for month_abrv in month_table:
                if str(month_abrv) == result_month:
                    result_month = month_table[result_month]

            date_format = '{0}/{1}/{2}'.format(result_month, result_day, result_year)
            dt = datetime.datetime.strptime(date_format, '%m/%d/%Y')
            rtc = time.mktime(dt.timetuple())



            for key in result:
                if 'Result' in key:
                    result_key_list.append(key)

            for result_key in result_key_list:
                end_date = result[result_key]['End Date']
                if end_date > rtc:
                    concentration = result[result_key]['Concentration']
                    concentration = concentration_digit.findall(concentration)
                    concentration = int(concentration[0])
                    concentration_list.append(concentration)



            concentration_list = sorted(concentration_list)
            detection = False
            # print(result['Compliance Status'])
            #if highest result of all post-return-to-compliance data results is not zero, change compliance status to 'Not Compliant'
            if len(concentration_list) > 0:
                # print(concentration_list[-1])
                if concentration_list[-1] > 0:
                    result['Compliance Status'] = 'Not Compliant'


            # print(result['Compliance Status'] + '\n')

            for result_key in result_key_list:
                end_date = result[result_key]['End Date']
                end_date = datetime.date.fromtimestamp(end_date)
                result[result_key]['End Date'] = end_date.strftime("%m/%d/%y")

            if 'Returned' in result['Compliance Status']:
                rtc = datetime.date.fromtimestamp(rtc)
                result['Compliance Status'] = 'Returned to Compliance on {0}'.format(rtc.strftime("%m/%d/%y"))

            print(result)

            concentration_list = []
            result_key_list = []


json.dump(results, open('detail_results_comp_updated.json', 'w'), indent=4)








# numbers = []
#
# number_range = range(1,101)
# for number in number_range:
#     numbers.append(int(number))
#
#
# with open(os.path.join('geocoding','test_results.json')) as results:
#     results = json.load(results)
#
#
#
#     for result in results:
#         for number in numbers:
#             if
#             indiv_result = result['Result no.{0}'.format(number)]
#
#
#
#
#
#     sorted_results = sorted(results, key=itemgetter('', 'age'))
#
#                 for key, value in sorted(mydict.iteritems(), key=lambda (k,v): (v,k)):
