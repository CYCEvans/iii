# 利用RNN來辨識captcha

## 主要參考github:https://github.com/Slyne/CaptchaVariLength
## 利用 generator.py 和 data_generate.py 來生成captcha sample ，差別只在於一個是用captcha套件，另一個是自己用PIL套件手刻的captcha生成器
## preprocess.py 前處理圖片， test_preprocess則是用來前處理測試集
## train.py開始訓練自己的model
## model.ipynb試著使用套件劃出model圖片