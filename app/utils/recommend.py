def Recommendation(train, userId, martix, K):
    """
    :param train: 数据
    :param userId: 指定的用户id
    :param martix: 余弦相似度矩阵
    :param K: 推荐的数量
    :return:
    """
    rank = dict()
    item_score = train[userId]  # 指定用户的评分
    for item, score in item_score.items():
        for j, mj in sorted(martix[item].items, key=lambda x: x[1], reverse=True)[0:K]:
            if j in item_score:
                continue
            else:
                rank.setdefault(j, 0)
                rank[j] += score * mj
    return sorted(rank.items(), key=lambda x: x[1], reverse=True)