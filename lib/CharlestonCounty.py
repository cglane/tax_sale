import requests
import csv
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
from lib.Helpers import merge_two_dicts
from lib.Helpers import stripWhiteSpace
from lib.Helpers import returnObjInList
from lib.GoogleAPI import LocationData
import xmltodict, json
from bs4 import BeautifulSoup
Zillow_API_Key = 'X1-ZWz195za60umff_728x4'


def lowestSalesValue(salesObjects):
    if len(salesObjects) > 0:
        salesData = [x['Sale Price'].strip('$') for x in salesObjects]
        return min([locale.atof(x) for x in salesData])
    return None


def highestSalesPrice(salesObjects):
    if len(salesObjects) > 0:
        salesData = [x['Sale Price'].strip('$') for x in salesObjects]
        return max([locale.atof(x) for x in salesData])
    return None


def lastSalesPrice(salesObjects):
    if(len(salesObjects) > 0):
        salesData = [x['Sale Price'].strip('$') for x in salesObjects]
        return locale.atof(salesData[0])
    return None

class WebParser(object):
    """Parser getting property info in Charleston County Per Property Pin"""
    def __init__(self, governmax_api_key):
        super(WebParser, self).__init__()
        self.property_data = {}
        self.governmax_api_key = governmax_api_key
        self.tables = {}
    def getSoup(self, property_pin):
        """Gets Soup Object from Governmax."""
        tab_url = ("http://sc-charleston-county.governmax.com/"
                   "svc/tab_summary_report_SC-Char.asp?t_nm=summary"
                   "&l_cr=1&t_wc=|parcelid="+property_pin+
                   "+++++++++++++++&sid="+self.governmax_api_key)
        request = requests.get(tab_url).content
        soup = BeautifulSoup(request, 'html.parser')
        self.tables = soup.findAll('table')[2].findAll('table')[5].findAll('table')
    def getOverview(self):
        """Gets overview table from governmax as dictionary"""
        first_table = self.tables[0]
        all_tr = first_table.findAll('tr')
        first_header = [x.get_text('', strip=True) for x in all_tr[0].findAll('span')]
        first_header_data = [x.get_text('', strip=True) for x in all_tr[1].findAll('span')]
        return dict(zip(first_header, first_header_data))
    def getCurrentParcelInfo(self):
        """Gets second table information s an object."""
        'Second Table'
        owner_class_table = self.tables[3]
        owner_values_fields = [stripWhiteSpace(x.get_text('', strip=True)) for x in owner_class_table.findAll('font')]
        owner_dict = dict(zip(*[iter(owner_values_fields)] * 2))
        'Fourth Class'
        property_info_table = self.tables[4]
        property_fields_values = [stripWhiteSpace(x.get_text('', strip=True)) for x in property_info_table.findAll('font')]
        property_class_dict = dict(zip(*[iter(property_fields_values)] * 2))
        return merge_two_dicts(owner_dict, property_class_dict)
    def getHistoricInformation(self):
        """This gets historic information table as array of dictionaries."""
        historic_info_table = self.tables[7]
        historic_fields = [x.get_text('', strip=True) for x in historic_info_table.findAll("span", class_="datalabel")]
        historic_data =  historic_info_table.findAll('tr')[1:]
        historic_info_list = [[stripWhiteSpace(p.get_text('', strip=True)) for p in x.findAll('span')] for x in historic_data]
        if (len(historic_info_list) > 0):
            return [dict(zip(historic_fields, x)) for x in historic_info_list]
        return [dict.fromkeys(historic_fields)]
    def getSalesDisclosure(self):
        """This gets sales disclosure table as array of dictionaries."""
        sales_disclosure_table = self.tables[9]
        sales_disclosure_fields = [x.get_text('', strip=True) for x in sales_disclosure_table.findAll("span", class_="datalabel")]
        sales_disclosure_data = sales_disclosure_table.findAll('tr')[1:]
        sales_disclosure_info_list = [[stripWhiteSpace(p.get_text('', strip=True)) for p in x.findAll('font')] for x in sales_disclosure_data]
        if(len(sales_disclosure_info_list) > 0):
            return [dict(zip(sales_disclosure_fields, x)) for x in sales_disclosure_info_list]
        return [dict.fromkeys(sales_disclosure_fields)]
    def getImprovements(self):
        """Get improvements table as dictionary"""
        improvements_table = self.tables[10]
        improvements_fields = [x.get_text('', strip=True) for x in improvements_table.findAll("span", class_="datalabel")]
        improvements_data = improvements_table.findAll('tr')[2:]
        improvements_values = [[stripWhiteSpace(p.get_text('', strip=True)) for p in x.findAll('font')] for x in improvements_data]
        if(len(improvements_values) > 0):
            return [dict(zip(improvements_fields, x)) for x in improvements_values]
        return [dict.fromkeys(improvements_fields)]

    def aggregateData(self, year):
        """Aggregate Data from all tables."""
        if(self.tables):
            overview = self.getOverview()
            current_parcel = self.getCurrentParcelInfo()
            historic_info = self.getHistoricInformation()
            sales_disclosure = self.getSalesDisclosure()
            improvements = self.getImprovements()
            'Set rtrnData'
            rtrnData = merge_two_dicts(overview, current_parcel)
            rtrnData = merge_two_dicts(rtrnData, returnObjInList('Tax Year', year, historic_info))
            rtrnData = merge_two_dicts(rtrnData, improvements[0])
            rtrnData['lastSalesPrice'] = lastSalesPrice(sales_disclosure)
            rtrnData['lowestSalesValue'] = lowestSalesValue(sales_disclosure)
            rtrnData['highestSalesPrice'] = highestSalesPrice(sales_disclosure)
            return rtrnData
        else:
            print 'Error Parsing Data, possibly out of data api_key'
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
        google_api = LocationData()
        faulty_pins = []
        for itr, row in enumerate(fileDict):
            if not any(d['Pin'] == row['Pin'] for d in export_file_contents):
                try:
                    self.getSoup(row['Pin'])
                    print row['Pin']
                    governmax_data = self.aggregateData(fileName)
                    governmax_data['auction_year'] = fileName
                    latLng = google_api.getLatLong(governmax_data['Parcel Address'])
                    government_data = merge_two_dicts(row, governmax_data)
                    google_and_gov = merge_two_dicts(government_data, latLng)
                    self.writeRowToFile(exportPath, google_and_gov)
                    print ('Success with pin', row['Pin'])
                except Exception as e:
                    print e
                    faulty_pins.append(row['Pin'])
                    print ('Error with pin:', row['Pin'])
        print (faulty_pins)
