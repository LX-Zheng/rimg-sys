
class read:

    def __init__(self):
        self.users_rating = dict()

    def ReadFile(self, rating):
        """
        :param rating: 用户评分文件
        :return:
        """
        with open(rating, "r", encoding="utf-8") as fp:
            for line in fp:
                user, item, score = line.split(",")[0:3]
                # self.users_rating.setdefault(user, {})
                # self.users_rating[user][int(item)] = float(eval(score))
                self.Userappend(user, item, score)

    def Userappend(self, user, item, score):
        self.users_rating.setdefault(user, {})
        self.users_rating[user][item] = float(eval(score))

