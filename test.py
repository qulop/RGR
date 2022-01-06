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

postgres_cursor = sqlrequests.PsqlRequests()
all_items = postgres_cursor.select(from_to_take='item', what_to_take=['item.*', 'writer.full_name', 'item_photo.path'],
                                   join=[['writer', 'writer_id'], ['item_photo', 'photo_id']],
                                   select_exceptions=['item.writer_id', 'item.photo_id'])
print(all_items)