import datetime
import time
import json
import os
import re
import math
import random

import requests
from bs4 import BeautifulSoup
from lxml import html


class RentExtract():

    def __init__(self, raw_data_path="", ex_data_path="", soup="", tree=""):
        self.raw_data_path = raw_data_path
        self.ex_data_path = ex_data_path
        self.soup = soup
        self.tree = tree

    def load_data(self, path):
        dict_lists = []
        filename_lists = []
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                filename_lists.append(filename)
                with open(path + filename, "r", encoding="utf-8") as f:
                    dict_lists.append(json.load(f))
        return dict_lists, filename_lists

    def load_extract_data(self):
        dict_lists, filename_lists = self.load_data(self.ex_data_path)
        return dict_lists, filename_lists

    def load_raw_data(self):
        dict_lists, filename_lists = self.load_data(self.raw_data_path)
        return dict_lists, filename_lists

    def get_content(self, content):
        self.soup = BeautifulSoup(content, "lxml")
        self.tree = html.fromstring(content)

    def get_location(self, address, proxies="", api_key=""):
        time.sleep(1.5)
        api_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
        api_url2 = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}"
        URL = api_url.format(address, api_key)
        res = requests.get(URL, proxies=proxies)
        location_dict = res.json()
        lat = location_dict['results'][0]['geometry']['location']['lat']
        lng = location_dict['results'][0]['geometry']['location']['lng']
        try:
            cityID = int(location_dict['results'][0]['address_components'][-1]['short_name'][:3])
        except ValueError:
            time.sleep(2)
            URL2 = api_url2.format(lat, lng, api_key)
            res2 = requests.get(URL2, proxies=proxies)
            zip_dict = res2.json()
            cityID = int(zip_dict['results'][0]['address_components'][-1]['short_name'][:3])
            res2.close()
        res.close()
        time.sleep(1.5)
        return lat, lng, cityID

    def get_status(self):
        pass

    def set_dict(self, data_lists):
        name_list = ["url", "update", "title", "address", "label", "temp", "rent", "sex", "pet", "cook", "smoke",
                      "space", "floor", "stories", "pattern", "landlord", "description", "lat", "lng", "cityID"]
        data_dict = dict(zip(name_list, data_lists))
        return data_dict

    def save_extract_data(self, data, filename=""):
        with open(self.ex_data_path + filename, "w") as f:
            json.dump(data, f)


