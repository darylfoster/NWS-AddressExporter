from urllib.parse import urlencode
import sys
import requests
import csv
import json

master_file_name = 'TransylvaniaCounty.json'

class GeoRectangle:
    longitude_min = 0
    longitude_max = 0
    latitude_min = 0
    latitude_max = 0

    def __init__(self, longitude_min, longitude_max, latitude_min, latitude_max):
        self.longitude_min = longitude_min
        self.longitude_max = longitude_max
        self.latitude_min = latitude_min
        self.latitude_max = latitude_max

def request_addresses(area):
    url_base = 'https://gis.transylvaniacounty.org/server/rest/services/Addresses/FeatureServer/0/query?'
    county = 'TRANSYLVANIA'
    where_parameters = 'COUNTY = \'' + county + '\' AND XCOOR >= ' + str(area.longitude_min) + ' AND XCOOR <= ' + str(area.longitude_max) + ' AND YCOOR >= ' + str(area.latitude_min) + ' AND YCOOR <= ' + str(area.latitude_max)
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
    record_count = 0
    file_count = 0
    csv_output, csv_writer = init_csv_file(file_name)
    for key in address_db:
        address = address_db[key]

        # Create a new file every 300 records
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
            apartment = address['UNIT']
            if address['ADDRESSTYPE'] == 'COM':
                address_type = 'Business'
            elif address['ADDRESSTYPE'] == 'MFD':
                address_type = 'Apartment'
            elif address['ADDRESSTYPE'] == 'SFD':
                address_type = 'House'
            else:
                address_type = 'Other'
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
        lng_min = sys.argv[2]
        lng_max = sys.argv[3]
        lat_min = sys.argv[4]
        lat_max = sys.argv[5]
        area = GeoRectangle(lng_min, lng_max, lat_min, lat_max)
        address_data = request_addresses(area)
        append_master_addresses(address_data)
    case 'export':
        export_street_addresses(sys.argv[2])
    case default:
        print('Unknown argument: ' + action)
