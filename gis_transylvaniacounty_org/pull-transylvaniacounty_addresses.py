from urllib.parse import urlencode
import sys
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
    with open('TransylvaniaCounty.json', 'r') as master_input:
        address_db = json.load(master_input)
    with open('TransylvaniaCounty-Exported.json', 'r') as exported_file:
        exported_addresses = json.load(exported_file)
    for record in records:
        address = record['attributes']
        if exported_addresses[record['FULLADDR'] + '-' + record['POSTALCOM']]:
            address['Exported'] = True
        address_db[str(record['attributes']['OBJECTID'])] = address
    with open('TransylvaniaCounty.json', 'w') as master_output:
        json.dump(address_db, master_output)

# Script starts here
action = sys.argv[1]

match action:
    case 'pull':
        address_data = request_addresses()
        append_master_addresses(address_data)
    case default:
        print('Unknown argument: ' + action)
