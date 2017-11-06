import csv

# bio_result_var = []
# chem_result_var = []
# narrow_result_var = []

bio_set = []
bio_populated_test = []

with open('test_bio_result.csv') as bio_data:
    bio_data = csv.reader(bio_data)
    bio_row1 = next(bio_data)
    bio_row2 = next(bio_data)

    for data_column in bio_row2:
        if data_column == "":
            bio_populated_test.append('Empty')
        else:
            bio_populated_test.append('Filled')

            for title_column in bio_row1:
                title_column_list.append(title_column)
                for test_column in bio_populated_test:
                    if test_column == 'Filled':
                        bio_set.append(title_column)

bio_list_set = set(bio_set)

print(bio_list_set)

# with open('test_chem_result.csv') as chem_data:
#     chem_data = csv.reader(chem_data)
#     chem_set = set(next(chem_data))
#
# with open('test_narrow_result.csv') as narrow_data:
#     narrow_data = csv.reader(narrow_data)
#     narrow_set = set(next(narrow_data))
#
# # print('{0}\n\n{1}\n\n{2}\n\n'.format(bio_result_var, chem_result_var, narrow_result_var))
#
#
# bio_chem_dif = bio_set - chem_set
# bio_narrow_dif = bio_set - narrow_set
# narrow_chem_dif = narrow_set - chem_set
#
# print("Variable is in bio result but not chem result: \n")
# for row in bio_chem_dif:
#     print(row)
#
# print('\n\nVariable is in bio/chem result but not narrow result: \n')
# for row in bio_narrow_dif:
#     print(row)
#
# print("\n\nVariable is in narrow result but not bio/chem result: \n")
# for row in narrow_chem_dif:
#     print(row)
