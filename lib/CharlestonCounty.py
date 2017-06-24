import requests
import csv
from lib.Helpers import merge_two_dicts
import xmltodict, json
from bs4 import BeautifulSoup
Zillow_API_Key = 'X1-ZWz195za60umff_728x4'

class WebParser(object):
    """Parser getting property info in Charleston County Per Property Pin"""
    def __init__(self, governmax_api_key):
        super(WebParser, self).__init__()
        self.property_data = {}
        self.governmax_api_key = governmax_api_key
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

    def getDataByPin(self, propertyPin):
        tab_url = ("http://sc-charleston-county.governmax.com/"
                    "svc/tab_summary_report_SC-Char.asp?t_nm=summary"
                    "&l_cr=1&t_wc=|parcelid="+propertyPin+
                    "+++++++++++++++&sid="+self.governmax_api_key)
        request = requests.get(tab_url).content
        soup = BeautifulSoup(request, 'html.parser')
        list_data = soup.findAll("span", class_="listdata")
        font_data = soup.findAll('font')
        owner_address = font_data[28].get_text('', strip=True)
        if(len(list_data) < 1):
            print ('queryError for pin: ', propertyPin)
            return {'address': '', 'owner_address': '', 'property_code': ''}
        else:
            data = self.getOtherData(soup)
            self.property_data = {
                    'address': list_data[2].get_text('', strip=True),
                    'owner_address': " ".join(owner_address.split()),
                    'property_code': font_data[30].get_text('', strip=True)
            }
            print ('Query success for pin: ', propertyPin)
            return self.property_data
    def writeRowToFile(self, exportPath, data_dict):
        "Read file and write row"
        export_file_contents = [x for x in csv.reader(open(exportPath))]
        with open(exportPath, 'a') as export:
            writer = csv.DictWriter(export, fieldnames=data_dict.keys())
            if(len(export_file_contents) < 1):
                print ('Write Header')
                writer.writeheader()
                writer.writerow(data_dict)
            else:
                writer.writerow(data_dict)
            export.close()
    def writeAndQuery(self, fileName, exportPath):
        "Read write and query."
        fileDict = [x for x in csv.DictReader(open('../imports/'+fileName+'.csv'))]
        export_file_contents = [x for x in csv.DictReader(open(exportPath))]
        for itr, row in enumerate(fileDict):
            if not any(d['Pin'] == row['Pin'] for d in export_file_contents):
                governmax_data = self.getDataByPin(row['Pin'])
                governmax_data['auction_year'] = fileName
                merged_dict = merge_two_dicts(row, governmax_data)
                self.writeRowToFile(exportPath, merged_dict)
