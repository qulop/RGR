from tkinter import *
from tkinter import ttk
import storelib
import tkinter.font as font
import sqlrequests
from PIL import Image, ImageTk
import time


root = Tk()     # создаем непосредственно само окно программы

height = root.winfo_screenwidth()   # узнаем ширину экрана
width = root.winfo_screenheight()   # и высоту

height = (height // 2) - 450    # рассчитываем середину экрана (по x-координате)
width_for_main_frame = (width // 2) - 320   # по координате y


main_width = 1200
main_height = 800
geometry_for_main_frame = f'{main_width}x{main_height}+{height}+{width_for_main_frame}'

main_bg = '#4d4d4d'
text_fg = '#b3b3b3'
button_bg = '#666666'   # '#cc5200'
button_ab = '#8c8c8c'
text_label_bg = button_bg
table_bg = '#808080'
lines_fill = '#404040'


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


def where_is_cursor():
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()


def center_widget(widget, locate: str, center_by: str, correction: list = None):
    if locate not in ['bottom', 'top']:
        raise 'locate parameter error'

    if center_by not in ['x', 'y']:
        raise 'center_by parameter error'

    root.update()

    center = {
        'bottom': {
            'x': 600 - (widget.winfo_width() // 2),
            'y': ((642 // 2) + 142) - (widget.winfo_height() // 2)
        },

        'top': {
            'x': 600 - (widget.winfo_width() // 2),
            'y': (158 // 2) - (widget.winfo_height() // 2)
        }
    }

    return center[locate][center_by]


root.geometry(geometry_for_main_frame)
root.resizable(height=False, width=False)
root.title('BC-AC.by')
root.config(bg=main_bg)


class SearchingArea:
    def __init__(self, x, y, area_width):
        self._x = x
        self._y = y
        self.__width = area_width
        self.__loupe_incon = Image.open('icons/icons/loupe.png')
        self.__loupe_incon = self.__resize_image(self.__loupe_incon)


        self._searching_area_width = int(area_width * 0.625)
        self._search_button_width = int(area_width * 0.25)

        self._searching_area = Entry(main_canvas,  border=0, width=self._searching_area_width, bg=button_bg,
                                     highlightthickness=0)
        self._searching_area.place(x=x, y=y)
        self._searching_area.insert(0, 'Поиск по товарам')
        root.update()

        self._search_button = Button(main_canvas, border=0, image=self.__loupe_incon, width=self._search_button_width,
                                     bg='#cc5200', highlightthickness=0, activebackground='#e65c00')
        self._search_button.place(x=733, y=y)


    def ivent_getter(self, event):
        if (event.x >= self._x and event.x <= (self._x + self._searching_area.winfo_width())) and \
        (event.y >= self._y and event.y <= (self._y + self._searching_area.winfo_height())):
            self._searching_area.delete(first=0, last=END)
        print(f'X: {event.x}; Y: {event.y}')
        print(self._x, (self._x + self._searching_area.winfo_width()))
        print(self._y, (self._y + self._searching_area.winfo_height()))

    @staticmethod
    def __resize_image(image):
        image = image.resize((17, 17))
        image = ImageTk.PhotoImage(image)

        return image


class ItemsPlacingTemplate:
    def __init__(self, start_x: int, start_y: int, total_items_quantity: int):
        # self._buttons_list = []
        self.__x = start_x
        self.__y = start_y

    def add_item(self, *args):
        for argument in args:
            self._buttons_list.append(argument)

    def fill_in(self):
        pass


class ItemButton:
    def __init__(self, master, item: tuple = None, **kwargs):
        self.__get_kwargs(kwargs)

        if not item:
            self.title = None
            self.__title_bg = button_ab
            self.writer = None
            self.image = PhotoImage(file='content/icons/template.png')
            self.issue_year = None
            self.rating = None
            self.price = None
        else:
            self.title = item[1]
            self.__title_bg = button_bg
            self.writer = item[2]
            self.image = self.__image_resize(image)
            self.issue_year = issue_year
            self.rating = rating
            self.price = str(price) + ' руб.'

        self.__button_frame = Canvas(master, width=self.__width, height=self.__height, bg=self.__background,
                                     highlightthickness=0)
        # self.__draw_item_frame()
        # self.__button_frame.place(x=self.__x, y=self.__y)
        #
        # self.__image_label = Label(self.__button_frame, image=self.__image)
        # self.__image_label.place(x=30, y=20)

        # root.after(1, self._monitoring_cursor_position)

        # self.__add_text()

    def __get_kwargs(self, kwargs: dict):
        kwargs_list = ['height', 'width', 'x', 'y', 'bg', 'abg', 'cursor']

        user_kwargs = kwargs.keys()
        if len(user_kwargs) > len(kwargs_list):
            raise 'Too many keyword arguments given'

        for argument in user_kwargs:
            if argument not in kwargs_list:
                raise 'Unknown keyword argument'

        if 'x' and 'y' not in user_kwargs:
            raise 'Not specified main coordinates "x" or(and) "y"'
        self.__x = kwargs.get('x')
        self.__y = kwargs.get('y')

        if 'height' in user_kwargs:
            self.__height = kwargs.get('height')
        else:
            self.__height = 340

        if 'width' in user_kwargs:
            self.__width = kwargs.get('width')
        else:
            self.__width = 300

        if 'bg' in user_kwargs:
            self.__background = kwargs.get('bg')
        else:
            self.__background = 'white'

        if 'act_bg' in user_kwargs:
            self.__active_bg = kwargs.get('act_bg')
        else:
            self.__active_bg = '#f2f2f2'

    def __image_resize(self, image):
        im_width, im_height = image.size
        im_width = int(im_width // 3.2)
        im_height = int(im_height // 3.2)

        image = image.resize((141, 218))
        self.__side_indent = (self.__width - image.size[0]) // 2
        image = ImageTk.PhotoImage(image)

        return image

    def __draw_item_frame(self):
        self.__button_frame.create_line(0, 0, 300, 0, width=3)
        self.__button_frame.create_line(0, 337, 300, 337, width=3)

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
        indent_by_y = 245

        self.__draw_item_frame()
        self.__button_frame.place(x=self.__x, y=self.__y)

        self.__image_label = Label(self.__button_frame, image=self.image, bg=button_bg)
        self.__image_label.place(x=30, y=20)

        self.__title_label = Label(self.__button_frame, text=self.title, font=title_font, bg=self.__title_bg)
        self.__title_label.place(x=30, y=indent_by_y)

        indent_by_y += 25

        if not self.writer and not self.issue_year:
            writer_and_issue_year = None
        else:
            writer_and_issue_year = self.writer + ', ' + str(self.issue_year)
        self.__writer_label = Label(self.__button_frame, font=other_text_font, text=writer_and_issue_year,
                                    bg=button_bg, fg='#262626')
        self.__writer_label.place(x=30, y=indent_by_y)

        indent_by_y += 25

        self.__price_label = Label(self.__button_frame, font=other_text_font, text=self.price, bg=button_bg)
        self.__price_label.place(x=30, y=indent_by_y)

    @staticmethod
    def _get_width_and_height(element):
        root.update()

        return [element.winfo_width(), element.winfo_height()]


class ChangeBackground(ItemButton):
    def _add_elements(self, *args):
        self._elements = []
        for element in args:
            self._elements.append(element)

    def _change_bg(self, background):
        for element in self._elements:
            element.config(bg=background)


# class App:
#     def __init__(self, *args: ItemButton):
#         self__error_font = font.Font(size=20, family='Times', weight='bold')
#         self.__database_error_image = PhotoImage(file='icons/icons/database-error.png')
#         self.__database_error_image_label = Label(main_canvas, image=self.__database_error_image, bg=main_bg)
#         self.__database_error_image_text = Label(text="Ошибка подключения к базе данных: ошибка подключения 1-го уровня",
#                                                  font=self__error_font, bg=main_bg)
#         root.update()
#         print(self.__database_error_image_text.winfo_width())
#
#         self.__refresh_icon = Image.open('icons/icons/refresh.png')
#         self.__refresh_icon = self.__refresh_icon.resize((35, 35))
#         self.__refresh_icon = ImageTk.PhotoImage(self.__refresh_icon)
#         self.__refresh_button = Button(image=self.__refresh_icon, highlightthickness=0, border=0, relief=RIDGE,
#                                        bg=main_bg, activebackground=button_ab, command=self._refresh)
#
#         self.__items = []
#         for argument in args:
#             self.__items.append(argument)
#
#         self.__psql = SQLrequests.PsqlRequests()
#         if not self.__psql.connect(password="Y5n1e887k69"):
#             self._place_widgets()
#         else:
#             self._place_items()
#
#     def _place_widgets(self):
#         self.__database_error_image_label.place(x=438, y=225)
#         self.__database_error_image_text.place(x=122, y=570)    # 165
#         self.__refresh_button.place(x=1022, y=565)
#
#     def _refresh(self):
#         self.__database_error_image_label.destroy()
#         self.__database_error_image_text.destroy()
#         self.__refresh_button.destroy()
#
#         animation = Amy()
#
#     def _place_items(self):
#         for item in self.__items:
#             item.place_button()


class Amy:
    def __init__(self):
        self.filename = 'content/icons/refresh.png'
        self.canvas = Canvas(root, width=50, height=50, bg=main_bg, highlightthickness=0)
        self.canvas.place(x=445, y=350)

        self.__font = font.Font(size=30, family='Times', weight='bold')
        self.__update_text = Label(text='обновление...', font=self.__font, bg=main_bg)
        self.__update_text.place(x=517, y=356)
        self.__angle = 0
        self.__full_revolutions = 0


        self.process_next_frame = self.draw().__next__  # Using "next(self.draw())" doesn't work
        root.after(1, self.process_next_frame)

    def draw(self):
        image = Image.open(self.filename).resize((45, 45))
        print(self.process_next_frame)
        while 1:
            tkimage = ImageTk.PhotoImage(image.rotate(self.__angle))
            canvas_obj = self.canvas.create_image(25, 25, image=tkimage)
            root.after_idle(self.process_next_frame)
            yield
            self.canvas.delete(canvas_obj)
            self.__angle += 1
            self.__angle %= 360
            if self.__angle >= 90:
                time.sleep(0.000001)
            else:
                time.sleep(0.002)

            if self.__angle == 359:
                print('Amy, stop be angry to me pls')
                self.__full_revolutions += 1

            if self.__full_revolutions == 4:
                # self._place_widgets()
                raise StopIteration

# b1984 = Image.open('icons/item-photo/1984.jpg')
# j = Image.open('icons/item-photo/dr-jivago.jpg')
# s = Image.open('icons/item-photo/spire.jpeg')
# sh = Image.open('icons/item-photo/short-answers.png')
#
#
# A = SearchingArea(x=235, y=25, area_width=100)
# icon = PhotoImage(file='icons/icons/database-error.png')
# icon = icon.resize((312, 304))
# icon = ImageTk.PhotoImage(icon)
# a = ItemButton(main_canvas, '1984', 'Джордж Оруэлл', b1984, 2021, 4.5, 9.8, x=0, y=160, bg=button_bg)
# b = ItemButton(main_canvas, 'Доктор Живаго', 'Борис Пастернак', j, 2019, 4.4, 15, x=300, y=160, bg=button_bg)
# c = ItemButton(main_canvas, 'Шпиль', 'Уильям Голдинг', s, 2018, 4.4, 7.6, x=600, y=160, bg=button_bg)
# d = ItemButton(main_canvas, 'Краткие ответы на большие вопросы', 'Стивен Хокинг', sh, 2021, 4.4, 22,
#                    x=900, y=160, bg=button_bg)

app = storelib.App(root, main_height, main_width, main_bg, button_bg, button_ab)
a = ItemButton(root, x=0, y=160, bg=button_bg)
a.place_button()


root.after(60, where_is_cursor)
root.bind('<Button-1>', get_cursor_cords)
root.mainloop()






