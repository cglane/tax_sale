import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lib.GoogleAPI import LocationData

google_api = LocationData()
google_api.readFileQuery('../data/data-2012.csv', '../data/data-all.csv')
google_api.readFileQuery('../data/data-2013.csv', '../data/data-all.csv')
google_api.readFileQuery('../data/data-2014.csv', '../data/data-all.csv')
