import requests
from xml.etree import ElementTree as ET
import xmltodict, json


API_KEY = 'X1-ZWz195za60umff_728x4'

test_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+API_KEY+"&address=0+Bigelow+Ave&citystatezip=Seattle%2C+WA"


my_dict = xmltodict.parse(requests.get(test_url).content)
# If successful will response with "Request successfully processed"
message = my_dict['SearchResults:searchresults']['message']

result = my_dict['SearchResults:searchresults']['response']['results']['result']
text_file = open("Output.txt", "w")
for key in result.keys():
    print (key, result[key])
    text_file.write(key + ',' + str(result[key])+ '\n')
text_file.close()


##TODO
'Filter out if tax assesment earlier than auction date'
'Convert useCode to an index'
