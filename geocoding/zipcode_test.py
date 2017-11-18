import requests, json, re

zipcode_data = []
zipcodes = [98271,
97306,
98526,
98036,
99122,
98952,
98562,
99109,
98951,
81611,
98247,
75074,
98264,
98948,
93274,
99040,
99040,
98223,
98241,
98513,
98513,
98513,
75230,
75230,
99801,
99827,
99840,
99840,
99840,
99901]

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'AIzaSyDrawt5ZWXPR7eg0ihu3t6p9A_Yrm1ss0E'

for code in zipcodes:
    params = {'address' : code,
    'key': api_key
    }

    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    print(req)
    print(res)
    zipcode_data.append(res)
json.dump(zipcode_data, open('zipcode_test.json','w'), indent=4)
