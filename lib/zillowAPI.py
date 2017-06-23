import requests
import xmltodict, json
from collections import defaultdict
from yattag import indent
ZILLOW_API_KEY = 'X1-ZWz195za60umff_728x4'


class ZillowAPI(object):
    """docstring for ZillowAPI."""
    def __init__(self, address, state ='SC'):
        super(ZillowAPI, self).__init__()
        self.address = address
        self.state = state
        self.zillow_data = {}
    def queryZillow(self, zillow_address):
        run_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+ZILLOW_API_KEY+zillow_address
        zillow_response = requests.get(run_url).content
        print zillow_response
        my_dict = xmltodict.parse(indent(zillow_response).encode('utf-8'))
        # If successful will response with "Request successfully processed"
        message = my_dict['SearchResults:searchresults']['message']
        print message
        if(message['text'] != 'Request successfully processed'):
            print ('Address not found: zillow_address:', zillow_address)
            return {}
        else:
            result = my_dict['SearchResults:searchresults']['response']['results']['result']
            zillow_data = {
                'zpid': result.get('zpid'),
                'latitude': result.get('address')['latitude'],
                'longitude': result.get('address')['longitude'],
                'taxAssessmentYear': result.get('taxAssessmentYear'),
                'taxAssessment': result.get('taxAssessment'),
                'yearBuilt': result.get('yearBuilt'),
                'lotSizeSqFt': result.get('lotSizeSqFt'),
                'bathrooms': result.get('bathrooms'),
                'bedrooms': result.get('bedrooms'),
                'lastSoldDate': result.get('lastSoldDate'),
                'lastSoldPrice': result.get('lastSoldPrice')['#text'],
                'zestimate': result.get('zestimate').get('amount').get('#text')

            }
            return zillow_data
