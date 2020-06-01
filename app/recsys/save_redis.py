# -*- coding: utf-8 -*- 
# @Time : 2020/4/8 12:02 
# @Author : long 
# @File : save_redis.py

import os
import numpy as np
from app.dbUtils import config
import json


def save_rec(path, db):
    """
    将推荐的结果存放到redis中
    存储的数据结构{"hot": [(*,*),(*,*)]}
    :param path: 推荐结果存放的路径
    :param db: 推荐结果存放的db
    :return: null
    """
    rec_dict = np.load(path, allow_pickle=True).item()
    r = config.conn()
    for key, value in rec_dict.items():
        r.zadd(key, dict(value))
    r.close()


def save_metadata(path, db):
    """
    将壁纸的信息存储到redis中
    {"id": (wp_id, wp_type, wp_url)}
    :param path: 壁纸data存放的路径
    :param db: 存的的db
    :return: null
    """
    rec = np.load(path, allow_pickle=True).item()
    r = config.conn()
    metadata_dict = np.load(path, allow_pickle=True).item()
    for key, value in metadata_dict.items():
        (wp_id, wp_url) = value[0], value[2]
        j = json.dumps({"wp_id": wp_id, "wp_url": wp_url})
        r.hset("metadata", wp_id, j)
    r.close()


cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))

# hot_rec_p = f_path + "/output/hot_rec.npy"
# hot_rec_db = 0
# save_rec(hot_rec_p, hot_rec_db)

# similarity_rec_p = f_path + "/output/similarity_rec.npy"
# similarity_rec_db = 1
# save_rec(similarity_rec_p, similarity_rec_db)


# --  start
# item_based_rec_p = f_path + "/output/item_based_rec.npy"
# item_based_rec_db = 2
# save_rec(item_based_rec_p, item_based_rec_db)
#
# metadata_p = f_path + "/output/paper_metadata.npy"
# metadata_db = 3
# save_metadata(metadata_p, metadata_db)
