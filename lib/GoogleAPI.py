import requests
import csv
import json
API_KEY = 'AIzaSyCW_RhZ1WBIUVbXT_kG_39d7-LPD-BG2x4'


class LocationData(object):
    """docstring for LocationData."""
    def __init__(self):
        super(LocationData, self).__init__()
        self.API_KEY = API_KEY

    def getLatLong(self, address):
        """Get lat long from google."""
        api_string = 'https://maps.googleapis.com/maps/api/geocode/json?address='
        address_string = "+".join(address.split(' '))
        query_string = api_string+address_string+'&key='+self.API_KEY
        results = json.loads(requests.get(query_string).content)
        if(results['status'] == 'OK'):
            print results['results'][0]['geometry']['location']['lat']
            if results['results'][0]['geometry']['location']['lat'] < 34.0:
                return results['results'][0]['geometry']['location']
            elif len(results['results']) > 1:
                if results['results'][1]['geometry']['location']['lat'] < 34.0:
                    return results['results'][1]['geometry']['location']
                else:
                    return {'lat': '', 'lng': ''}
        elif results['status'] == 'ZERO_RESULTS':
            return {'lat': '', 'lng': ''}
        else:
            raise ValueError('Over API Threshold')
    def writeRowToFile(self, data_dict, exportPath):
        "Read file and write row"
        export_file_contents = [x for x in csv.reader(open(exportPath))]
        with open(exportPath, 'a') as export:
            writer = csv.DictWriter(export, fieldnames=data_dict.keys())
            if(len(export_file_contents) < 1):
                print ('Write Header')
                writer.writeheader()
                writer.writerow(data_dict)
            else:
                writer.writerow(data_dict)
            export.close()
    def readFileQuery(self, importPath, exportPath):
        "Read file and query each row that doesn't have lat, long."
        fileDict = [x for x in csv.DictReader(open(importPath))]
        export_file_contents = [x for x in csv.DictReader(open(exportPath))]
        for itr, row in enumerate(fileDict):
            try:
                if ((row['lat'] == '' or float(row['lat']) > 34.0) and not any(d['Pin'] == row['Pin'] for d in export_file_contents)):
                    latLng = self.getLatLong(row['Parcel Address'])
                    row['lat'] = latLng['lat']
                    row['lng'] = latLng['lng']
                    self.writeRowToFile(row, exportPath)
            except Exception as e:
                print (e, row['Pin'])
