import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser
from lib.zillowAPI import ZillowAPI
from lib.PropertyData import getPropertyInfo
property_pin = '3500600166'
governmax_api_key = '4CC385361D944882A296CDFDBBF886BD'


class TestStringMethods(unittest.TestCase):
    """This is For Testing."""
    def test_connection_county(self):
        """This is to test the connection with governmax."""
        web_parser = WebParser(governmax_api_key)
        data = web_parser.getDataByPin(property_pin)
        print data
        self.assertEqual(data['address'], '13 TRADD ST, CHARLESTON')

    # def test_zillow_results(self):
    #     """This calls zillow with the address supplied from governmax."""
    #     web_parser = WebParser(property_pin)
    #     web_parser.getDataByPin(governmax_api_key)
    #     zillow_address = web_parser.formatAddressForZillow()
    #     zillow_api = ZillowAPI(zillow_address)
    #     zillow_results = zillow_api.queryZillow(zillow_address)
    #     self.assertEqual(zillow_results['yearBuilt'], '1778')
    #
    # def test_get_property_data(self):
    #     """This calls governmax and zillow."""
    #     print 'getPropertyInfo'
    #     results = getPropertyInfo(governmax_api_key, property_pin)
    #     print results
    #     self.assertEqual(results['yearBuilt'], '1778')


if __name__ == '__main__':
    unittest.main()
