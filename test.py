# import sqlrequests
#
# sql_cursor = sqlrequests.PsqlRequests()
# if not sql_cursor.IS_CONNECT:
#     print('bad')
#
# a = sql_cursor.select('item')
# print(a)
#
#
# item = sql_cursor.select(from_to_take="item")
# writer = sql_cursor.select(from_to_take="writer")
# photo = sql_cursor.select(from_to_take="item_photo")

# a = open('item.txt', 'w')
# a.close()
# a = open('writer.txt', 'w')
# a.close()
# a = open('item_photo.txt', 'w')
# a.close()
#
#
# with open('item.txt', 'w') as f:
#     f.write(str(item))
# with open('writer.txt', 'w') as f:
#     f.write(str(writer))
# with open('item_photo.txt', 'w') as f:
#     f.write(str(photo))

import sqlrequests
names = ['Amy', 'Clara', 'Vika', 'Yan']


# class SpamPas:
#     def __init__(self, names :list = None):
#         self._name = names
#
#     def create(self):
#         self._hellos = []
#
#         for i in self._name:
#             a = Pas(i)
#             self._hellos.append(a)


a = sqlrequests.PsqlRequests()
b = a.select('item')


for i in range(20, 0, -1):
    print(i)
