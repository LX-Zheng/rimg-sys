# -*- coding: utf-8 -*- 
# @Time : 2020/2/28 15:36 
# @Author : long 
# @File : userhistory.py

import numpy as np
import os

from app.models import UserPaper


def user_action_to_map():
    """
    将用户行为转化为dict存储到本地
    :param store_path: 存储地址
    :return: null
    """
    cwd = os.getcwd()
    f_path = os.path.abspath(os.path.join(cwd, ".."))
    store_path = f_path + "/output/play_action.npy"
    rec_map = dict()
    data = UserPaper.query.all()
    for i, element in enumerate(data):
        d = element.to_dict()
        user_id = d['u_id']
        paper_id = d['wp_id']
        score = 1
        if user_id in rec_map:
            s = rec_map.get(user_id)
            s.add((paper_id, score))
            rec_map[user_id] = s
        else:
            s = set()
            s.add((paper_id, score))
            rec_map[user_id] = s
    np.save(store_path, rec_map)


# cwd = os.getcwd()
# f_path = os.path.abspath(os.path.join(cwd, ".."))
#
# store_path = f_path + "/output/play_action.npy"
# user_action_to_map(store_path)
user_action_to_map()

