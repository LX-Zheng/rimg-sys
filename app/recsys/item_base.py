# -*- coding: utf-8 -*- 
# @Time : 2020/2/28 19:33 
# @Author : long 
# @File : item_base.py

import os
import numpy as np

rec_num = 15

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))


def item_base():
    play_action_f = f_path + "/output/play_action.npy"
    similarity_f = f_path + "/output/similarity_rec.npy"

    play_action = np.load(play_action_f, allow_pickle=True).item()
    similarity = np.load(similarity_f, allow_pickle=True).item()

    item_based_rec_map = dict()
    for u, u_play in play_action.items():
        u_rec = dict()
        for (vid, u_score) in u_play:
            if vid in similarity:
                for (vid_s, vid_score) in similarity[vid]:
                    if vid_s in u_rec:
                        u_rec[vid_s] += u_score * vid_score
                    else:
                        u_rec[vid_s] = u_score * vid_score
        if len(u_rec) >= rec_num:
            sorted_list = sorted(u_rec.items(), key=lambda item: item[1], reverse=True)
            res = sorted_list[:rec_num]
            item_based_rec_map[u] = res

    # print(item_based_rec_map)
    item_base_rec_path = f_path + "/output/item_based_rec.npy"
    np.save(item_base_rec_path, item_based_rec_map)



