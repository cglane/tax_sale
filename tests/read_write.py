import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser
governmax_api_key = 'E4D2DBDC03F14F9792D58D89BFB30CC7'


class TestReadWriteQuery(unittest.TestCase):
    """This is For Testing."""
    def test_read_query(self):
        """This is to test the connection with governmax."""
        Governmax = WebParser(governmax_api_key)
        Governmax.writeAndQuery('test', exportPath='../data/governmax-2012.csv')
        # self.assertEqual(finalDict[0]['address'], '107 BLUE HERON POND RD, KIAWAH ISLAND')


if __name__ == '__main__':
    unittest.main()
