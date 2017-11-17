import requests, json

geocode_list = []

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'AIzaSyDrawt5ZWXPR7eg0ihu3t6p9A_Yrm1ss0E'

with open('test_results.json') as results:
    results = json.load(results)

    for result in results:
        params = {'address': result['PWS Name'],
        'components' : {
            'locality':result['City'],
            'administrative_area':result['State/EPA Region'],
            'postal_code':result['Zip Code'],
            'country':'us'
            },
        'key': api_key
        }

        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        geocode_list.append(res)

print(geocode_list)
json.dump(geocode_list, open('test_geocode_results.json', 'w'), indent=4)









# params = {
#     'address': '221B Baker Street, London, United Kingdom',
#     'sensor': 'false',
#     'region': 'uk'
# }
#
# # Do the request and get the response data
# req = requests.get(GOOGLE_MAPS_API_URL, params=params)
# res = req.json()
#
# # Use the first result
# result = res['results'][0]
#
# geodata = dict()
# geodata['lat'] = result['geometry']['location']['lat']
# geodata['lng'] = result['geometry']['location']['lng']
# geodata['address'] = result['formatted_address']

#print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
# 221B Baker Street, London, Greater London NW1 6XE, UK. (lat, lng) = (51.5237038, -0.1585531)
