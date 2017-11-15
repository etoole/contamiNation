import json

# list_ = []
#
# with open('detail_violations2.json') as all_nat_det:
#     all_nat_det = json.load(all_nat_det)
#     for detail in all_nat_det:
#         list_.append(detail)
# print(len(list_))

list_ = []

with open('pbcu_results.json') as pbcu_results:
    pbcu_results = json.load(pbcu_results)
    for result in pbcu_results:
        list_.append(result)

print(len(list_))
