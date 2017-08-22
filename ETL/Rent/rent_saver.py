import json
import os

import pymysql


path = "./ExData/"
objlist = []

#讀取所有檔案 
for filename in os.listdir(path):
    if filename.endswith(".json"):
        with open(path + filename, "r") as f:
            objlist.append(json.load(f))


# 存入mariadb
for obj in objlist:
    conn = pymysql.connect(host='hostIP',
                                port=3036,
                                user='username',
                                password='password',
                                db='rent_obj',
                                charset='utf8mb4')
    
	try:
        with conn.cursor() as cursor:
			# rent(db name) 插入資料
            sql = '''INSERT INTO rent (url,update_date,title,address,label,temp,sex,pet,cook,smoke,space,floor,stories,
                pattern,rent,landlord,description,lat,lng,cityID) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}',
                '{}',{},{},{},'{}',{},'{}','{}',{},{},{});'''.format(obj['url'], obj['updateDate'], obj['title'],
                                                                     obj['address'],obj['label'], obj['temp'],
                                                                     obj['sex'], obj['pet'], obj['cook'], obj['smoke'],
                                                                     obj['space'], obj['floor'], obj['stories'],
                                                                     obj['pattern'], obj['rent'],
                                                                     obj['landlord'], obj['description'], obj['lat'],
                                                                     obj['lng'], obj['cityID'])
            cursor.execute(sql)
            conn.commit()
   
   except Exception as e:
        print(obj)
        print(e)

    finally:
        conn.close()

