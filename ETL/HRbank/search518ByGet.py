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
    numberReg = re.compile(r'(\d+)頁')
    mo = numberReg.search(soup.select_one("div#linkpage > span.pagecountnum").text)
    pageNum = int(mo.group(1))
    res.close()
    return pageNum
# 518 Get 網址 連結解析:
# ab = 職業類別 2032001 軟體類別 ad = Keyword ,  {軟體設計工程師、大數據分析師、大數據工程師、資料分析師} 關鍵字
# https://www.518.com.tw/job-index-P-{}.html?ad=軟體設計工程師&ab=2032001
#讀取資料(連結)
def getPageLinks(href):
    linkList = []
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    jobList = soup.select("li.title > a")
    for job in jobList:
        linkList.append(job["href"])
    res.close()
    return linkList
def getJobInfo(href):
    jobInfo = dict()
    res = requests.get(href)
    soup = BeautifulSoup(res.text, 'lxml')
    tree = html.fromstring(res.content)
    jobInfo["title"] = soup.select_one(".job-title").text
    jobInfo["company"] = soup.select_one("h3 > a")["title"]
    jobInfo["content"] = soup.select_one("div.JobDescription").text.replace("\n", "").replace("\r", "")
    jobInfo["post_date"] = soup.select_one("time").text.split(":")[1]
    jobInfo["tools"] = tree.xpath("//dt[contains(text(), '擅長工具：')]/following-sibling::dd")[0].text
    jobInfo["skills"] = tree.xpath("//dt[contains(text(), '工作技能：')]/following-sibling::dd")[0].text
    jobInfo["other_condition"] = tree.xpath("//dt[contains(text(), '其他條件：')]/following-sibling::dd")[0].text
    res.close()
    return jobInfo
def saveData(data,fileName = "data.json"):
    with open(fileName, 'w') as f:
        json.dump(data, f)
if __name__ == "__main__":
    # 輸入關鍵字
    keywordList = ["Python","HADOOP","Spark","PHP","Linux"]
    for keyword in keywordList:
        now = time.ctime()
        data = []
        jobLink = []
        # 得到所有軟體人才(ab:2032001)有關的頁數
        href = "https://www.518.com.tw/job-index-P-1.html?ad={}&ab=2032001".format(keyword)
        pageNum = getPageNumber(href)
        # 得到所有軟體人才、網管人才、系統人才(d0:140200、140300、140400)的連結
        for num in range(1,pageNum+1):
            try:
                web = "https://www.518.com.tw/job-index-P-{}.html?ad={}&ab=2032001".format(num,keyword)
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
        print("%s抓取結束時間%s" % (keyword,end))