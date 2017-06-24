import csv
from lib.Helpers import merge_two_dicts, formatAddressForZillow
from lib.zillowAPI import ZillowAPI


class AggregateData(object):
    """docstring for AggregateData."""
    def __init__(self, fileName,  exportPath, zillowAPIKey):
        super(AggregateData, self).__init__()
        self.fileName = fileName
        self.exportPath = exportPath
        self.zillowAPIKey = zillowAPIKey
    def getZillowData(self, csvObj):
        """Queries Zillow and Governmax for data"""
        zillow_address = formatAddressForZillow(csvObj['address'])
        Zillow = ZillowAPI(zillow_address, self.zillowAPIKey)
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
            export.close()
    def writeAndQuery(self):
        "Read write and query."
        fileDict = [x for x in csv.DictReader(open('../data/'+self.fileName+'.csv'))]
        export_file_contents = [x for x in csv.DictReader(open(self.exportPath))]
        for itr, row in enumerate(fileDict):
            if not any(d['Pin'] == row['Pin'] for d in export_file_contents):
                zillow_data = self.getZillowData(row)
                if zillow_data:
                        "Don't write to file if xml parsing error"
                        merged_dict = merge_two_dicts(row, zillow_data)
                        self.writeRowToFile(self.exportPath, merged_dict)
