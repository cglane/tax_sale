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
        self.zillow_dict = {
                'zpid': '',
                'latitude': '',
                'longitude': '',
                'taxAssessmentYear': '',
                'taxAssessment': '',
                'yearBuilt': '',
                'lotSizeSqFt': '',
                'bathrooms': '',
                'bedrooms': '',
                'lastSoldDate': '',
                'lastSoldPrice': '',
                'zestimate': ''
        }
    def queryZillow(self):
        if (not self.address):
            return self.zillow_dict
        run_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+ZILLOW_API_KEY+self.address
        zillow_response = requests.get(run_url).content
        my_dict = xmltodict.parse(indent(zillow_response).encode('utf-8'))
        # If successful will response with "Request successfully processed"
        message = my_dict['SearchResults:searchresults']['message']
        if(message['text'] != 'Request successfully processed'):
            print ('Address not found: zillow_address:', self.address)
            return self.zillow_dict
        else:
            result = my_dict['SearchResults:searchresults']['response']['results']['result']
            if(type(result) is list):
                zillow_data = {
                    'zpid': result[0].get('zpid'),
                    'latitude': result[0].get('address')['latitude'],
                    'longitude': result[0].get('address')['longitude'],
                    'taxAssessmentYear': result[0].get('taxAssessmentYear'),
                    'taxAssessment': result[0].get('taxAssessment'),
                    'yearBuilt': result[0].get('yearBuilt'),
                    'lotSizeSqFt': result[0].get('lotSizeSqFt'),
                    'bathrooms': result[0].get('bathrooms'),
                    'bedrooms': result[0].get('bedrooms'),
                    'lastSoldDate': result[0].get('lastSoldDate'),
                    'lastSoldPrice': result[0].get('lastSoldPrice')['#text'],
                    'zestimate': result[0].get('zestimate').get('amount').get('#text')
                }
            else:
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
