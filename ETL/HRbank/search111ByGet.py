import json
import re
import time

from lxml import html
from bs4 import BeautifulSoup
import requests

#找出你要的頁面數(連結)
def getPageNumber(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    numberReg = re.compile(r'(\d+) 頁')
    mo = numberReg.search(soup.select_one("div.pagedata").text)
    pageNum = int(mo.group(1))
    res.close()
    return pageNum
# 1111 Get 網址 連結解析:
# si :1 找工作 2: 找公司, ps:頁數 , d0: 140201~140213 軟體開發人才 140301~140306 系統人才 ,140401~140405 網管人才
# col= ab 以相關性來排列,da 以日期排列,
# ks:{軟體設計工程師、大數據分析師、大數據工程師、資料分析師} 關鍵字
# https://www.1111.com.tw/job-bank/job-index.asp?si=1&ps=100&ks=軟體設計工程師&d0=140200,140300,140400&page=
#讀取資料(連結)
def getPageLinks(href):
    linkList = []
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    jobList = soup.select("div.jbInfo > div > h3 > a")
    for job in jobList:
        link = "http:" + job["href"]
        linkList.append(link)
    res.close()
    return linkList
def getJobInfo(href):
    jobInfo = dict()
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    tree = html.fromstring(res.content)
    jobInfo["title"] = soup.select_one("h1").contents[0]
    jobInfo["company"] = soup.select_one("li.ellipsis").text
    jobInfo["content"] = soup.select_one("li.paddingLB").text.replace("\xa0", "")
    dateReg = re.compile(r'：(\d+\/\d+\/\d+)')
    mo2 = dateReg.search(soup.select_one("span.update").text)
    jobInfo["post_date"] = mo2.group(1)
    skills = tree.xpath("//div[contains(text(), '電腦專長：')]/following-sibling::div")
    if skills != []:
        jobInfo["skills"] = skills[0].text
    else:
        jobInfo["skills"] = ""
    other_condition_tag = tree.xpath("//div[contains(text(), '附加條件：')]/following-sibling::div")
    if other_condition_tag != []:
        other_condition = "".join([one.text for one in other_condition_tag[0]])
        jobInfo["other_condition"] = other_condition.replace("\xa0", "").replace("\u3000", "")
    else:
        jobInfo["other_condition"] = ""
    res.close()
    return jobInfo
def saveData(data,fileName = "data.json"):
    with open(fileName, 'w') as f:
        json.dump(data, f)
if __name__ == "__main__":
    # 輸入關鍵字
    keywordList = ["JAVA","PYTHON","大數據","SQL","PHP","HADOOP"]
    for keyword in keywordList:
        now = time.ctime()
        data = []
        jobLink = []
        # 得到所有軟體人才、網管人才、系統人才(d0:140200、140300、140400)有關的頁數
        href = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ps=100&ks={}&d0=140200,140300,140400&page=1".format(keyword)
        pageNum = getPageNumber(href)
        # 得到所有軟體人才、網管人才、系統人才(d0:140200、140300、140400)的連結
        for num in range(1,pageNum+1):
            try:
                web = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ps=100&ks={}&d0=140200,140300,140400&page={}".format(keyword,num)
                jobLink.extend(getPageLinks(web))
                 # time.sleep(1)
            except Exception as e:
                print("a")
                print(e)
                pass
        #改成set，去除重複連結
        jobLink = set(jobLink)
        # 透過連結得到所有軟體人才、網管人才、系統人才(d0:140200、140300、140400)的資料
        for link in jobLink:
            try:
                jobInfo = getJobInfo(link)
                data.append(jobInfo)
                time.sleep(3)
            except Exception as e:
                print("b")
                print(e)
                pass
        fileName = "518_Get_{}_ab2032001.json".format(keyword)
        saveData(data,fileName)
        end = time.ctime()
        print("%s抓取開始時間%s" % (keyword,now))
        print("%s抓取開始時間%s" % (keyword,end))