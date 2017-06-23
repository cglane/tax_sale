import csv
from lib.PropertyData import getPropertyInfo
from lib.Helpers import merge_two_dicts



class AggregateData(object):
    """docstring for AggregateData."""
    def __init__(self, fileList, governmax_api_key):
        super(AggregateData, self).__init__()
        self.fileList = fileList
        self.governmax_api_key = governmax_api_key
    def readCSV(self, fileName):
        """Reads a csv file into dictionary."""
        csv_dict = csv.DictReader(open("../imports/"+fileName+".csv"))
        return[x for x in csv_dict]
    def getZillowData(self, csvObj):
        """Queries Zillow and Governmax for data"""
        return getPropertyInfo(self.governmax_api_key, csvObj['Pin'])
    def buildDictionaryList(self, fileName):
        """Builds master dictionary list for all rows in file."""
        dictionary_list = []
        government_data = self.readCSV(fileName)
        for sub_dict in government_data:
            zillow_data = self.getZillowData(sub_dict)
            zillow_data['auction_year'] = fileName
            data_object = merge_two_dicts(sub_dict, zillow_data)
            dictionary_list.append(data_object)
        return dictionary_list
    def writeListToFile(self, listObjects):
        """Writes list of objects to File."""
        keys = listObjects[0].keys()
        with open('../data/dataFile.csv', 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(listObjects)
    def buildAndWrite(self):
        all_data = []
        for fileName in self.fileList:
            data_list = self.buildDictionaryList(fileName)
            all_data.append(data_list)
        flat_list = [item for sublist in all_data for item in sublist]
        self.writeListToFile(flat_list)
