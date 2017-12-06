import requests, json, re, os

geojson_list = []
geocode_list = []
zip_pattern = re.compile('[0-9]{5}(?!.)')

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'AIzaSyDrawt5ZWXPR7eg0ihu3t6p9A_Yrm1ss0E'

with open(os.path.join(os.path.abspath('../geocoding/'),'list_index_error.json')) as results:
    results = json.load(results)

    for result in results:
        if result['Zip Code'] != '-':
            for result_key in result:
                if result_key == 'Result no.1':

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

                    if res['status'] !='ZERO_RESULTS':
                        if len(res['results']) > 0:

                            address_components = res['results'][0]['address_components']

                            for components in address_components:
                                if components['types'][0] == 'postal_code':

                                    m = re.match(zip_pattern, components['long_name'])
                                    if m:
                                        google_maps_zip_code = m.group()
                                        google_maps_zip_short = re.match('[0-9]{3}', google_maps_zip_code)


                            latitude = res['results'][0]['geometry']['location']['lat']
                            longitude = res['results'][0]['geometry']['location']['lng']
                            coordinates = [longitude, latitude]

                            epa_zip_short = re.match('[0-9]{3}', result['Zip Code'])
                            if epa_zip_short.group() == google_maps_zip_short.group():
                                print(epa_zip_short.group())
                                print(google_maps_zip_short.group())
                                    #write geojson with google maps data and pwsid at end

                                geojson = {
                                      "type": "Feature",
                                      "geometry": {
                                        "type": "Point",
                                        "coordinates": coordinates
                                      },
                                      "properties": {
                                        "title": result['PWS Name'],
                                        "description": res['results'][0]['formatted_address'],
                                        "pwsid": result['PWS ID'],
                                        "icon": {
                                        "iconUrl": result['Marker Color'],
                                        "iconSize": [25,25]
                                        }
                                      }
                                    }
                                geojson_list.append(geojson)
                                print(geojson)
                            else:
                                    #write geojson with epa zipcode. make googlemaps request for longlat and use epa name & pwsid
                                print(epa_zip_short.group())
                                print(google_maps_zip_short.group())
                                zipcode_marker = {'address' : result['Zip Code'],
                                'key': api_key
                                }

                                zip_req = requests.get(GOOGLE_MAPS_API_URL, params=zipcode_marker)
                                zip_res = zip_req.json()
                                if zip_res['status'] != 'ZERO_RESULTS':
                                    zip_latitude = zip_res['results'][0]['geometry']['location']['lat']
                                    zip_longitude = zip_res['results'][0]['geometry']['location']['lng']
                                    zip_coordinates = [zip_longitude, zip_latitude]
                                    print(zip_coordinates)
                                geojson = {
                                      "type": "Feature",
                                      "geometry": {
                                        "type": "Point",
                                        "coordinates": zip_coordinates
                                      },
                                      "properties": {
                                        "title": result['PWS Name'],
                                        "description": "{0}, {1} {2}".format(result['City'], result['State/EPA Region'], result['Zip Code']),
                                        "pwsid": result['PWS ID'],
                                        "icon": {
                                        "iconUrl": result['Marker Color'],
                                        "iconSize": [25,25]
                                        }
                                      }
                                    }
                                geojson_list.append(geojson)
                                print(geojson)
