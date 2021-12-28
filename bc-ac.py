import PIL.Image
import PIL.ImageTk
from typing import Union
import tkinter.font as font
from tkinter import *
import sqlrequests

root = Tk()

height = root.winfo_screenwidth()
width = root.winfo_screenheight()

height = (height // 2) - 450    # calculating center of monitor for X
width_for_main_frame = (width // 2) - 320  # here for Y

root_width = 1200
root_height = 800
geometry_for_main_frame = f'{root_width}x{root_height}+{height}+{width_for_main_frame}'

main_bg = '#4d4d4d'
text_fg = '#b3b3b3'
button_bg = '#666666'   # '#cc5200'
button_ab = '#8c8c8c'
text_label_bg = button_bg
table_bg = '#808080'
lines_fill = '#404040'

root.geometry(geometry_for_main_frame)
root.resizable(height=False, width=False)
root.title('BC-AC.by')
root.config(bg=main_bg)

postgres_cursor = sqlrequests.PsqlRequests()
all_items = postgres_cursor.select(from_to_take='item', what_to_take=['item.*', 'writer.full_name', 'item_photo.path'],
                                   join=[['writer', 'writer_id'], ['item_photo', 'photo_id']],
                                   select_exceptions=['item.writer_id', 'item.photo_id'])


class ItemButton:
    def __init__(self, master, item, x: int, y: int, height: int = 340, width: int = 300, bg: str = 'white',
                 active_bg: str = '#f2f2f2', cursor=None):
        self.__x = x
        self.__y = y
        self.__height = height
        self.__width = width
        self.__background = bg
        self.__active_bg = active_bg

        self._title = item[1]
        self._writer = item[6]
        self._price = str(item[3]) + ' руб.'
        self._genre = item[4]
        self._rating = item[5]
        self._issue_year = item[2]
        path = item[-1]
        self._image = self.__image_resize(path)
        self.__title_bg = bg

        self.__button_frame = Canvas(master, width=self.__width, height=self.__height, bg=self.__background,
                                     highlightthickness=0)
        # self.__draw_item_frame()
        # self.__button_frame.place(x=self.__x, y=self.__y)
        #
        # self.__image_label = Label(self.__button_frame, image=self.__image)
        # self.__image_label.place(x=30, y=20)

        # root.after(1, self._monitoring_cursor_position)

        # self.__add_text()

    def __image_resize(self, path):
        image = PIL.Image.open(path)

        im_width, im_height = image.size
        im_width = int(im_width // 3.2)
        im_height = int(im_height // 3.2)

        image = image.resize((141, 218))
        self.__side_indent = (self.__width - image.size[0]) // 2
        image = PIL.ImageTk.PhotoImage(image)

        return image

    def __draw_item_frame(self):
        self.__button_frame.create_line(0, 0, 300, 0, width=3)
        self.__button_frame.create_line(0, 338, 300, 338, width=3)
        self.__button_frame.create_line(0, 0, 0, self.__height)

    def __text_wrapping(self, text):
        wrap_index = 0
        for i in range(21, 0, -1):
            if text[i] == ' ':
                wrap_index = i
                break

        text = list(text)
        text[wrap_index] = '\n'

        return ''.join(text)

    def __placing_too_long_title(self, title):
        wrap_index = 0

        upper_iteration_index = len(title)
        if upper_iteration_index < 33:
            upper_iteration_index = 21
        else:
            upper_iteration_index = 33
            print(len(title), upper_iteration_index)
        for i in range(upper_iteration_index-1, 0, -1):
            print(i)
            if title[i] == ' ':
                wrap_index = i
                break

        title = list(title)
        title1 = title[:wrap_index]
        title2 = title[wrap_index:]

        title1 = ''.join(title1)
        title2 = ''.join(title2)

        font_ = font.Font(size=15, family='Times', slant='roman', weight='bold')

        top_title = Label(self.__button_frame, text=title1, font=font_, bg=self.__title_bg)
        bottom_title = Label(self.__button_frame, text=title2, font=font_, bg=self.__title_bg)

        y1 = 235
        y2 = 260

        return [top_title, bottom_title], [y1, y2]
    # def _line_animation(self):
    #     def draw():
    #         if self.start <= self.__height:
    #             self.start += 1
    #             self.__button_frame.coords(self.__line1, 0, 0, 0, self.start)
    #             root.after(100, draw)
    #
    #     self.start = 0
    #     self.__line1 = self.__button_frame.create_line(0, 0, 0, self.start, width=3)
    #     root.after(1, draw)

    # def _monitoring_cursor_position(self):
    #     x = root.winfo_pointerx() - root.winfo_rootx()
    #     y = root.winfo_pointery() - root.winfo_rooty()
    #
    #     if (x >= self.__x and x <= self.__width) and (y >= self.__y and y <= self.__height):
    #         self.__button_frame.config(bg=button_ab)
    #         self._line_animation()
    #     else:
    #         self.__button_frame.config(bg=button_bg)
    #     root.after(1, self._monitoring_cursor_position)

    # def _cursor_on_widget(self):
    #     pass
    #
    # def _click_to_button(self, target):
    #     pass

    def place_button(self):
        title_font = font.Font(size=20, family='Times', slant='roman', weight='bold')
        other_text_font = font.Font(size=13, slant='roman')
        indent_by_y = 240
        x = 20

        y_indent_increment = {
            'too long title': {
                'writer increment': 43,
                'price increment': 27
            },
            'normal title length': {
                'writer increment': 30,
                'price increment': 25
            }
        }
        if len(self._title) > 20:
            title_size = 'too long title'
        else:
            title_size = 'normal title length'

        self.__draw_item_frame()
        self.__button_frame.place(x=self.__x, y=self.__y)

        self.__image_label = Label(self.__button_frame, image=self._image, bg=self.__background)
        self.__image_label.place(x=x, y=10)

        if len(self._title) > 20:
            self.__title_label, y_coordinates = self.__placing_too_long_title(self._title)
            for i in range(2):
                self.__title_label[i].place(x=x, y=y_coordinates[i])
                if i == 1:
                    self.__title_label[i].place(x=16, y=y_coordinates[i])

        else:
            self.__title_label = Label(self.__button_frame, text=self._title, font=title_font, bg=self.__title_bg)
            self.__title_label.place(x=x, y=indent_by_y)

        indent_by_y += y_indent_increment[title_size]['writer increment']

        writer_and_issue_year = self._writer + ', ' + str(self._issue_year)
        self.__writer_isuue_year_label = Label(self.__button_frame, font=other_text_font, text=writer_and_issue_year,
                                    bg=self.__background, fg='#262626')
        self.__writer_isuue_year_label.place(x=x, y=indent_by_y)

        indent_by_y += y_indent_increment[title_size]['price increment']

        self.__price_label = Label(self.__button_frame, font=other_text_font, text=self._price, bg=self.__background)
        self.__price_label.place(x=x, y=indent_by_y)

    def destroy(self):
        pass


class CreateItemsGroup:
    def __init__(self,  master, all_items_on_page: tuple, bg: str = 'white', active_bg: str = '#f2f2f2', cursor=None):
        self._all_items_on_page = all_items_on_page

        self._master = master
        self.__bg = bg
        self._active_bg = active_bg

        self.__x = 0
        self.__y = 160

        self.__buttons_group = []
        for i in range(len(self._all_items_on_page)):
            button = self.__create_button(self._all_items_on_page[i])
            self.__buttons_group.append(button)

        for i in range(len(self.__buttons_group)):
            self.__buttons_group[i].place_button()

    def __get_easter_eggs(self):
        self._suns = []

        for item in self._all_items_on_page:
            if item[0] == 1 or item[0] == 2 or item[0] == 19:
                self._suns.append(item)

    def __create_button(self, item) -> ItemButton:
        if self.__x == 1200:
            self.__x = 0
            self.__y += 340

        button = ItemButton(master=self._master, item=item, x=self.__x, y=self.__y, bg=self.__bg,
                            active_bg=self._active_bg)

        self.__x += 300

        return button

    def destroy_group(self):
        for i in range(len(self.__buttons_group)):
            self.__buttons_group[i].destroy()


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


def center_by(master, widget1, center_coordinate: str, correction: Union[list, int] = 0, widget2=None):
    widget1.place(x=0, y=0)
    root.update()

    h1 = widget1.winfo_height()
    w1 = widget1.winfo_width()

    width = master.winfo_width() // 2
    heigh = master.winfo_height() // 2

    center_of_widget1_by_x = w1 // 2
    center_of_widget1_by_y = h1 // 2

    center = {
        'x': width - center_of_widget1_by_x - correction,
        'y': heigh - center_of_widget1_by_y - correction
    }

    if center_coordinate == 'xy':
        return [width - center_of_widget1_by_x - correction[0], heigh - center_of_widget1_by_y - correction[1]]
    return center[center_coordinate]

def init_list_of_items() -> CreateItemsGroup:
    return CreateItemsGroup(master=root, all_items_on_page=all_items, bg=button_bg)


buttons = init_list_of_items()

root.bind('<Button-1>', get_cursor_cords)
root.mainloop()

