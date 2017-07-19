import json
import math
import re
import time
# from collections import Counter
# from urllib.request import urlopen

from bs4 import BeautifulSoup
import requests

# 找出你要的頁面數(連結)
def getPageNumber(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    # 找到查詢的筆數
    numberReg = re.compile(r'(\d+ )筆')
    mo = numberReg.search(soup.select('ul > li.right')[0].text)
    pageNum = int(mo.group(1))
    totalPages = 150 if math.ceil(pageNum / 20) > 150 else math.ceil(pageNum / 20) # 除以20筆得出幾頁
    res.close()
    return totalPages
# 104 GET 連結 解析
# "order :1 相關性 2: 日期" cat: 2007001001~2007001012 軟體開發人才 , 2007002001~2007002008 網管人才
# keyword:{軟體設計工程師、大數據分析師、大數據工程師、資料分析師}
# "https://www.104.com.tw/jobbank/joblist/joblist.cfm?keyword=軟體設計工程師&jobsource=n104bank1&jobcat=2007001001&order=1&page="
# "https://www.104.com.tw/jobbank/joblist/joblist.cfm?keyword=軟體設計工程師&jobsource=n104bank1&jobcat=2007002001&order=1&page="

#讀取連結資料
def getPageLinks(href):
    linkList = []
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    jobList = soup.select("div.jobname_summary > a")
    for job in jobList:
        link = "https://www.104.com.tw" + job["href"]
        linkList.append(link)
    res.close()
    return linkList
def getJobInfo(href):
    jobInfo = dict()
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    # 將找到的資料放入dicrtionary
    jobInfo["title"] = soup.select_one("header > div > h1").contents[0].replace("\r\n", "").strip(" ")
    jobInfo["company"] = soup.select_one("a.cn").text
    jobInfo["content"] = soup.select_one("div.content > p").text.replace("\r", "").replace(" ", "")
    jobInfo["tools"] = soup.select("dd.tool")[0].text
    jobInfo["skills"] = soup.select("dd.tool")[1].text
    jobInfo["post_date"] = soup.select_one("time.update").text.split("：")[1]
    jobInfo["other_condition"] = soup.select("section.info")[1].select("dl > dd ")[-1].text.replace("\r","").replace(" ","")
    res.close()
    return jobInfo
def saveData(data,fileName = "data.json"):
    # 輸出成json檔
    with open(fileName, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    now = time.ctime()
    data = []
    start = 2007001000
    jobLink = []
    pageNum = []
    #得到所有軟體人才(jobcat2007001001-2007001012)有關的頁數
    for n in range(1, 13):
        start += 1
        herf = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?keyword=大數據工程師&jobsource=n104bank1&jobcat=" + str(start) + "&order=1&page="
        try:
            pages = getPageNumber(herf)
        except:
            pass
        pageNum.append(pages)
    # 得到所有軟體人才(jobcat2007001001-2007001012)的連結
    start = 2007001000
    for totalPages in pageNum:
        start += 1
        for num in range(1,totalPages+1):
            try:
                web = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?keyword=大數據工程師&jobsource=n104bank1&jobcat={}&order=1&page={}".format(start,num)
                jobLink.extend(getPageLinks(web))
                # time.sleep(1)
            except Exception as e:
                print("a")
                print(e)
                pass
    #改成set，去除重複連結
    jobLink = set(jobLink)
    # 透過連結得到所有軟體人才(jobcat2007001001-2007001012)的資料
    for link in jobLink:
        try:
            jobInfo = getJobInfo(link)
            data.append(jobInfo)
            time.sleep(3)
        except Exception as e:
            print("b")
            print(e)
            pass
    saveData(data,"104_Get_大數據工程師_cat2007001000All.json")
    end = time.ctime()
    print("開始時間%s" % (now))
    print("結束時間%s" % (end))