class SinyiExtract(RentExtract):

    def get_status(self, var_list):
        title = self.soup.select_one("div.top > h1").text
        address_tag = self.tree.xpath("//th[contains(text(), '地　　址')]/following-sibling::td")
        if address_tag:
            address = re.sub(r"X|x", "", address_tag[0].text)
        else:
            address = "NA"

        house_type_tag = self.tree.xpath("//th[contains(text(), '類　　型')]/following-sibling::td")
        if house_type_tag:
            if house_type_tag[0].text == "套房":
                label = '套'
            elif house_type_tag[0].text == "雅房":
                label = "雅"
            elif house_type_tag[0].text == "整層住宅":
                label = "住"
            else:
                label = "NA"
        else:
            label = "NA"

        temp_tag = self.tree.xpath("//th[contains(text(), '最短租期')]/following-sibling::td")
        if temp_tag:
            temp_text = re.sub(r"\n|\t| |\r", "", temp_tag[0].text)
            if temp_text == "一年":
                temp = "N"
            else:
                temp = "Y"
        else:
            temp = "N"

        rent_tag = self.tree.xpath("//th[contains(text(), '租　　金')]/following-sibling::td")
        if rent_tag:
            rent_txt = rent_tag[0].text.replace(",", "")
            rent = int(re.findall(r"(\d+)元/月", rent_txt)[0])
        else:
            rent = 0

        sex_tag = self.tree.xpath("//th[contains(text(), '身份限制')]/following-sibling::td")
        if sex_tag:
            sex_text = re.sub(r"\n|\t| |\r", "", sex_tag[0].text)
            if "男女不拘" in sex_text:
                sex = "A"
            elif "限女性" in sex_text:
                sex = "F"
            elif "限男性" in sex_text:
                sex = "M"
        else:
            sex = "A"

        live_tag = self.tree.xpath("//th[contains(text(), '生活約定')]/following-sibling::td")
        if live_tag:
            live_text = re.sub(r"\n|\t", "", live_tag[0].text)
            pet_text = re.findall(r"養寵物(.*)、開伙", live_text)[0]
            cook_text = re.findall(r".*、開伙(.*)、.*", live_text)[0]
            smoke_text = re.findall(r"、抽菸(.*)", live_text)[0]
            if pet_text == "可":
                pet = "Y"
            else:
                pet = "N"
            if cook_text == "可":
                cook = "Y"
            else:
                cook = "N"
            if smoke_text == "可":
                smoke = "Y"
            else:
                smoke = "N"
        else:
            pet = "N"
            cook = "N"
            smoke = "N"

        space_tag = self.tree.xpath("//th[contains(text(), '建物坪數')]/following-sibling::td")
        if space_tag:
            space = float(re.sub("坪| *", "", space_tag[0].text))

        else:
            space = 0.0
        stories_tag = self.tree.xpath("//th[contains(text(), '樓　　層')]/following-sibling::td")
        if stories_tag:
            stories_text = stories_tag[0].text
            stories_pattern = re.findall(r"(\d+)樓/ 總樓層(\d+)", stories_text)[0]
            floor = int(stories_pattern[0])
            stories = int(stories_pattern[1])
        else:
            floor, stories = 0, 0

        pattern_tag = self.tree.xpath("//th[contains(text(), '隔間材料')]/following-sibling::td")
        if pattern_tag:
            pattern = pattern_tag[0].text
        else:
            pattern = "NA"

        tel_num = []
        tel_tags = self.tree.xpath("//div[@class='tel clearfix']//child::span")
        if tel_tags:
            for tel_tag in tel_tags:
                tel_num.append(tel_tag.attrib['class'].replace('dash', '').replace('d', '').replace('-', ''))
            tel = ''.join(tel_num)
        else:
            tel = ''
        landlord_tag = self.soup.select_one("div.landlord")
        if landlord_tag:
            landlord_name = landlord_tag.text
        else:
            landlord_name = ''
        if landlord_name != '' and tel != '':
            landlord = "{},{}".format(landlord_name, tel)
        else:
            landlord = "NA"
        description = re.sub(r"\u3000|\xa0|\n|\t|\r", "", self.soup.select("span[style=font-size:16px;]")[0].text)

        var_list.extend([title, address, label, temp, rent, sex, pet, cook, smoke,
                           space, floor, stories, pattern, landlord, description])
        return var_list


