import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.CharlestonCounty import WebParser


governmax_api_key = 'E4D2DBDC03F14F9792D58D89BFB30CC7'

Governmax = WebParser(governmax_api_key)
Governmax.writeAndQuery('2014', exportPath='../data/governmax-2014.csv')
