import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from lib.AggregateData import AggregateData
governmax_api_key = '131F8BD68C1848DF91406C829A1AB5C2'


class TestStringMethods(unittest.TestCase):
    """This is For Testing."""
    def test_read_csv(self):
        """This is to test the connection with governmax."""
        Aggregation = AggregateData(['2012'], governmax_api_key)
        agg_dict = Aggregation.readCSV('2012')
        self.assertEqual(agg_dict[0]['Pin'], '2650200054')
    def test_read_zillow(self):
        """Read from csv and query zillow"""
        Aggregation = AggregateData(['test'], governmax_api_key)
        agg_dict = Aggregation.readCSV('test')
        zillow_data = Aggregation.getZillowData(agg_dict[0])
        self.assertEqual(zillow_data['latitude'], '32.625842')
    def test_build_dictionary_list(self):
        """For testing building large dictionary list."""
        Aggregation = AggregateData(['test'], governmax_api_key)
        dictionay_list = Aggregation.buildDictionaryList('test')
        self.assertEqual(dictionay_list[0]['property_code'], '905 - VAC-RES-LOT')
    def test_build_and_write(self):
        Aggregation = AggregateData(['test'], governmax_api_key)
        Aggregation.buildAndWrite()
if __name__ == '__main__':
    unittest.main()
