import requests
import xmltodict, json
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
        my_dict = xmltodict.parse(requests.get(run_url).content)
        # If successful will response with "Request successfully processed"
        message = my_dict['SearchResults:searchresults']['message']
        if(message == 'Request successfully processed'):
            result = my_dict['SearchResults:searchresults']['response']['results']['result']
        else:
            result = my_dict['SearchResults:searchresults']['response']['results']['result']
            self.zillow_data = {
            'zpid': result['zpid'],
            'latitude': result['address']['latitude'],
            'longitude': result['address']['longitude'],
            'useCode': result['useCode'],
            'taxAssesmentYear': result['taxAssesmentYear'],
            'taxAssesment': result['taxAssesment'],
            'yearBuilt': result['yearBuilt'],
            'lotSizeSqFt': result['lotSizeSqFt'],
            'bathrooms': result['bathrooms'],
            'bedrooms': result['bedrooms'],
            'lastSoldDate': result['lastSoldDate'],
            'lastSoldPrice': result['lastSoldPrice']['#text'],
            'zestimate': result['zestimate']['#text']
            }
            return self.zillow_data
