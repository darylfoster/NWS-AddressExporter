from urllib.parse import urlencode
import requests
import csv
import json

def request_addresses():
    url_base = 'https://gis.transylvaniacounty.org/server/rest/services/Addresses/FeatureServer/0/query?'
    county = 'TRANSYLVANIA'
    city = 'BREVARD'
    longitude_min = -82.72856422933208
    longitude_max = -82.65685061335734
    latitude_min = 35.25985966009217
    latitude_max = 35.28591600668164
    where_parameters = 'COUNTY = \'' + county + '\' AND POSTALCOM = \'' + city + '\' AND XCOOR >= ' + str(longitude_min) + ' AND XCOOR <= ' + str(longitude_max) + ' AND YCOOR >= ' + str(latitude_min) + ' AND YCOOR <= ' + str(latitude_max)
    parameters = {
      'where':where_parameters,
      'outFields':'*',
      'returnGeometry':'false',
      'outSR':4326,
      'f':'json'
    }
    query_string = urlencode(parameters)
    url = url_base + query_string

    response = requests.get(url)
    if response.ok:
        response_data = response.json()
        return response_data['features']
    else:
        print('Response code: ' + str(response.status_code) + '\nResponse detail: ' + response.text)
        return None

def append_master_addresses(records):
    address_db = {}
    for record in records:
        address_db[record['attributes']['OBJECTID']] = record['attributes']
    with open('TransylvaniaCounty.json', 'w') as master_file:
        json.dump(address_db, master_file)

# Script starts here
address_data = request_addresses()
append_master_addresses(address_data)
