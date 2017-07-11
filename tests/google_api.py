import unittest
import sys, os
import requests
import csv
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.GoogleAPI import LocationData
test_address = '107 BLUE HERON POND RD, KIAWAH ISLAND'

class TestReadWriteQuery(unittest.TestCase):
    """This is For Testing."""
    def test_query_google(self):
        """This is to test the connection with governmax."""
        google_api = LocationData()
        latLng = google_api.getLatLong(test_address)
        self.assertEqual(latLng['lat'], 32.625849)

    def test_read_query(self):
        google_api = LocationData()
        google_api.readFileQuery('../imports/test.csv', '../data/test.csv')
        data_dict = [x for x in csv.DictReader(open('../data/test.csv'))]
        self.assertEqual(data_dict[0]['lat'], '32.625849')
if __name__ == '__main__':
    unittest.main()
