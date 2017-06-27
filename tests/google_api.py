import unittest
import sys, os
import requests
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.GoogleAPI import LocationData
test_address = '107 BLUE HERON POND RD, KIAWAH ISLAND'

class TestReadWriteQuery(unittest.TestCase):
    """This is For Testing."""
    def test_query_zillow(self):
        """This is to test the connection with governmax."""
        google_api = LocationData()
        latLng = google_api.getLatLong(test_address)
        self.assertEqual(latLng['lat'], '32.625849')


if __name__ == '__main__':
    unittest.main()
