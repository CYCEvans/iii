import concurrent.futures
import os
import json
import time

from pymongo import MongoClient


def read_data(path):
    dict_lists = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            with open(path + filename, "r") as f:
                dict_lists.append(json.load(f))
    return dict_lists


def save_to_mongo(board, keyword, dict_lists):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.ptt
    collection_name = "ptt_{}_{}".format(board.replace("-", "_"), keyword)
    collection = db[("{}".format(collection_name))]
    result = collection.insert_many(dict_lists)
    client.close()


def main():
    board = "rent-exp"
    keyword = "all"
    path = "./Data/{}/{}/".format(board, keyword)
    dict_lists = read_data(path)
    print("extraction is OK")
    save_to_mongo(board, keyword, dict_lists)

if __name__ == "__main__":
    main()
