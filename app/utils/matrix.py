import math


def ItemSimilarity(train):
    """
    :param train: 用户评分文件
    :return: 物品之间的余弦相似度矩阵
    """
    item_martix = dict()  # 共现矩阵
    user_martix = dict()  # 物品出现的次数
    for user, items in train.items():
        for i in items.keys():
            item_martix.setdefault(i, {})
            user_martix.setdefault(i ,0)
            user_martix[i] += 1
            for j in items.keys():
                if i == j:
                    continue
                else:
                    item_martix[i].setdefault(j, 0)
                    item_martix[i][j] += 1
    cosine_martix = dict()
    for i, items in item_martix.items():
        for j, v in items.items():
            cosine_martix.setdefault(i, {})
            cosine_martix[i].setdefault(j, 0)
            cosine_martix[i][j] = v / math.sqrt(user_martix[i] * user_martix[j])
    return cosine_martix


