import requests
import xmltodict, json
from collections import defaultdict
from yattag import indent


class ZillowAPI(object):
    """docstring for ZillowAPI."""
    def __init__(self, address, apiKey,  state ='SC'):
        super(ZillowAPI, self).__init__()
        self.address = address
        self.state = state
        self.apiKey = apiKey
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
        run_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+self.apiKey+self.address
        zillow_response = requests.get(run_url).content
        try:
            my_dict = xmltodict.parse(indent(zillow_response).encode('utf-8'))
        except Exception as e:
            print 'XMLparsing error'
            return False
        # If successful will response with "Request successfully processed"
        message = my_dict['SearchResults:searchresults']['message']
        if(message['text'] != 'Request successfully processed'):
            print message
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
                    'zestimate': result[0].get('zestimate').get('amount').get('#text')
                }
                try:
                    lastSoldPrice = result[0].get('lastSoldPrice')['#text']
                    zillow_data['lastSoldPrice'] = lastSoldPrice
                except Exception as e:
                    zillow_data['lastSoldPrice'] = ''
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
                    'zestimate': result.get('zestimate').get('amount').get('#text')
                }
                try:
                    lastSoldPrice = result.get('lastSoldPrice')['#text']
                    zillow_data['lastSoldPrice'] = lastSoldPrice
                except Exception as e:
                    zillow_data['lastSoldPrice'] = ''
            print 'Succesful call to Zillow'
            return zillow_data
