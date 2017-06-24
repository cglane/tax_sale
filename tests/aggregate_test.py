import unittest
import sys, os
import csv
sys.path.append(os.path.abspath(os.path.join('..')))

from lib.AggregateData import AggregateData
governmax_api_key = '131F8BD68C1848DF91406C829A1AB5C2'


class TestStringMethods(unittest.TestCase):
    """This is For Testing."""
    def test_write_and_query(self):
        """Read from csv and query zillow"""
        Aggregation = AggregateData('governmax-test', governmax_api_key, '../data/data-test.csv')
        Aggregation.writeAndQuery()
        test_data = [x for x in csv.DictReader(open('../data/data-test.csv'))]
        self.assertEqual(test_data[0]['latitude'], '32.625842')


if __name__ == '__main__':
    unittest.main()
