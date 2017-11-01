import csv

bio_var_list = []
chem_var_list = []
narrow_var_list = []
flag = True

with open('test_bio_result.csv') as bio_data:
    bio_data = csv.DictReader(bio_data)
    if flag == True:
        for dictionary in bio_data:
            bio_full_dict = {k:v for k,v in dictionary.items() if v != ''}
            for keys in bio_full_dict:
                bio_var_list.append(keys)
                bio_var_set = set(bio_var_list)
                flag == False


flag = True

with open('test_chem_result.csv') as chem_data:
    chem_data = csv.DictReader(chem_data)
    if flag == True:
        for dictionary in chem_data:
            chem_full_dict = {k:v for k,v in dictionary.items() if v != ''}
            for keys in chem_full_dict:
                chem_var_list.append(keys)
                chem_var_set = set(chem_var_list)
                flag == False

flag = True

with open('test_bio_result.csv') as narrow_data:
    narrow_data = csv.DictReader(narrow_data)
    if flag == True:
        for dictionary in narrow_data:
            narrow_full_dict = {k:v for k,v in dictionary.items() if v != ''}
            for keys in narrow_full_dict:
                narrow_var_list.append(keys)
                narrow_var_set = set(narrow_var_list)
                flag == False

print(bio_var_set)
print(chem_var_set)
print(narrow_var_set)
