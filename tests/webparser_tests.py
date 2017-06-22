import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser
from lib.zillowAPI import ZillowAPI
property_pin = '4581301045'
governmax_api_key = 'B07C904752684AF08A2BB27E4E9B3C11'
class TestStringMethods(unittest.TestCase):
    "This is For Testing"
    def test_connection_county(self):
        """This is to test the connection with governmax."""
        web_parser = WebParser(property_pin)
        data = web_parser.getDataByPin(governmax_api_key)
        self.assertEqual(data['address'], '13 TRADD ST, CHARLESTON')

    def test_zillow_results(self):
        web_parser = WebParser(property_pin)
        web_parser.getDataByPin(governmax_api_key)
        zillow_address = web_parser.formatAddressForZillow()
        zillow_api = ZillowAPI(zillow_address)
        zillow_results = zillow_api.queryZillow(zillow_address)
        print zillow_results
        self.assertEqual(zillow_results['yearBuilt'], '1778')

if __name__ == '__main__':
    unittest.main()
