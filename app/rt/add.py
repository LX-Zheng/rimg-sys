# fp = open('data.txt', 'w')

# for i in range(10):
#     c = "1" + str(i) + " 1"
#     fp.write(c)

with open('data.txt', 'w') as f:
    for j in range(1, 11):
        for i in range(1, 11):
            c = str(j) + "," + str(i) + ",1"
            f.write(c)
            f.write('\n')
