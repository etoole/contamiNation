import json
from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

with open ('detail_results_comp_updated.json') as all_results:
    all_results = json.load(all_results)

    for i, group in enumerate(grouper(all_results, 5000)):
        with open('outputbatch_{}.json'.format(i), 'w') as outputfile:
            json.dump(list(group), outputfile)














# import json
#
# group_1 = []
# group_2 = []
# group_3 = []
# group_4 = []
# group_5 = []
# group_6 = []
# group_7 = []
# group_8 = []
# group_9 = []
# group_10 = []
# group_11 = []
# group_12 = []
# group_13 = []
# group_14 = []
#
# group_counter = 0
# dictionary_counter = 0
#
# with open ('detail_results_comp_updated.json') as all_results:
#     all_results = json.load(all_results)
#
#     dictionary_counter = 0
#     while (dictionary_counter<500):
#         group_counter +=1
#         group_number = "group_{0}".format(group_counter)
#         print(group_number)
#         dictionary_counter += 1
#         for dicitonary in all_results:
#             group_number.append(dictionary)
