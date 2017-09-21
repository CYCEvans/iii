import math
import re
import time

from splinter import Browser


def getPageNumber(browser):
    # 找出你要的頁面數(瀏覽器)
    # 找到Tag
    numTag = browser.find_by_css("h1.counter")[0]
    # 找到筆數
    numStr = re.findall(r"(\d+)筆", numTag.text)
    # 轉換成頁數
    pageNum = math.ceil(int(numStr[0]) / 20)
    return pageNum


def chooseCity(browser,city):
    cityList = browser.find_by_css("div#cityList")[0]
    cityTag = cityList.find_by_css("a[title={}]".format(city))
    cityTag.click()
    goPage = browser.find_by_css("input.submit")
    goPage.click()


def changePage(browser,page):
    pageTag = browser.find_by_css("div.paginate")[0]
    pageBtn = pageTag.find_by_xpath("//a[@title=' %d']"%(page))[0]
    pageBtn.click()


def getLink(browser):
    linkList = []
    links =browser.find_by_css("a.name")
    for link in links:
        linkList.append(link["href"])
    return linkList


#讀取資料(頁面數)
def saveLink(linkList,fileName = "data.txt"):
    with open(fileName, 'w') as f:
        for link in linkList:
            f.write(link+",")


def readLink(fileName = "data.txt"):
    data = []
    with open(fileName,'r') as f:
        dataLinks=f.read().split(",")
        for link in dataLinks:
            data.append(link)
    return data



def main():
    newLinks = []
    oldLinks = readLink("123Links.txt")
    executable_path = {'executable_path': r"D:\phantomjs\bin\phantomjs.exe"}
    browser = Browser('phantomjs', **executable_path)
    browser.visit("http://rent.sinyi.com.tw/")
    time.sleep(5)
    cityTag = browser.find_by_css("input#city")[0]
    cityTag.click()
    time.sleep(1)
    chooseCity(browser, "新北市")
    time.sleep(5)
    pageNum = getPageNumber(browser)

    for i in range(1,pageNum+1):
        time.sleep(1)
        tmpLinks = []
        if i == 1:
            tmpLinks = getLink(browser)
        else:
            changePage(browser,i)
            time.sleep(2)
            tmpLinks = getLink(browser)
        for tmpLink in tmpLinks:
            if tmpLink not in oldLinks:
                newLinks.append(tmpLink)

    oldLinks.extend(newLinks)
    saveLink(oldLinks,"Sinyi_NewTPE_Links.txt")

if __name__ == "__main__":
   main()
