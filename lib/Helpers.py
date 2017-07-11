import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
def formatAddressForZillow(address, stateCode='SC'):
    if(address):
        address_list = address.split(',')
        zillow_address = '+'.join(address_list[0].split(' '))
        zillow_city = ''.join(address_list[1].split(' '))
        return ('&address='+zillow_address+'&citystatezip='+zillow_city+'%2C+'+stateCode)
def stripWhiteSpace(string):
    str_arr = string.split(' ')
    clean_arr = list(filter(None, str_arr))
    return " ".join(clean_arr)

def returnObjInList(key, val, arr):
    for obj in arr:
        if(obj[key] == val):
            return obj
    return arr[0]
def currencyToFloat(value):
    try:
        newVal = value.replace(' ', '').strip('$').replace(',', '')
        print newVal
        return locale.atof(newVal)
    except Exception as e:
        return 0
def stringToFloat(value):
    try:
        return locale.atof(value.replace(',', ''))
    except Exception as e:
        return 0.0
def propTypeObject(classCode):
    property_code_dict = {'742 - HOA-PROP': 21, '700 - SPCLTY-HTL': 24, '580 - SPCLTY-RST': 16, '650 - SPCLTY-OFC': 28, '800 - AGRICULTURAL': 15, '200 - SPCLTY-APT': 1, '451 - ROAD-ROW': 19, '121 - GROUP-LIV': 27, '990 - UNDEVELOPABLE': 5, '905 - VAC-RES-LOT': 0, '952 - VAC-COMM-LOT': 3, '630 - SPCLTY-WHS': 22, '130 - RESID-DUP/TRI': 9, '250 - SPCLTY-COMMCONDO': 14, '110 - RESID-MBH': 10, '120 - RESID-TWH': 4, '460 - AUTO-PARKING': 6, '500 - General Commercial': 2, '900 - RES-DEV-ACRS': 13, '101 - RESID-SFR': 7, '530 - SPCLTY-RTL': 20, '140 - MH-PARKS': 17, '304 - MFG/INDUST': 25, '750 - SPCLTY-REC': 11, '910 - COM-DEV-ACRS': 18, '195 - COMM-APP-RES': 26, '210 - SPCLTY-SMA': 8, '691 - RELIGIOUS': 23, '160 - RESID-CNU': 12}
    try:
        return property_code_dict[classCode]
    except Exception as e:
        print e
        return 0
def setLabel(value):
    if value == 'DEED':
        print value
        return 1.0
    return 0.0
