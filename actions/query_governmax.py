import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser


governmax_api_key = '72477E9A8976468CADD1CC57631BDC8F'


Governmax = WebParser(governmax_api_key)
Governmax.writeAndQuery('2013', exportPath='../data/data-2013.csv')
Governmax.writeAndQuery('2013', exportPath='../data/data-2013.csv')
Governmax.writeAndQuery('2014', exportPath='../data/data-2014.csv')
