import datetime
import random


class Pic_str:
    def create_uuid(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0, 100)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum


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
