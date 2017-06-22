import requests
import xmltodict, json
from bs4 import BeautifulSoup
import re
from mechanize import Browser

def getOtherData(soup):
    data = []
    font_tags = soup.findAll('tr')
    for itr, tr in enumerate(font_tags):
        for td in tr.findAll('td'):
            font_tags = td.findAll('font')
            for fontItr, font in enumerate(td.findAll('font')):
                data.append(font.get_text())
    return data


def getDataByPin(parcelId, apiKey):
    tab_url = "http://sc-charleston-county.governmax.com/svc/tab_summary_report_SC-Char.asp?t_nm=summary&l_cr=1&t_wc=|parcelid="+parcelId+"+++++++++++++++&sid="+apiKey
    request = requests.get(tab_url).content
    soup = BeautifulSoup(request, 'html.parser')
    list_data = soup.findAll("span", class_="listdata")
    font_data = soup.findAll('font')
    if(len(list_data) < 1):
        print 'apiKey out of date'
        return {}
    else:
        data = getOtherData(soup)
        property_fields = {
                'address' : list_data[2].get_text(),
                'owner_address' : font_data[33].get_text(),
        }
        return property_fields

def formatAddressForZillow(address, stateCode):
        address_list = address.split(',')
        zillow_address = '+'.join(address_list[0].split(' '))
        zillow_city = ''.join(address_list[1].split(' '))
        return '&address='+zillow_address+'&citystatezip='+zillow_city+'%2C+'+stateCode

def queryZillow(address, state='SC'):
    API_KEY = 'X1-ZWz195za60umff_728x4'
    zillow_address = formatAddressForZillow(address, state)
    print zillow_address
    run_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+API_KEY+zillow_address
    print run_url
    my_dict = xmltodict.parse(requests.get(run_url).content)
    # If successful will response with "Request successfully processed"
    message = my_dict['SearchResults:searchresults']['message']
    print message
    result = my_dict['SearchResults:searchresults']['response']['results']['result']
    text_file = open("Output.txt", "w")
    for key in result.keys():
        print (key, result[key])
        text_file.write(key + ',' + str(result[key])+ '\n')
    text_file.close()
    test_url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+API_KEY+"&address=0+Bigelow+Ave&citystatezip=Seattle%2C+WA"

county_data_dict = getDataByPin('7641400090', 'DA36B3DADD854B599C5C23402CCEFD7E')
queryZillow(county_data_dict['address'])
