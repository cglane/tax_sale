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
            return results['results'][0]['geometry']['location']
        else:
            print results['status']
            return {'lat': '', 'lng': ''}
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
    def readFileQuery(self, fileName, exportPath):
        "Read file and query each row that doesn't have lat, long."
        fileDict = [x for x in csv.DictReader(open('../imports/'+fileName+'.csv'))]
        export_file_contents = [x for x in csv.DictReader(open(exportPath))]
        for itr, row in enumerate(fileDict):
            if row['lat'] == '':
                latLng = self.getLatLong(row['Parcel Address'])
                row['lat'] = latLng['lat']
                row['lng'] = latLng['lng']
                self.writeRowToFile(row, exportPath)
            else:
                self.writeRowToFile(row, exportPath)
