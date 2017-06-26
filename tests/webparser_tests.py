import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser
from lib.zillowAPI import ZillowAPI
property_pin = '4581301045'
governmax_api_key = 'FEF8EC5AED114482874581334CADB4C8'


class TestStringMethods(unittest.TestCase):
    """This is For Testing."""
    def test_connection_county(self):
        """This is to test the connection with governmax."""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        overview = web_parser.getOverview()
        self.assertEqual(overview['Parcel Address'], '13 TRADD ST, CHARLESTON')
    def test_current_parcel_info(self):
        """"This checks currenc parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getCurrentParcelInfo()
        self.assertEqual(data['Owner'], 'MARCUS ARNOLD L TRUST MARCUS BARBARA C TRUST')
    def test_historic_information(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getHistoricInformation()
        self.assertEqual(data[0]['Land'], '$779,000')
    def test_sales_disclosure(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getSalesDisclosure()
        self.assertEqual(data[0]['Date'], '12/23/2013')
    def test_get_improvements(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getImprovements()
        self.assertEqual(data[0]['Finished Sq. Ft.'], '2,291')
    def test_aggregate(self):
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.aggregateData('2013')
        print (data, 'data')
        self.assertEqual(data['lowestSalesValue'], 5.0)


if __name__ == '__main__':
    unittest.main()
