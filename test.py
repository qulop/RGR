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

from tkinter import *
from tkinter.font import Font

def anime():
    global y, x, font_start, a
    a.config(font=font_start)
    y += 1
    x -= 1
    a.place(x=x, y=y)
    if y != 60:
        font_start['size'] += 2
        root.after(1, anime)

def down():
    global y, x, font_start
    a.config(font=font_start)
    y -= 1
    x += 1
    a.place(x=x, y=y)
    if y != 50:
        font_start['size'] -= 2
        root.after(1, anime)


def main():
    a.place(x=x, y=y)
    anime()
    # down()

root = Tk()
root.config(width=600, height=600)
font_start = Font(size=1)
x = 50
y = 50
a = Label(root, text='Amy!', font=font_start)

root.after(1000, main)
a.destroy()


root.mainloop()

