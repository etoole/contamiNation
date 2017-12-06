import json

all_markers = []

def joiner (json_chunk, output_list):
    for result in json_chunk:
        output_list.append(result)

with open('markers_0.json') as list0:
    list0 = json.load(list0)
    joiner(list0, all_markers)

# with open('markers_1.json') as list1:
#     list1 = json.load(list1)
#     joiner(list1, all_markers)

with open('markers_2.json') as list2:
    list2 = json.load(list2)
    joiner(list2, all_markers)

with open('markers_3.json') as list3:
    list3 = json.load(list3)
    joiner(list3, all_markers)

# with open('markers_4.json') as list4:
#     list4 = json.load(list4)
#     joiner(list4, all_markers)

with open('markers_5.json') as list5:
    list5 = json.load(list5)
    joiner(list5, all_markers)

# with open('markers_6.json') as list6:
#     list6 = json.load(list6)
#     joiner(list6, all_markers)

with open('markers_7.json') as list7:
    list7 = json.load(list7)
    joiner(list7, all_markers)

json.dump(all_markers, open('all_markers.json', 'w'))
