import concurrent.futures
import math
import os
import re
import time

from rent_extract import SinyiExtract


def save_data(extractor, data_obj):
    data, fileName = data_obj
    extractor.save_extract_data(data, fileName)


def update_loc_data(extractor, data_obj):
    # api_key ="YourAPIKey"
    data, fileName = data_obj
    if data["lat"] == 0.0 and data["lng"] == 0.0 and data["cityID"] == 0:
        data["lat"], data["lng"], data["cityID"] = extractor.get_location(data["address"], api_key="")
        extractor.save_extract_data(data, fileName)


def main():
    api_key = "YourAPIKey"
    proxies = {"http": "http_loc",
               "https": "https_loc"}
    for name in ["TPE"]:
        city_name = name
        raw_data_path = "./Data/Sinyi/{}/".format(city_name)
        ex_data_path = "./ExData/Sinyi/{}/".format(city_name)
        if not os.path.exists(ex_data_path):
            os.makedirs(ex_data_path)
        sy_extractor = SinyiExtract(raw_data_path, ex_data_path)
        dict_lists, filename_lists = sy_extractor.load_raw_data()
        exist_data = sy_extractor.load_extract_data()
        print("{}共有{}個資料輸出".format(city_name, len(dict_lists)))
        data_lists = []
        for dict_obj in dict_lists:
            var_list = []
            iter_extractor = SinyiExtract()
            var_list.append(dict_obj["url"])
            var_list.append(dict_obj["update"])
            html = dict_obj['html']
            iter_extractor.get_content(html)
            iter_extractor.get_status(var_list)

            var_list.extend([0.0, 0.0, 0])
            data = iter_extractor.set_dict(var_list)
            data_lists.append(data)
        print("finish extraction!")
        # 如果沒更新到經緯度，用下列程式碼更新
        zip_obj = zip(data_lists, filename_lists)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            data_lists = [executor.submit(save_data, sy_extractor, data_obj) for data_obj in zip_obj]
            for future in concurrent.futures.as_completed(data_lists):
                try:
                    future.result()
                except Exception as e:
                    print(e)
        print("finish saving files")
        ex_data_path = "./ExData/Sinyi/{}/".format(city_name)
        sy_extractor = SinyiExtract(ex_data_path=ex_data_path)
        dict_lists, filename_lists = sy_extractor.load_extract_data()
        print("{}共有{}個資料修改".format(city_name, len(dict_lists)))
        zip_obj = zip(dict_lists, filename_lists)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            data_lists = [executor.submit(update_loc_data, sy_extractor, data_obj) for data_obj in zip_obj]
            for future in concurrent.futures.as_completed(data_lists):
                try:
                    future.result()
                except Exception as e:
                    print(e)
        print("finish updating files")


if __name__ == "__main__":
    main()