class HFExtract(RentExtract):

    def get_status(self, var_list, house_type):
        update_pattern = r"更新日期：(.+) \d{1,2}:\d{1,2}"
        update = (re.findall(update_pattern, self.soup.select_one("time.timer").text)[0]).replace("/", "-")
        title = self.soup.select_one("div.titleName > h2.title").text
        address_pattern = "//span[contains(text(), '地　　址：')]/following-sibling::address[@class='value addr']"
        address_tag = self.tree.xpath(address_pattern)
        if address_tag:
            address = re.sub(r"X|x", "", address_tag[0].text)
        else:
            address = "NA"

        if house_type == "H":
            label = "住"
        elif house_type == "T":
            label = "套"
        elif house_type == "Y":
            label = "雅"

        temp_tag = self.tree.xpath("//td[contains(text(), '最短租期')]/following-sibling::td[@class='values']")
        if temp_tag:
            temp_text = re.sub(r"\n|\t| |\r", "", temp_tag[0].text)
            if temp_text == "一年":
                temp = "N"
            else:
                temp = "Y"
        else:
            temp = "N"

        rent_tag = self.tree.xpath("//span[contains(text(), '租　　金：')]/following-sibling::span[@class='value']")
        if rent_tag:
            rent_txt = rent_tag[0].text_content().replace(",", "")
            rent = int(re.findall(r"(\d+) 元 / 月", rent_txt)[0])
        else:
            rent = "NA"

        sex_tag = self.tree.xpath("//td[contains(text(), '性別限制')]/following-sibling::td[@class='value']")
        if sex_tag:
            sex_text = re.sub(r"\n|\t| ", "", sex_tag[0].text)
            if "男女皆可" in sex_text:
                sex = "A"
            elif "限女生" in sex_text:
                sex = "F"
            elif "限男生" in sex_text:
                sex = "M"
            else:
                sex = "A"
        else:
            sex = "A"

        smoke = "N"

        cook_tag = self.tree.xpath("//td[contains(text(), '開　　伙')]/following-sibling::td[@class='value']")
        if cook_tag:
            cook_text = cook_tag[0].text
            if cook_text == "可":
                cook = "Y"
            elif cook_text == "不可":
                cook = "N"
            else:
                cook = "N"
        else:
            cook = "N"

        pet_tag = self.tree.xpath("//td[contains(text(), '養 寵 物')]/following-sibling::td[@class='value']")
        if pet_tag:
            pet_text = pet_tag[0].text
            if pet_text == "可":
                pet = "Y"
            elif pet_text == "不可":
                pet = "N"
            else:
                pet = "N"
        else:
            pet = "N"

        space_tag = self.tree.xpath("//span[contains(text(), '坪　　數：')]/following-sibling::span[@class='value']")
        if space_tag:
            space_text = re.sub("坪| *", "", space_tag[0].text)
            if space_text.isdigit():
                space = float(space_text)
            else:
                space = 0.0
        else:
            space = 0.0

        stories_tag = self.tree.xpath("//span[contains(text(), '樓　　層：')]/following-sibling::span[@class='value']")
        if stories_tag:
            stories_text = stories_tag[0].text
            stories_pattern = re.findall(r"(\d+) / (\d+) 樓", stories_text)[0]
            floor = int(stories_pattern[0])
            stories = int(stories_pattern[1])
        else:
            floor, stories = 0, 0

        pattern_tag = self.tree.xpath("//td[contains(text(), '隔間材質')]/following-sibling::td[@class='value']")
        if pattern_tag:
            pattern = pattern_tag[0].text
        else:
            pattern = "NA"

        tel_tag = re.findall(r"\d+-\d+-\d+", self.soup.select_one("span.tel").text)
        if tel_tag:
            tel = tel_tag[0].replace("-", "")
        else:
            tel = ''
        name_tag = self.tree.xpath(r"//span[contains(text(), '聯　絡　人：')]/following-sibling::span[@class='val']")
        if name_tag:
            landlord_name = name_tag[0].text
        else:
            landlord_name = ''

        if landlord_name != '' and tel != '':
            landlord = "{},{}".format(landlord_name, tel)
        else:
            landlord = "NA"

        description_tag = self.soup.select_one("div#divDes > div.freeWrap")
        if description_tag:
            description = re.sub(r"\u3000|\xa0|\n|\t| |\r", "", description_tag.text).replace("若無法播放影音，可能是您所使用的瀏覽器並未支援我們提供的播放程式，建議可根據您使用的瀏覽器，從以下連結進行更新：GoogleChromeFireFoxSafari若無法播放影音，可能是您所使用的瀏覽器並未安裝，或支援Flash播放程式，建議可根據您使用的瀏覽器，安裝適合的Flash播放程式。", "")
        else:
            description = "NA"
        var_list.extend([update, title, address, label, temp, rent, sex, pet, cook, smoke,
                         space, floor, stories, pattern, landlord, description])
        return var_list


