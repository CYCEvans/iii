import concurrent.futures
import time
import os

import flickrapi
import requests

API_KEY = "Your API Key"
API_SECRET = "Your API Secret"
# Search the scene you want
keyword_list = [("象山101", "101"), ("女王頭", "queen_head"), ("彩虹橋", "rainbow_bridge"),
                ("西門紅樓", "Red_House_Theater"),("不厭亭", "Buyen_Pavilion"), ("十分瀑布", "Shihfen_Waterfall"),
                ("總統府", "president_office"), ("新北大橋", "New_Taipei_Expwy"),
                ("自由廣場", "C_K_M_Hall"), ("富貴角燈塔", "Tapin_lighthouse")]


def get_links(keyword, photo_size, api_key, api_secret):
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    try: # key_word sorted_rating
        # sort="relevance","date-posted-desc","date-taken-asc","interestingness-desc"
        # min_taken_date='2008-08-20'
        # max_upload_date = '2008-08-30'
        photos = flickr.walk(text=keyword, extras=photo_size, sort="relevance")
    except Exception as e:
        print('Error:{}'.format(e))
    url_list = []
    for photo in photos:
        url = photo.get(photo_size)
        if url:
            url_list.append(url)
    url_list = set(url_list)

    return url_list


def get_filenames(links, place):
    fileames = []
    for link in links:
        if link:
            fname = "./data/{}/".format(place) + link.split("/")[-1]
            fileames.append(fname)
    return fileames


def save_urls(filename, url_list):
    with open(filename, "w+") as f:
        for url in url_list:
            if url is not "":
                f.write(url + ",")


def read_urls(filename):
    old_links = []
    with open(filename, 'r') as f:
        if f.readable():
            dataLinks = f.read().split(",")
            dataLinks.pop(-1)
            for link in dataLinks:
                old_links.append(link)
    return old_links


def save_image(link, fname):
    res = requests.get(link)
    with open(fname, 'wb') as f:
        f.write(res.content)


def main():
    for keyword, place in keyword_list:
        ex_path = "./data/{}/".format(place)
        if not os.path.exists(ex_path):
            os.makedirs(ex_path)
        photo_size = 'url_m'
        filename = "{}_links.txt".format(place)
        if not os.path.exists(filename):
            with open(filename, "w+"):
                pass
        old_links = read_urls(filename)
        print("Total old links is {}".format(len(old_links)))
        new_links = []
        links = list(get_links(keyword, photo_size, API_KEY, API_SECRET))
        for link in links:
            if link not in old_links:
                new_links.append(link)
        print("Total new links is {}".format(len(new_links)))

        file_names = get_filenames(new_links, place)
        # multi_thread
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            pageCotents = [executor.submit(save_image, link, fname) for link, fname in zip(new_links, file_names)]
            for future in concurrent.futures.as_completed(pageCotents):
                try:
                    future.result()
                except Exception as e:
                    print(e)
    print("{} 已爬圖完成".format(keyword))
    new_links = new_links + old_links
    links = set(new_links)
    save_urls(filename, links)


if __name__ == "__main__":
    print(time.ctime())
    start = time.time()
    main()
    end = time.time()
    print("Total time is {} seconds".format(end - start))
    print(time.ctime())
