def ReadFile(rating):
    """
    :param rating: 用户评分文件
    :return: 用户物品倒排表
    """
    users_rating = dict()
    with open(rating, "r", encoding="utf-8") as fp:
        for line in fp:
            user, item, score = line.split(",")[0:3]
            users_rating.setdefault(user, {})
            users_rating[user][int(item)] = float(eval(score))
    return users_rating