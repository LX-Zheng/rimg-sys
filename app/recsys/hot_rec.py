# -*- coding: utf-8 -*- 
# @Time : 2020/3/7 13:01 
# @Author : long 
# @File : hot_rec.py

import os
import numpy as np
from app.dbUtils import config

# redis
redis = config.conn()

N = 20


def hot_rec():
    cwd = os.getcwd()
    f_path = os.path.abspath(os.path.join(cwd, ".."))
    store_path = f_path + "/output/hot_rec.npy"

    data = redis.hgetall('hot')
    res = sorted(data.items(), key=lambda item: item[1], reverse=True)[:30]
    np.save(store_path, res)
