# -*- coding: utf-8 -*- 
# @Time : 2020/2/29 09:56 
# @Author : long 
# @File : relevance_rec.py

import os
import numpy as np
from scipy.sparse import dok_matrix
import heapq

from app.models import UserPaper


def relevance():
    rec_num = 30
    cwd = os.getcwd()
    # f_path = os.path.abspath(os.path.join(cwd, ".."))

    user_s = set()
    paper_s = set()
    # 获取所有用户的id和壁纸的id，使用set避免重复
    data = UserPaper.query.all()
    for i, element in enumerate(data):
        d = element.to_dict()
        user_id = d['u_id']
        paper_id = d['wp_id']
        user_s.add(user_id)
        paper_s.add(paper_id)

    user = list(user_s)
    paper = list(paper_s)

    user_num = len(user)
    paper_num = len(paper)

    print("===================开始构建用户id索引==================")
    uid2idx_map = dict()
    idx2uid_map = dict()
    index = 0
    for uid in user:
        uid2idx_map[uid] = index
        idx2uid_map[index] = uid
        index += 1

    print("===================开始构建壁纸id索引==================")
    pid2idx_map = dict()
    idx2pid_map = dict()
    index = 0
    for pid in paper:
        pid2idx_map[pid] = index
        idx2pid_map[index] = pid
        index += 1

    print("===================开始构建用户行为矩阵==================")
    # 构建用户行为矩阵
    Mat = dok_matrix((paper_num, user_num))
    for i, element in enumerate(data):
        d = element.to_dict()
        user_id = d['u_id']
        paper_id = d['wp_id']
        score = 1
        u_id = uid2idx_map[user_id]
        p_id = pid2idx_map[paper_id]
        Mat[p_id, u_id] = score

    print("===================完成构建用户行为矩阵==================")

    Mat_csr = Mat.tocsr()  # 压缩稀疏行矩阵

    print("===================Mat_csr.shape==================")
    print(Mat_csr.shape)
    print("-----------video_num---------------")
    print(paper_num)

    f_path = os.path.abspath(os.path.join(cwd, ".."))
    data_f = f_path + "/output/similarity_rec.npy"

    all_sim_map = dict()
    for v1 in range(paper_num):
        print(v1)
        vec1 = Mat_csr.getrow(v1)
        vec = np.zeros(paper_num)  # 评分
        for v2 in range(paper_num):
            if v1 == v2:
                val = 0
            else:
                vec2 = Mat_csr.getrow(v2)
                val = cos_sim(vec1.A, vec2.A)
            vec[v2] = val
        c = top_n_max(vec, rec_num)  # [[v1,v2,v3],[idx1,idx2,idx3]]
        original_vid = idx2pid_map[v1]
        sim = c[0]
        idx = c[1]
        vid = [idx2pid_map[k] for k in idx]
        res = zip(vid, sim)
        all_sim_map[original_vid] = res

    print(len(all_sim_map))
    np.save(data_f, all_sim_map)


def top_n_max(vector, n):
    """
    给定一个数组，求该数组最大的n个值，及每个值对应的下标index.
    :param vector: 输入的数值型数组，类型 <type 'numpy.ndarray'>
    :param n: 输出最大值的个数
    :return: [[v1,v2,v3],[idx1,idx2,idx3]]
    """
    idx_ = heapq.nlargest(n, range(len(vector)), vector.take)
    res_ = vector[idx_]
    return [res_, idx_]


def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    inner_product = float(vector_a * vector_b.T)
    nom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = inner_product / nom
    return cos

# relevance()



