import datetime
import random
import urllib.request
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Pic_str:
    def create_uuid(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0, 100)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum


class Reptile:
    def __init__(self, pos):
        self.urlStr = str()
        self.pos = pos

    def crawling(self, url):
        global html
        req = urllib.request.urlopen(url)
        try:
            html = req.read().decode("gb2312")
        except UnicodeDecodeError:
            print("err")
        reg = r'src="(.+?\.jpg)"'
        imgre = re.compile(reg)
        self.urlStr = imgre.findall(html)[0]
        name = Pic_str().create_uuid() + '.jpg'
        urllib.request.urlretrieve(self.urlStr, self.pos+'/'+name)
        return name


def type_to_type(type):
    new_type = ""
    if type == "life":
        new_type = "生活写真"
    elif type == "color":
        new_type = "炫彩壁纸"
    elif type == "animal":
        new_type = "动物植物"
    elif type == "food":
        print("进入")
        new_type = "美食壁纸"
    elif type == "person":
        new_type = "人物写真"
    elif type == "design":
        new_type = "设计创意"
    elif type == "sport":
        new_type = "体育壁纸"
    elif type == "nature":
        new_type = "自然风景"
    elif type == "other":
        new_type = "其他壁纸"
    return new_type
