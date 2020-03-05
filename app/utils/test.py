import json

from app.dbUtils import config
from app.utils.matrix import matrix
from app.utils.userItem import read

# r = read()
# r.ReadFile('data.csv')

# m = matrix()
# m.ItemSimilarity(r.users_rating)
# print(m.cosine_martix)
# print(m.user_martix)
#
# r.Userappend('1', '3', '1')
# m.UpdateMartix('3', r.users_rating['1'])
# print(m.cosine_martix)
# print(m.user_martix)

if __name__ == '__main__':
    # redis
    redis = config.conn()
    # 用户物品倒排表
    r = read()
    r.ReadFile('data.csv')
    m = matrix()
    m.ItemSimilarity(r.users_rating)
    # 将倒排表存储到redis
    # for i, v in r.users_rating.items():
    #     redis.hset('user_item', i, json.dumps(v))
    # 共现矩阵
    # for i, v in m.item_martix.items():
    #     redis.hset('item_martix', i, json.dumps(v))
    # # 余弦相似度矩阵
    # for i, v in m.cosine_martix.items():
    #     redis.hset('cosine_martix', i, json.dumps(v))
    # 物品出现次数
    # for i, v in m.item_numbers.items():
    #     redis.hset('item_numbers', i, v)


