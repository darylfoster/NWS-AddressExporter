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
    # latitude_min = 35.25985966009217
    # latitude_max = 35.28591600668164
    latitude_min = 35.23380331
    latitude_max = 35.25985967
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
        object_id = str(address['OBJECTID'])
        if object_id not in address_db or not address_db[object_id]:
            if address['FULLADDR'] + '-' + address['POSTALCOM'] in exported_addresses:
                address['Exported'] = True
            else:
                address['Exported'] = False
            address_db[object_id] = address
    with open(master_file_name, 'w') as master_output:
        json.dump(address_db, master_output)

def init_csv_file(file_name):
    csv_output = open(file_name + '.csv', 'w', newline='')
    csv_writer = csv.writer(csv_output, delimiter=',')
    csv_writer.writerow(['Number', 'Street', 'City', 'State', 'PostalCode', 'Latitude', 'Longitude', 'Type', 'ApartmentNumber'])
    return csv_output, csv_writer


def export_street_addresses(file_name):
    with open(master_file_name, 'r') as master_input:
        address_db = json.load(master_input)
    # TODO: Create a new file every 300 records
    record_count = 0
    file_count = 0
    csv_output, csv_writer = init_csv_file(file_name)
    for key in address_db:
        address = address_db[key]

        if record_count >= 300:
            record_count = 0
            file_count += 1
            csv_output.close()
            csv_output, csv_writer = init_csv_file(file_name + str(file_count))

        if not address['Exported']:
            number = address['ADDRNUM']
            street = address['FULLSTREET']
            city = address['POSTALCOM']
            state = address['State']
            postal_code = address['POSTALZIP']
            latitude = address['YCOOR']
            longitude = address['XCOOR']
            if (address['COMMENTS'] and address['COMMENTS'].strip()) or (address['UNIT'] and address['UNIT'].strip()):
                address_type = 'Apartment'
                apartment = address['UNIT']
            else:
                address_type = 'House'
                apartment = None
            csv_writer.writerow([number, street, city, state, postal_code, latitude, longitude, address_type, apartment])
            address['Exported'] = True
            record_count += 1
    csv_output.close()
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
