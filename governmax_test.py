import requests
from bs4 import BeautifulSoup
from lib.CharlestonCounty import WebParser
Govermax_API_KEY = 'FEF8EC5AED114482874581334CADB4C8'
property_pin = '4580901002'

tab_url = ("http://sc-charleston-county.governmax.com/"
            "svc/tab_summary_report_SC-Char.asp?t_nm=summary"
            "&l_cr=1&t_wc=|parcelid="+property_pin+
            "+++++++++++++++&sid="+Govermax_API_KEY)
request = requests.get(tab_url).content
soup = BeautifulSoup(request, 'html.parser')
tables = soup.findAll('table')[2].findAll('table')[5].findAll('table')
first_table = tables[0]
all_tr = first_table.findAll('tr')

'Fist Table'
first_header = [x.get_text('', strip=True) for x in all_tr[0].findAll('span')]
first_header_data = [x.get_text('', strip=True) for x in all_tr[1].findAll('span')]
first_dict = dict(zip(first_header, first_header_data))
'Second Table'
owner_class_table = tables[3]
owner_values_fields = [x.get_text('', strip=True) for x in owner_class_table.findAll('font')]
owner_dict = dict(zip(*[iter(owner_values_fields)] * 2))
'Fourth Class'
property_info_table = tables[4]
property_fields_values = [x.get_text('', strip=True) for x in property_info_table.findAll('font')]
property_class_dict = dict(zip(*[iter(property_fields_values)] * 2))
'Historic Information'
historic_info_table = tables[7]
historic_fields = [x.get_text('', strip=True) for x in historic_info_table.findAll("span", class_="datalabel")]
historic_info_list = [[p.get_text('', strip=True) for p in x.findAll('span')] for x in historic_info_table.findAll('tr')[1:]]
historic_info_dict_list = [dict(zip(historic_fields, x)) for x in historic_info_list]
'Sales Disclosure'
sales_disclosure_table = tables[9]
sales_disclosure_fields = [x.get_text('', strip=True) for x in sales_disclosure_table.findAll("span", class_="datalabel")]
sales_disclosure_info_list = [[p.get_text('', strip=True) for p in x.findAll('font')] for x in sales_disclosure_table.findAll('tr')[1:]]
sales_disclosure_dict_list = [dict(zip(sales_disclosure_fields, x)) for x in sales_disclosure_info_list]
'Improvements'
improvements_table = tables[10]
improvements_fields = [x.get_text('', strip=True) for x in improvements_table.findAll("span", class_="datalabel")]
improvements_values = [[p.get_text('', strip=True) for p in x.findAll('font')] for x in improvements_table.findAll('tr')[2:]]
improvements_dict_list = [dict(zip(improvements_fields, x)) for x in improvements_values]
