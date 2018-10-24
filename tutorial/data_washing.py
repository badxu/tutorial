
import re


re_prourl = re.compile(r'.*categoryNum=\d{12}')#match project detail url
re_pronum = re.compile(r'\w{3}\-\d{2}\-\d{4}\-\d{4}')#match project number
re_proretime = re.compile(r'\d{4}\-\d{2}\-\d{2}')#match project release time
re_entqlurl = re.compile(r'.*\/showCompInfo\/.*') #match enter qulification url

def prourl_filter(li_0):
    url_list = [element for element in li_0 if re_prourl.match(element)!= None]
    return url_list
def pronumber_filter(li_1):
    pronumber_list = [re_pronum.findall(elem) for elem in li_1]
    return pronumber_list
def proretime_filter(li_2):
    proretime_list = [re_proretime.findall(elem) for elem in li_2]
    return proretime_list
def entqlurl_filter(li_entqlurl):
    entqlurl_list = [element for element in li_entqlurl if re_entqlurl.match(element)!= None]
    return entqlurl_list