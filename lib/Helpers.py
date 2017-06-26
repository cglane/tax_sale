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
