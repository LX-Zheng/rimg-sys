# -*- coding: utf-8 -*- 
# @Time : 2020/5/13 18:17 
# @Author : long 
# @File : handle.py
import os

from app.recsys.item_base import item_base
from app.recsys.metadata import save_metadata
from app.recsys.relevance_rec import relevance
from app.recsys.save_redis import save_rec, save_metadata
from app.recsys.userhistory import user_action_to_map

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))


def start():
    save_metadata()  # 将mysql中的壁纸信息写到本地
    user_action_to_map()  # 将用户行为转化为dict存储到本地
    relevance()
    item_base()

    item_based_rec_p = f_path + "/output/item_based_rec.npy"
    item_based_rec_db = 2
    save_rec(item_based_rec_p, item_based_rec_db)

    metadata_p = f_path + "/output/paper_metadata.npy"
    metadata_db = 3
    save_metadata(metadata_p, metadata_db)

