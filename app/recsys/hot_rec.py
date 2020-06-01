# -*- coding: utf-8 -*- 
# @Time : 2020/3/7 13:01 
# @Author : long 
# @File : hot_rec.py

import os
import numpy as np
from app.dbUtils import config

# redis
from app.models import UserPaper

redis = config.conn()

N = 20


def hot_rec():
    cwd = os.getcwd()
    f_path = os.path.abspath(os.path.join(cwd, ".."))
    store_path = f_path + "/output/hot_rec.npy"

    # play_action_f = f_path + "/output/play_action.npy"
    # play_action = np.load(play_action_f, allow_pickle=True).item()
    # print(play_action)

    data = UserPaper.query.all()
    result = dict()
    for i, element in enumerate(data):
        d = element.to_dict()
        # user_id = d['u_id']
        # paper_id = d['wp_id']
        # print(d)
        wp_id = d['wp_id']
        if result.get(wp_id) is None:
            result[wp_id] = 1
        else:
            result[wp_id] += 1
    return result


hot_rec()

