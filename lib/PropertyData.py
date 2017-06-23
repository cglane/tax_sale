from lib.CharlestonCounty import WebParser
from lib.zillowAPI import ZillowAPI
from lib.Helpers import merge_two_dicts

def getPropertyInfo(governmax_api_key, property_pin):
    web_parser = WebParser(property_pin)
    governmax_data = web_parser.getDataByPin(governmax_api_key)
    zillow_address = web_parser.formatAddressForZillow()
    zillow_api = ZillowAPI(zillow_address)
    zillow_results = zillow_api.queryZillow(zillow_address)

    return merge_two_dicts(zillow_results, governmax_data)
