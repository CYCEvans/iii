import concurrent.futures
import math
import re
import time

from rent import SinyiCrawler

city = "TPE"
if city =="TPE":
    cityNumber = 1
elif city =="NTP":
    cityNumber = 7

url = "http://rent.sinyi.com.tw/AJAX/ajax_searchItem.php?search=1&b={}&g=a_b_c_d&page=1".format(cityNumber)
links = "./Links/Sinyi_{}_Links.txt".format(city)


def saveData(iterObj):
    url,fileName = iterObj
    crawler = SinyiCrawler(url)
    crawler.connect()
    crawler.savePages(fileName)


def main():
    new_urls = []
    sycrawler = SinyiCrawler(url, links)
    sycrawler.connect()
    old_data = sycrawler.readOldLinks()
    fileNames = []
    page_num = sycrawler.getTotalPage()
    print("共{}頁".format(page_num))

    for i in range(1, page_num+1):
        iter_url = "http://rent.sinyi.com.tw/AJAX/ajax_searchItem.php?search=1&g=a_b_c_d&b={}&page={}".format(cityNumber,i)
        iter_crawler = SinyiCrawler(iter_url)
        iter_crawler.connect()
        new_urls.extend(iter_crawler.extractUrls(old_data))
        iter_crawler.close()

    print("獲取新連結總數{}".format(len(new_urls)))

    for new_url in new_urls:
        fileNo = re.findall(r"itemid=([A-Z]*\d+)", new_url)[0]
        fileNames.append(r'./data/sinyi/{}/{}.json'.format(city, fileNo))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        pageCotents = [executor.submit(saveData,iterObj) for iterObj in zip(new_urls, fileNames)]
        for future in concurrent.futures.as_completed(pageCotents):
            try:
                future.result()
            except Exception as e:
                print(e)

    old_data.extend(new_urls)
    sycrawler.saveLinks(old_data, links)
    sycrawler.close()

if __name__ == "__main__":
   main()
