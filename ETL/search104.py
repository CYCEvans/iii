import json
from collections import Counter
from urllib.request import urlopen

def getPageNumber(web):
    html = urlopen(web)
    jsonObj = json.load(html)
    num = jsonObj.get("TOTALPAGE")
    return num

def getData(pagenum):
    result = Counter()
    for n in range(1,pagenum+1):
        web = "http://www.104.com.tw/i/apis/jobsearch.cfm?cat=2007001004&fmt=8&page={}&pgsz=200&cols=PCSKILL_ALL_DESC".format(n)
        html = urlopen(web)
        jsonObj = json.load(html)
        lst = jsonObj.get("data")
        for obj in lst:
            if not (obj == {} or obj['PCSKILL_ALL_DESC'] == ''):
                lstB = obj['PCSKILL_ALL_DESC'].split(" ")
                for objB in lstB:
                    result[objB] +=1
    return result
num = int(getPageNumber("http://www.104.com.tw/i/apis/jobsearch.cfm?cat=2007001004&fmt=8&page=1&pgsz=200&cols=PCSKILL_ALL_DESC"))
print(num)
print(getData(num).most_common(20))
