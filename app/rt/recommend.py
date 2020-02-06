import numpy as np
import pandas as pd

data_col = ['user_id', 'item_id', 'rating']

# 用户、物品、评分
data = pd.read_table('./data.txt', header=None, names=data_col, parse_dates=['rating'], sep=',')


# 生成用户对物品的评分矩阵
def user_item_score(df, user_name, item_name, score_name):
    """
    :param df: 数据源
    :param user_name: 用户列名
    :param item_name: 物品列名
    :param score_name: 评分列名
    :return: 返回用户对物品的评分矩阵
    """
    user_names = df[user_name].unique()
    item_names = df[item_name].unique()
    user_num = len(user_names)
    item_num = len(item_names)
    zero_matrix = pd.DataFrame(np.zeros((user_num, item_num)), index=user_names, columns=item_names)
    for i in df.itertuples():
        zero_matrix.loc[getattr(i, user_name), getattr(i, item_name)] = getattr(i, score_name)
    return zero_matrix


user_item_matrix = user_item_score(data, 'user_id', 'item_id', 'rating')


# print(user_item_matrix)


# user_item_matrix.to_csv('./user_item_matrix.csv')

# 生成物品同现矩阵，按照用户ID来进行物品的一个汇总，生成一个用户分组后的物品列表
def create_item_list_by_user(df, user_name, item_name):
    """
    :param df: 数据源
    :param user_name: 按照用户列名来划分
    :param item_name: 对应的物品列表比如物品ID
    :return: 返回结果是按照用户ID和对应的物品列表ID列表
    """
    res = {}
    item_list = []
    for i in df.itertuples():
        res.setdefault(getattr(i, user_name), []).append(getattr(i, item_name))
    for i in res.keys():
        item_list.append(res[i])
    return item_list


item_list = create_item_list_by_user(data, 'user_id', 'item_id')  # [[],[],[]]


def create_item_matrixs(items, item_len, item_name_list):
    """
    :param items: 物品集合
    :param item_len: 总物品数
    :param item_name_list: 物品总集合(无重复)
    :return: 返回物品同现矩阵，此处实际返回DataFrame类型
    """
    item_matrixs = pd.DataFrame(np.zeros((item_len, item_len)), index=item_name_list, columns=item_name_list)
    for im in items:  # [[],[],[]]
        for i in range(len(im)):
            for j in range(len(im) - i):
                item_matrixs.loc[im[i], im[j + i]] += 1
                item_matrixs.loc[im[j + i], im[i]] = item_matrixs.loc[im[i], im[j + i]]
    return item_matrixs


item_set = data['item_id'].unique()
item_matrix = create_item_matrixs(item_list, len(item_set), item_set)


# print(item_matrix)
# item_matrix.to_csv('./item_matrix.csv')

# 通过物品同现矩阵*用户评分矩阵=推荐结果
def get_itemCF(item_matrix, user_score, col_num):
    """
    :param item_matrix: 物品同现矩阵
    :param user_score: 用户评分矩阵
    :param col_num:
    :return: 用户对物品的兴趣值
    """
    columns = item_matrix.columns  # 获取列索引
    user_score = user_score[columns]
    # 过滤掉用户评价的物品
    user_wp = user_score[user_score.iloc[0] == 0].index  # .index获取行索引 .value返回ndarray类型 ndarray是numpy的N维数组对象
    # 取True即值为0的行索引即用户没有评分的物品
    item_matrix = np.mat(item_matrix.to_numpy().astype(int))
    user_score = np.mat(user_score.to_numpy().astype(int))[0].T
    result_score = item_matrix * user_score
    result = pd.DataFrame(result_score, index=columns, columns=['rating'])
    result = result.sort_values(by='rating', ascending=False)
    result[col_num] = columns
    return result[result[col_num].isin(user_wp)]


user_result = get_itemCF(item_matrix, user_item_matrix, 'wp_id')
print(user_result)
