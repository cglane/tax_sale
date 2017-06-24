import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.AggregateData import AggregateData

ZILLOW_API_KEY = 'X1-ZWz195za60umff_728x4'
JUANES_API_KEY = 'X1-ZWz1950j8ffu2z_1u0pu'

Aggregation = AggregateData('governmax-2014', '../data/data-2014.csv', JUANES_API_KEY)
Aggregation.writeAndQuery()
