import json
from collections import Counter
from urllib.request import urlopen
#找出你要的頁面數
def getPageNumber(web):
    html = urlopen(web)
    jsonObj = json.load(html)
    # 得到key為TOTALPAGE的總頁數(字串)
    num = jsonObj.get("TOTALPAGE")
    return num
#讀取資料(頁面數)
def getData(pagenum):
    result = Counter()
    #迭代所有頁數
    for n in range(1,pagenum+1):
        #api網址:cat職位名稱 page={} PCSKILL_ALL_DESC:電腦技術
        web = "http://www.104.com.tw/i/apis/jobsearch.cfm?cat=2007001004&fmt=8&page={}&pgsz=200&cols=PCSKILL_ALL_DESC".format(n)
        #得到json格式的文字檔
        html = urlopen(web)
        #得到json物件
        jsonObj = json.load(html)
        #得到key為data的list
        lst = jsonObj.get("data")
        for obj in lst:
            #排除list中物件為{}或是電腦技術沒有的物件
            if not (obj == {} or obj['PCSKILL_ALL_DESC'] == ''):
                #電腦技術全部小寫後切片，加入Counter計數
                lstB = obj['PCSKILL_ALL_DESC'].lower().split(" ")
                for objB in lstB:
                    result[objB] +=1
    return result
if __name__ == "__main__":
    num = int(getPageNumber("http://www.104.com.tw/i/apis/jobsearch.cfm?cat=2007001004&fmt=8&page=1&pgsz=200&cols=PCSKILL_ALL_DESC"))
    print(num)
    print(getData(num).most_common(20))
