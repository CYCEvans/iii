# 爬房仲網公用爬蟲模組
import datetime
import time
import json
import os
import re
import math
import random

import requests
from bs4 import BeautifulSoup



class RentCrawler():

    def __init__(self, url, links="", res="", soup=""):
        self.url = url
        self.links = links
        self.res = res
        self.soup = soup

    def connect(self, headers="",proxies=""):
        # 預設用get方法
        self.res = requests.get(self.url, headers=headers, proxies=proxies)
        self.res.encoding = "utf-8"
        self.soup = BeautifulSoup(self.res.text, "lxml")

    def close(self):
        self.res.close()

    def getTotalPage(self):
        pass

    def readOldLinks(self):
        oldLinks = []
        with open(self.links, 'r') as f:
            if f.readable():
                dataLinks = f.read().split(",")
                dataLinks.pop(-1)
                for link in dataLinks:
                    oldLinks.append(link)
        return oldLinks

    def extractUrls(self,oldLinks):
        pass

    def put_links(self, href, oldLinks, urls):
        if href not in oldLinks:
            urls.append(href)
        else:
            print("href %s exist" % (href))
            pass

    def savePages(self, fileName="data.txt"):
        dataDict = dict()
        dataDict["html"] = self.res.text
        dataDict["url"] = self.url
        today = datetime.date.today().strftime("%Y-%m-%d")
        dataDict["update"] = today
        with open(fileName, "w") as f:
            json.dump(dataDict, f)

    def saveLinks(self,linksList, fileName="data.txt"):
        with open(fileName, 'w+') as f:
            for link in linksList:
                if link is not "":
                    f.write(link + ",")


class SinyiCrawler(RentCrawler):

    def getTotalPage(self):
        pageNum = re.findall("計有(.*)筆", self.soup.select_one('h1').text)
        pageNum = int(pageNum[0].replace(",", ""))
        totalPages = math.ceil(pageNum / 20)
        return totalPages

    def extractUrls(self,oldLinks):
        urls = []
        try:
            for link in self.soup.select('a.name'):
                href = link['href']
                self.put_links( href, oldLinks, urls)
            return urls
        except Exception as e:
            self.close()
            print(e)


class HBHCrawler(RentCrawler):

    def getTotalPage(self):
        pagetext = re.sub("\\r|\\n|\/|<|!|-|>|", "", self.soup.select_one("script").text)
        totalPages = int(re.findall(r"^pageListFill\(\d*,(\d*)\)$", pagetext)[0])

        return totalPages

    def extractUrls(self, oldLinks):
        urls = []
        try:
            for link in self.soup.select("div.name > a"):
                href = "http://www.hbhousing.com.tw" + link["href"]
                self.put_links(href, oldLinks, urls)
            return urls
        except Exception as e:
            self.close()
            print(e)


class YCCrawler(RentCrawler):

    def __init__(self, url, links="", res="", soup="", data="", headers=""):
        super().__init__(url, links, res, soup)
        self.data = data
        self.headers = headers

    def connect_by_post(self):
        self.res = requests.post(self.url,data=self.data,headers=self.headers)
        self.res.encoding = "utf-8"
        self.soup = BeautifulSoup(self.res.text, "lxml")

    def getTotalPage(self):
        totalPages = int(self.soup.select_one('#hidTotalPages')["value"])

        return totalPages

    def extractUrls(self, oldLinks):
        urls = []
        try:
            for link in self.soup.select("div.house_block_content > h2 > a"):
                if "housefun" not in link["href"]:
                    href = "http://rent.yungching.com.tw"+link["href"]
                    self.put_links(href, oldLinks, urls)
            return urls
        except Exception as e:
            self.close()
            print(e)


class HFCrawler(YCCrawler):

    def extractUrls(self, oldLinks):
        urls = []
        try:
            for link in self.soup.select("div.house_block_content > h2 > a"):
                if "housefun" in link["href"]:
                    href = link["href"]
                    self.put_links(href, oldLinks, urls)
            return urls
        except Exception as e:
            self.close()
            print(e)
