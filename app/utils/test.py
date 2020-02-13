from app.utils.matrix import matrix
from app.utils.userItem import read

r = read()
r.ReadFile('data.csv')

m = matrix()
m.ItemSimilarity(r.users_rating)
print(m.cosine_martix)
print(m.user_martix)

r.Userappend('1', '3', '1')
m.UpdateMartix('3', r.users_rating['1'])
print(m.cosine_martix)
print(m.user_martix)
