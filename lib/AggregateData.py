import csv
from lib.PropertyData import getPropertyInfo
from lib.Helpers import merge_two_dicts, formatAddressForZillow
from lib.zillowAPI import ZillowAPI


class AggregateData(object):
    """docstring for AggregateData."""
    def __init__(self, fileList, governmax_api_key):
        super(AggregateData, self).__init__()
        self.fileList = fileList
        self.governmax_api_key = governmax_api_key
    def readCSV(self, fileName):
        """Reads a csv file into dictionary."""
        csv_dict = csv.DictReader(open("../data/"+fileName+".csv"))
        return[x for x in csv_dict]
    def getZillowData(self, csvObj):
        """Queries Zillow and Governmax for data"""
        zillow_address = formatAddressForZillow(csvObj['address'])
        Zillow = ZillowAPI(zillow_address)
        return Zillow.queryZillow()
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
    def writeAndQuery(self, fileName, exportPath):
        "Read write and query."
        fileDict = [x for x in csv.DictReader(open('../data/'+fileName+'.csv'))]
        export_file_contents = [x for x in csv.DictReader(open(exportPath))]
        for itr, row in enumerate(fileDict):
            if not any(d['Pin'] == row['Pin'] for d in export_file_contents):
                zillow_data = self.getZillowData(row)
                merged_dict = merge_two_dicts(row, zillow_data)
                self.writeRowToFile(exportPath, merged_dict)
