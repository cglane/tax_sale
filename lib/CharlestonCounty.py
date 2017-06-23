import requests
import xmltodict, json
from bs4 import BeautifulSoup
Zillow_API_Key = 'X1-ZWz195za60umff_728x4'

class WebParser(object):
    """Parser getting property info in Charleston County Per Property Pin"""
    def __init__(self, propertyPin):
        super(WebParser, self).__init__()
        self.property_data = {}
        self.propertyPin = propertyPin
        self.zillowAddressQuery = ''
    def getOtherData(self, soup):
        data = []
        font_tags = soup.findAll('tr')
        for tr in font_tags:
            for td in tr.findAll('td'):
                font_tags = td.findAll('font')
                for font in td.findAll('font'):
                    data.append(font.get_text())
        return data

    def getDataByPin(self, apiKey):
        tab_url = ("http://sc-charleston-county.governmax.com/"
                    "svc/tab_summary_report_SC-Char.asp?t_nm=summary"
                    "&l_cr=1&t_wc=|parcelid="+self.propertyPin+
                    "+++++++++++++++&sid="+apiKey)
        request = requests.get(tab_url).content
        soup = BeautifulSoup(request, 'html.parser')
        list_data = soup.findAll("span", class_="listdata")
        font_data = soup.findAll('font')
        if(len(list_data) < 1):
            print 'apiKey out of date'
            return {}
        else:
            data = self.getOtherData(soup)
            owner_address = font_data[33].get_text('', strip=True)
            self.property_data = {
                    'address': list_data[2].get_text('', strip=True),
                    'owner_address': " ".join(owner_address.split()),
                    'property_code': font_data[35].get_text('', strip=True)
            }
            return self.property_data

    def formatAddressForZillow(self, stateCode='SC'):
        address_list = self.property_data['address'].split(',')
        zillow_address = '+'.join(address_list[0].split(' '))
        zillow_city = ''.join(address_list[1].split(' '))
        return ('&address='+zillow_address+'&citystatezip='+zillow_city+'%2C+'+stateCode)
