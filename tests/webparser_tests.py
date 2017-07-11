import unittest
import sys, os
import csv
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser
from lib.zillowAPI import ZillowAPI
property_pin = '2030000115'
governmax_api_key = 'BEBF3C1F72E84A1C9E28BA17F0EDD369'


class TestStringMethods(unittest.TestCase):
    """This is For Testing."""
    def test_connection_county(self):
        """This is to test the connection with governmax."""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        overview = web_parser.getOverview()
        self.assertEqual(overview['Parcel Address'], '5345 HALFWAY CREEK RD, MC CLELLANVILLE')
    def test_current_parcel_info(self):
        """"This checks currenc parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getCurrentParcelInfo()
        self.assertEqual(data['Owner'], 'WILLIAMS VALERIA H')
    def test_second_dict(self):
        """"This checks currenc parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getCurrentParcelInfo()
        print data
        self.assertEqual(data['Owner'], 'WILLIAMS VALERIA H')
    def test_historic_information(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getHistoricInformation()
        self.assertEqual(data[0]['Land'], '$10,000')
    def test_sales_disclosure(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getSalesDisclosure()
        self.assertEqual(data[0]['Date'], '8/15/2006')
    def test_get_improvements(self):
        """"This checks historic parcel info"""
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.getImprovements()
        self.assertEqual(data[0]['Finished Sq. Ft.'], '')
    def test_aggregate(self):
        web_parser = WebParser(governmax_api_key)
        web_parser.getSoup(property_pin)
        data = web_parser.aggregateData('2013')
        self.assertEqual(data['lowestSalesValue'], 0.0)
    def test_write_to_filed(self):
        web_parser = WebParser(governmax_api_key)
        web_parser.writeAndQuery('test', '../data/test.csv')
        data_dict = [x for x in csv.DictReader(open('../data/test.csv'))]
        self.assertEqual(data_dict[0]['lowestSalesValue'], '0.0')


if __name__ == '__main__':
    unittest.main()