class HBHExtract(RentExtract):

    def get_status(self, var_list, house_type):

        title = self.soup.select_one("span.adv").text
        address = self.soup.select_one("div.linetop > span.address").text

        if house_type == "H":
            label = "住"
        elif house_type == "T":
            label = "套"
        elif house_type == "Y":
            label = "雅"

        temp_tag = self.tree.xpath("//span[contains(text(), '短期租賃：')]")
        if temp_tag:
            temp_text = re.findall("短期租賃：(.*)", temp_tag[0].text)[0]
            if temp_text == "接受":
                temp = "Y"
            elif temp_text == "不接受":
                temp = "N"
            else:
                temp = "N"
        else:
            temp = "N"

        rent_tag = self.soup.select_one("span.itemmsg > span.price")
        if rent_tag:
            rent_text = rent_tag.text.replace("萬", '')
            try:
                rent = int((float(rent_text) * 10000))
            except Exception as e:
                print(e)
                rent = 0
        else:
            rent = 0

        sex_tag = self.tree.xpath("//span[contains(text(), '性別要求：')]")
        if sex_tag:
            sex_text = re.sub(r"\n|\t| ", "", sex_tag[0].text)
            sex_pattern = re.findall(r"性別要求：(.*)", sex_text)[0]
            if "不限" in sex_pattern:
                sex = "A"
            elif "限女生房客" in sex_pattern:
                sex = "F"
            elif "限男生房客" in sex_pattern:
                sex = "M"
            else:
                sex = "A"
        else:
            sex = "A"

        smoke = "N"

        cook_tag = self.tree.xpath("//span[contains(text(), '開伙：')]")
        if cook_tag:
            cook_text = re.findall(r"開伙：(.*)", cook_tag[0].text)[0]
            if cook_text == "接受":
                cook = "Y"
            elif cook_text == "不接受":
                cook = "N"
            else:
                cook = "N"
        else:
            cook = "N"

        pet_tag = self.tree.xpath("//span[contains(text(), '飼養寵物')]")
        if pet_tag:
            pet_text = re.findall(r"飼養寵物：(.*)", pet_tag[0].text)[0]
            if pet_text == "接受":
                pet = "Y"
            elif pet_text == "不接受":
                pet = "N"
            else:
                pet = "N"
        else:
            pet = "N"

        space_tag = self.tree.xpath("//span[contains(text(), '面積：')]/following-sibling::span[@class='itemmsg']|//span[contains(text(), '登記建坪：')]/following-sibling::span[@class='itemmsg']")
        if space_tag:
            try:
                space = float(space_tag[0].text.replace("坪", ""))
            except:
                space = 0.0
        else:
            space = 0.0

        stories_tag = self.tree.xpath("//span[contains(text(), '樓層：')]/following-sibling::span[@class='itemmsg']")
        if stories_tag:
            stories_text = stories_tag[0].text
            stories_pattern = re.findall(r"(\d+).*/.*(\d+)", stories_text)
            if stories_pattern:
                floor = int(stories_pattern[0][0])
                stories = int(stories_pattern[0][1])
            else:
                floor, stories = 0, 0
        else:
            floor, stories = 0, 0

        pattern = "NA"
        tel_tag = self.tree.xpath("//div[contains(text(), '行動電話：')]")
        if tel_tag:
            tel_text = tel_tag[0].text
            tel = (re.findall("行動電話：(.*)", tel_text)[0]).replace("-", "")
        else:
            tel = ''

        name_tag = self.tree.xpath("//div[contains(text(), '聯絡人：')]")
        if name_tag:
            name_text = name_tag[0].text
            landlord_name = re.findall(r"聯絡人：(.*)", name_text)[0]
        else:
            landlord_name = ''

        if landlord_name != '' and tel != '':
            landlord = "{},{}".format(landlord_name, tel)
        else:
            landlord = "NA"

        description_tag = self.soup.select_one("div#featurewrap > div.contentwrap")
        if description_tag:
            description = re.sub(r"\u3000|\xa0|\n|\t| |\r|●", "", description_tag.text)
        else:
            description = "NA"
        var_list.extend([title, address, label, temp, rent, sex, pet, cook, smoke,
                         space, floor, stories, pattern, landlord, description])
        return var_list