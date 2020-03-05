import math


class matrix:

    def __init__(self):
        self.item_martix = dict()  # 共现矩阵
        self.item_numbers = dict()  # 物品出现的次数
        self.cosine_martix = dict()  # 余弦相似度矩阵

    def ItemSimilarity(self, train):
        """
        :param train: 用户评分文件
        :return:
        """
        for user, items in train.items():
            for i in items.keys():
                self.item_martix.setdefault(i, {})
                self.item_numbers.setdefault(i, 0)
                self.item_numbers[i] += 1
                for j in items.keys():
                    if i == j:
                        continue
                    else:
                        self.item_martix[i].setdefault(j, 0)
                        self.item_martix[i][j] += 1

        for i, items in self.item_martix.items():
            for j, v in items.items():
                self.cosine_martix.setdefault(i, {})
                self.cosine_martix[i].setdefault(j, 0)
                self.cosine_martix[i][j] = v / math.sqrt(self.item_numbers[i] * self.item_numbers[j])

    def UpdateMartix(self, item, user_item):
        """
        :param item: 添加的物品id
        :param user_item: 指定用户的物品倒排表
        :return:
        """
        self.item_numbers.setdefault(item, 0)
        self.item_numbers[item] += 1
        # 更新共现矩阵和余弦相似度矩阵
        for i in user_item.keys():
            if i == item:
                continue
            else:
                self.item_martix[i].setdefault(item, 0)
                self.item_martix[i][item] += 1
                self.cosine_martix[i][item] = self.item_martix[i][item] / \
                                              math.sqrt(self.item_numbers[i] * self.item_numbers[item])
