# -*- coding: utf-8 -*- 
# @Time : 2020/2/18 13:32 
# @Author : long 
# @File : metadata.py
import os

from app.dbUtils import config
from app.models import WellPaper
import numpy as np

redis = config.conn()
cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))


# 将mysql中的壁纸信息写到本地
def save_metadata():
    data = WellPaper.query.all()
    metadata_map = dict()
    for i, element in enumerate(data):
        paper = element.to_dict()
        id = paper['id']
        wp_id = paper['wp_id']
        wp_type = paper['wp_type']
        wp_url = "http://127.0.0.1:5000/photo" + paper['wp_url'].split("/upload")[1]
        metadata_map[id] = (wp_id, wp_type, wp_url)
    store_path = f_path + "/output/paper_metadata.npy"
    np.save(store_path, metadata_map)


# save_metadata()
















