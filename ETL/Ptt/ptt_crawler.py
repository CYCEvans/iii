import concurrent.futures
import re
import os
import json
import time

import requests
from bs4 import BeautifulSoup
from lxml import html

# headers={"cookie": "over18=1;"}
# proxies = ""


def connect(url, headers={"cookie": "over18=1;"}, proxies=""):
    res = requests.get(url, headers=headers, proxies=proxies)
    return res


def get_total_page(url_index_page):
    res = connect(url_index_page)
    tree = html.fromstring(res.content)
    num_tag = tree.xpath('//a[contains(text(),"‹ 上頁")]')[0]
    num_text = num_tag.attrib["href"]
    total_pages = int(re.findall(r'index(\d+)', num_text)[0])
    res.close()
    return total_pages


def extract_comments(tree, comment_type):
    comments_list = tree.xpath("//span[text()='{}']/following-sibling::span[@class='f3 push-content']"
                               .format(comment_type))
    return comments_list


def content_crawler(page_num, board, keyword="all"):
    # 將一頁爬下來

    url = "https://www.ptt.cc/bbs/{}/index{}.html".format(board, page_num)
    res = connect(url)
    soup = BeautifulSoup(res.text, "lxml")
    raw_links = soup.select('div.r-ent')
    # 找到每個文章的區塊
    for raw_link in raw_links:
        try:
            # 先得到每篇文章的篇url
            link = "https://www.ptt.cc" + raw_link.select("a")[0]["href"]
            if link:
                # 確定得到url再去抓
                title = raw_link.select_one("div.title").text.strip()
                if title == keyword or keyword == "all":
                    date = raw_link.select_one("div.date").text.replace("/", "-").strip()
                    author = raw_link.select_one("div.author").text
                    ID = re.findall(r".*\/(.+)\.html", link)[0]
                    rate_text = raw_link.select_one("div.nrec").text
                    if rate_text:
                        if rate_text.startswith('爆'):
                            rate = 100
                        elif rate_text.startswith('X'):
                            rate = -1 * int(rate_text[1])
                        else:
                            rate = int(rate_text)
                    else:
                        rate = 0
                        # 比對推文數
                    # 連入聯結擷取文章內容
                    res_in = connect(link)
                    soup_in = BeautifulSoup(res_in.text, "lxml")
                    tree_in = html.fromstring(res_in.text)
                    content_txt = re.sub(r"\n", "", soup_in.select_one("div#main-content").text)
                    content = re.sub(r"\u3000", "", re.findall(r".+\d{2}:\d{2}:\d{2} \d{4}(.+)--※ 發信站:",
                                                               content_txt)[0])
                    date_text = tree_in.xpath("//span[contains(text(),'時間')]/following-sibling::span")[0].text
                    year = re.findall(r".+\d{2}:\d{2}:\d{2} (\d+)$", date_text)[0]
                    date = year + "-" + date
                    ip_tag = re.findall(r"來自: (\d+\.\d+\.\d+\.\d+)※", content_txt)
                    if ip_tag:
                        ip = ip_tag[0]
                    else:
                        ip = ""
                    comments = soup_in.select("div.push")
                    comments_count = len(comments)
                    boo_len = len(extract_comments(tree_in, "噓 "))
                    push_len = len(extract_comments(tree_in, "推 "))
                    neutral_len = len(extract_comments(tree_in, "→ "))
                    comments_list = []
                    for comment in comments:
                        push_content = comment.select_one("span.push-content").text
                        push_ipdatetime = comment.select_one("span.push-ipdatetime").text.replace("\n", "")
                        push_tag = comment.select_one("span.push-tag").text
                        push_userid = comment.select_one("span.push-userid").text
                        comments_list.append({'push_content': push_content,
                                              'push_ipdatetime': push_ipdatetime,
                                              "push_tag": push_tag,
                                              "push_userid": push_userid})
                    data = {
                        'ip': ip,
                        'article_id': ID,
                        "board": board,
                        'author': author,
                        'title': title,
                        'url': link,
                        'rate': rate,
                        'content': content,
                        'date': date,
                        'comments_count': {
                            "total_count": comments_count,
                            "boo": boo_len,
                            "push": push_len,
                            "neutral": neutral_len,
                        },
                        'comments': comments_list
                    }
                    path = "./Data/{}/{}/{}.json".format(board, keyword, ID)
                    save_data(data, path)
        except Exception as e:
            print('本文已被刪除', e)


def save_data(data, path):
    with open(path, "w") as f:
        json.dump(data, f)


def main():
    board = "rent-exp"
    url = "https://www.ptt.cc/bbs/{}/index.html".format(board)
    total_page_numbers = get_total_page(url)
    start_page = 1
    # total_page_numbers = 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        data_lists = [executor.submit(content_crawler, page_num, board) for page_num in range(start_page,
                                                                                              total_page_numbers+1)]
        for future in concurrent.futures.as_completed(data_lists):
            try:
                future.result()
            except Exception as e:
                print(e)
    print("finish extracting files")

if __name__ == "__main__":
    main()

