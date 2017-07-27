import json
import re
import time
import concurrent.futures

from lxml import html
from bs4 import BeautifulSoup
import requests

# 分割出post格式
def str2dict(data_str):
    data = {}
    for row in data_str.split('\n'):
        kv_list = row.split(":")
        data[kv_list[0]] = kv_list[1]
    return data

#找出你要的頁面數(連結)
def getPageNumber(href,data,headers):
    res = requests.post(href, data=data, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    pageContent = soup.select_one("div#top_title > table > tbody > tr > td[align]").text
    numberReg = re.compile(r'(\d+)頁')
    mo = numberReg.search(pageContent)
    pageNum = int(mo.group(1))
    res.close()
    return pageNum

#讀取資料(連結)
def getPageLinks(href,data,headers):
    linkList = []
    res = requests.post(href, data=data, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    jobList = soup.select("a.jobname")
    for job in jobList:
        link = "https://www.yes123.com.tw/admin/" + job["href"]
        linkList.append(link)
    res.close()
    return linkList

def getJobInfo(href,headers):
    jobInfo = dict()
    res = requests.get(href, headers=headers)

    soup = BeautifulSoup(res.text, 'lxml')
    tree = html.fromstring(res.content)

    jobInfo["title"] = soup.select_one("div.jobname_title").contents[0]
    jobInfo["company"] = soup.select_one("div.jobname_title > p > a").text
    jobInfo["content"] = soup.select_one("div.rr_box").text

    date = tree.xpath("//span[contains(text(), '職缺更新 ： ')]/following-sibling::span")
    jobInfo["post_date"] = date[0].text.replace("\xa0", "")

    skilltag = tree.xpath("//h2[contains(text(), '技能與求職專')]/following-sibling::ul / child::li /child ::span[@class='rr']")
    if skilltag != []:
        skills = skilltag[0].text_content()
        skills = re.sub("\n+|\r|／|：| +", " ", skills)
        skills = bytes(skills, "utf-8")
        skills = skills.decode("ascii", "ignore")
        skills.replace("Visual C++", "VisualC++")
        jobInfo["skills"] = skills
    else:
        jobInfo["skills"] = ""
    other_tag = tree.xpath("//h2[contains(text(), '其他條件')]/following-sibling::ul/child ::li")
    if other_tag != []:
        other_conition = other_tag[0].text_content()
        jobInfo["other_condition"] = other_conition
    else:
        jobInfo["other_condition"] = ""
    res.close()
    return jobInfo

def saveData(data,fileName = "data.json"):
    with open(fileName, 'w') as f:
        json.dump(data, f)

def saveLink(dataLinks,fileName = "data.txt"):
    with open(fileName, 'w') as f:
        for link in dataLinks:
            f.write(link+",")

def readLink(fileName = "data.txt"):
    data = []
    with open(fileName,'r') as f:
        dataLinks=f.read().split(",")
        for link in dataLinks:
            data.append(link)
    return data

if __name__ == "__main__":
    start = time.time()
    # post的資料
    params_str = '''find_key1:軟體
    search_work:職務
    search_type:job
    search_item:1
    search_from:index'''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    params = str2dict(params_str)
    params["strrec"] = 0
    data = []
    # 讀取檔案，找出舊的連結
    oldLinks = readLink("123Links.txt")
    newLinks = []
    # 得到所有有關的頁數
    href = "https://www.yes123.com.tw/admin/job_refer_list.asp"
    pageNum = getPageNumber(href, params, headers)
    # 得到所有的連結，比對舊連結，如有新的加入新連結
    for num in range(0,pageNum):
        params["strrec"] = num*20
        # 取得每一頁的連結
        tmpLinks = getPageLinks(href, params, headers)

        try:
            for tmpLink in tmpLinks:
                if tmpLink not in oldLinks:
                    newLinks.append(tmpLink)
        except Exception as e:
            print("a")
            print(e)
            pass
    print("新的連結共 %d個" % len(newLinks))
    mid = time.time()
    # 只爬新連結資料，用多緒程(5人)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        jobInfo = [executor.submit(getJobInfo, url,headers) for url in newLinks]
        for future in concurrent.futures.as_completed(jobInfo):
            try:
                finalData = future.result()
                data.append(finalData)
            except Exception as e:
                print(e)
                print("zzz")
                pass

    end = time.time()
    print("-----------------")
    print("爬連結時間 %d 秒" % (mid - start))
    print("爬蟲總時間 %d 秒" % (end - start))
    oldLinks.extend(newLinks)
    saveData(oldLinks, fileName="123Links.txt")
    fileName = "123軟體ByPostMP.json"
    saveData(data,fileName)

