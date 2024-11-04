from urllib.parse import urlencode
import sys
import requests
import csv
import json

master_file_name = 'TransylvaniaCounty.json'

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
    with open(master_file_name, 'r') as master_input:
        address_db = json.load(master_input)
    with open('TransylvaniaCounty-Exported.json', 'r') as exported_file:
        exported_addresses = json.load(exported_file)
    for record in records:
        address = record['attributes']
        if address['FULLADDR'] + '-' + address['POSTALCOM'] in exported_addresses:
            address['Exported'] = True
        else:
            address['Exported'] = False
        address_db[str(record['attributes']['OBJECTID'])] = address
    with open(master_file_name, 'w') as master_output:
        json.dump(address_db, master_output)

def export_street_addresses(file_name):
    with open(master_file_name, 'r') as master_input:
        address_db = json.load(master_input)
    with open(file_name + '.csv', 'w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output, delimiter=',')
        csv_writer.writerow(['Number', 'Street', 'City', 'State', 'PostalCode', 'Latitude', 'Longitude', 'Type', 'ApartmentNumber'])
        for key in address_db:
            address = address_db[key]
            if not address['Exported']:
                number = address['ADDRNUM']
                street = address['FULLSTREET']
                city = address['POSTALCOM']
                state = address['State']
                postal_code = address['POSTALZIP']
                latitude = address['YCOOR']
                longitude = address['XCOOR']
                if address['COMMENTS'] or address['UNIT']:
                    address_type = 'Apartment'
                    apartment = address['UNIT']
                else:
                    address_type = 'House'
                    apartment = None
                csv_writer.writerow([number, street, city, state, postal_code, latitude, longitude, address_type, apartment])
                address['Exported'] = True
    with open(master_file_name, 'w') as master_output:
        json.dump(address_db, master_output)

# Script starts here
action = sys.argv[1]

match action:
    case 'pull':
        address_data = request_addresses()
        append_master_addresses(address_data)
    case 'export':
        export_street_addresses(sys.argv[2])
    case default:
        print('Unknown argument: ' + action)
