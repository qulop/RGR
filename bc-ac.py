import PIL.Image
import PIL.ImageTk
import tkinter.font
import tkinter.ttk as ttk
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
root.title('BC-AVC.by')
root.config(bg=main_bg)

postgres_cursor = sqlrequests.PsqlRequests()
all_items = postgres_cursor.select(from_to_take='item', what_to_take=['item.*', 'writer.full_name', 'item_photo.path'],
                                   join=[['writer', 'writer_id'], ['item_photo', 'photo_id']],
                                   select_exceptions=['item.writer_id', 'item.photo_id'])


def center_by(widget, center_coordinate: str, master=None, center_in_area: list = None, correction: list = [0, 0]):
    widget.place(x=0, y=0)
    root.update()

    h1 = widget.winfo_height()
    w1 = widget.winfo_width()


    if center_in_area:
        width = center_in_area[0]
        heigh = center_in_area[1]
    else:
        width = master.winfo_width()
        heigh = master.winfo_height()

    center = {
        'x': (width - w1) // 2 - correction[0],
        'y': (heigh - h1) // 2 - correction[1]
    }

    if center_coordinate == 'xy':
        return [center['x'], center['y']]
    return center[center_coordinate]


def place_widget_n_pxls_from_another(master, parent_widget, space: int, parent_x: int) -> int:
    master.update()
    widget_width = parent_widget.winfo_width()
    return parent_x + widget_width + space


class App:
    def __init__(self, master):
        self._master = master

        self._master.update()

        self._load_screen = Frame(self._master, bg=main_bg, width=self._master.winfo_width(),
                                  height=self._master.winfo_height())
        self._load_screen.pack()
        self._loading = Label(self._load_screen, text='Загрузка...', font=font.Font(size=35), bg=main_bg)
        x, y = center_by(self._loading, 'xy', master=self._master)
        self._loading.place(x=463, y=370)

        self._canvas = Canvas(self._master, width=self._master.winfo_width(), height=self._master.winfo_height(),
                              bg=main_bg, highlightthickness=0)
        self._canvas.pack()

        self._canvas.create_line(0, 160, 1200, 160, width=3)

        label = Label(self._canvas, text='Вы можете продать нам свои книги', bg=main_bg,
                      font=font.Font(size=15, underline=True))
        x = center_by(label, 'x', self._canvas, correction=[60, 0])

        self._add_new_book = Button(text='подробнее', bg=main_bg, activebackground=button_ab, bd=0,
                              font=font.Font(size=14), command=AddEntryToDB)

        self.__toggle_open = PIL.Image.open('content/icons/toggle_open.png')
        self.__toggle_open = self.__toggle_open.resize((60, 60))
        self.__toggle_open = PIL.ImageTk.PhotoImage(self.__toggle_open)

        self._toggle_open_btn = Button(self._canvas, image=self.__toggle_open, bg=main_bg, activebackground=main_bg
                                       , highlightthickness=0, bd=0, relief=RIDGE, command=self.__toggle_menu)
        self._toggle_open_btn.place(x=1130, y=10)

        self.__add_searchbar(area_width=85)
        self._items = self.__init_items_list()

        self._load_screen.destroy()

        x = center_by(label, 'x', self._canvas, correction=[60, 0])
        label.place(x=x, y=70)
        x = place_widget_n_pxls_from_another(self._canvas, label, space=10, parent_x=x)
        self._add_new_book.place(x=x, y=66)

    def __init_items_list(self):
        return CreateItemsGroup(master=self._canvas, all_items_on_page=all_items, bg=button_bg)

    def __add_searchbar(self, area_width):
        width = area_width
        loupe_icon = PIL.Image.open('content/icons/loupe.png')
        loupe_icon = loupe_icon.resize((17, 17))
        self._loupe_icon = PIL.ImageTk.PhotoImage(loupe_icon)

        area_width = int(width * 0.625)
        button_width = int(width * 0.25)

        self._searching_area = Entry(self._canvas,  border=0, width=area_width, bg=button_bg,
                                     highlightthickness=0)
        area_x = center_by(self._searching_area, 'x', center_in_area=[1200, 160]) - 5
        self._searching_area.place(x=area_x, y=20)
        self._search_button = Button(self._canvas, border=0, image=self._loupe_icon, width=button_width,
                                        bg='#cc5200', highlightthickness=0, activebackground='#e65c00',
                                        command=self._search)
        self._search_button.place(x=(area_x + self._searching_area.winfo_width() + 5), y=20)

    def _search(self):
        request = self._searching_area.get().lower()

        replace_to_suns = {
            'эми': 'эмма',
            'клара': 'клара и солнце',
            'вика': 'виктория. пан',
            'виктория': 'виктория. пан'
        }
        if request in replace_to_suns.keys():
            request = replace_to_suns[request]

        if not request.strip():
            return

        coincidences = []

        server_answer = postgres_cursor.execute('SELECT item.id, LOWER(item.title), LOWER(item.genre), LOWER(writer.full_name) FROM item JOIN writer ON item.writer_id = writer.id;')

        for elemnt in server_answer:
            for i in range(1, 4):
                if request in elemnt[i]:
                    coincidences.append(elemnt[0])
                    break

        if len(coincidences) == 0:
            self.__nothing_found()
            return

        items = postgres_cursor.select(from_to_take='item',
                                        what_to_take=['item.*', 'writer.full_name', 'item_photo.path'],
                                        select_exceptions=['item.writer_id', 'item.photo_id'],
                                        join=[['writer', 'writer_id'], ['item_photo', 'photo_id']],
                                        where=['item.id', coincidences])


        self._items.destroy_group()
        self._items = CreateItemsGroup(self._canvas, items=items, bg=button_bg)

    def __nothing_found(self):
        self._items.destroy_group()

        loupe = PIL.Image.open('content/icons/nothing-found.png')
        loupe = loupe.resize((250, 250))
        loupe = PIL.ImageTk.PhotoImage(loupe)
        error_icon = self._canvas.create_image(600, 300, image=loupe)
        # errot_message = self._canvas.create_text(600, 350, text='Упс! Ничего не найдено!', font=font.Font(size=15))

        # self.label = Label(image=self.__loupe, bg=main_bg).place(relx=0.5, y=400)



    def __toggle_menu(self):
        self.__toggle_bg = '#808080'
        self.__toggle_canv = Canvas(self._master, width=400, height=self._master.winfo_height(),
                              bg=self.__toggle_bg, highlightthickness=0)
        self.__toggle_canv.place(x=800, y=0)

        self.__toggle_close = PIL.Image.open('content/icons/toggle_close.png')
        self.__toggle_close = self.__toggle_close.resize((50, 30))
        self.__toggle_close = PIL.ImageTk.PhotoImage(self.__toggle_close)

        self._close_btn = Button(self.__toggle_canv, image=self.__toggle_close, bg=self.__toggle_bg,
                                 activebackground=self.__toggle_bg, highlightthickness=0,
                                 bd=0, relief=RIDGE, command=self.__toggle_canv.destroy)
        self._close_btn.place(x=340, y=10)

        self.__generate_content_for_toggle_menu()
        self.__add_content_to_toggle_menu()

    def __generate_content_for_toggle_menu(self):
        titles = {
            0: 'Автор:',
            1: 'Год издания:',
            2: 'Жанр:',
            3: 'Цена:'
        }

        self.__titles_on_toggle = []
        for i in range(4):
            template = Label(self.__toggle_canv, text=titles[i], font=font.Font(size=15), bg=self.__toggle_bg)
            self.__titles_on_toggle.append(template)

        writers = postgres_cursor.select(from_to_take='writer', what_to_take=['writer.full_name'],
                                         order_by='full_name')
        issue_years = postgres_cursor.select(from_to_take='item', what_to_take=['item.issue_year'],
                                             distinct=True, order_by='item.issue_year', desc=True)
        genres = postgres_cursor.select(from_to_take='item', what_to_take=['item.genre'], distinct=True,
                                        order_by='item.genre')

        authors_remainder = len(writers) - 3
        issue_years_remainder = len(issue_years) - 3
        genres_remainder = len(genres) - 3

        self.__writer_checkbtns = []
        self.__issue_year_checkbtns = []
        self.__genre_checkbtns = []
        for i in range(3):
            v1 = BooleanVar()
            v1.set(False)

            v2 = BooleanVar()
            v2.set(False)

            v3 = BooleanVar()
            v3.set(False)

            writer = Checkbutton(self.__toggle_canv, text=writers[i][0], variable=v1, onvalue=1, offvalue=0,
                                 bg=self.__toggle_bg, activebackground=self.__toggle_bg, highlightthickness=0,
                                 font=font.Font(size=13))
            issue_year = Checkbutton(self.__toggle_canv, text=issue_years[i][0], variable=v2, onvalue=1, offvalue=0,
                                     bg=self.__toggle_bg, activebackground=self.__toggle_bg, highlightthickness=0,
                                     font=font.Font(size=13))
            genre = Checkbutton(self.__toggle_canv, text=genres[i][0], variable=v3, onvalue=1, offvalue=0,
                                bg=self.__toggle_bg, activebackground=self.__toggle_bg, highlightthickness=0,
                                font=font.Font(size=13))
            print((writer['text']))

            self.__writer_checkbtns.append(writer)
            self.__issue_year_checkbtns.append(issue_year)
            self.__genre_checkbtns.append(genre)

        self.__comboboxes= []
        writers = [writer[0] for writer in writers]

        for list_ in [writers[4:], issue_years[4:], genres[4:]]:
            selected_line = StringVar()
            template = ttk.Combobox(self.__toggle_canv, values=list_, textvariable=selected_line)
            template['state'] = 'readonly'

            self.__comboboxes.append(template)

        #     def ivent_getter(self, event):
        #         if (event.x >= self._x and event.x <= (self._x + self._searching_area.winfo_width())) and \
        #         (event.y >= self._y and event.y <= (self._y + self._searching_area.winfo_height())):
        #             self._searching_area.delete(first=0, last=END)
        #         print(f'X: {event.x}; Y: {event.y}')
        #         print(self._x, (self._x + self._searching_area.winfo_width()))
        #         print(self._y, (self._y + self._searching_area.winfo_height()))

    def __add_content_to_toggle_menu(self):
        Label(self.__toggle_canv, text='Расширенный поиск', font=font.Font(size=17),
              bg=self.__toggle_bg).place(anchor='n', relx=0.5, y=35)
        self.__toggle_canv.create_line(0, 70, 400, 70, width=3)
        checkbtns_lists = [self.__writer_checkbtns, self.__issue_year_checkbtns, self.__genre_checkbtns]

        y = 80 # 115
        for i in range(3):
            self.__titles_on_toggle[i].place(x=30, y=y)
            y += 35

            for button in checkbtns_lists[i]:
                button.place(x=60, y=y)
                y += 40

            self.__comboboxes[i].place(x=65, y=y)

            y += 30

        reset = Button(self.__toggle_canv, text='Сбросить настройки', bg=self.__toggle_bg,
                       activebackground=button_ab, bd=0)
        reset.place(anchor='sw', x=15, y=770)

        search = Button(self.__toggle_canv, text='Поиск', bg=self.__toggle_bg,
                       activebackground=button_ab, bd=0, command=self.__extended_search_onclick)
        search.place(anchor='se', x=380, y=770)

        # for title in self.__titles_on_toggle:
        #     title.place(x=30, y=y)

    def __extended_search_onclick(self):
        writers_request = []
        issue_years_request = []
        genres_request = []

        for btn in self.__writer_checkbtns:
            print(btn['variable'].get())


class AddEntryToDB:
    def __init__(self):
        self._win = Toplevel()
        self._win.geometry(f'600x400+{height}+{width_for_main_frame}')
        self._win.resizable(width=False, height=False)
        self._win.title('Заявка на продажу')
        self._win.config(bg=main_bg)

        self._canv = Canvas(self._win, width=600, height=400, highlightthickness=0, bg=main_bg)
        self._canv.pack()
        self._canv.create_line(0, 70, 600, 70, width=2)

        title_font = font.Font(size=20, family='Times', slant='roman')
        head_title = Label(self._canv, text='<<Throw old, get new>>', bg=main_bg, font=title_font)
        x, y = center_by(center_in_area=[600, 70], widget=head_title, center_coordinate='xy')
        head_title.place(x=x, y=y)

        self.__create_titles_fields()
        self.__create_entry_fields()

        label = Label(self._canv, text='Заявка будет рассмотрена в течении недели',
              font=font.Font(size=12), bg=main_bg)
        label.place(x=20, y=360)

        self.__send_application = Button(self._canv, text='Отправить заявку', font=font.Font(size=12), bg=button_bg,
                                         activebackground=button_ab, highlightthickness=0, bd=0,
                                         command=self.__add_info_to_database)

        x = place_widget_n_pxls_from_another(self._win, label, space=15, parent_x=20)
        self.__send_application.place(x=x, y=356)

    def __create_titles_fields(self):
        self._titles_list = []

        titles = {
            0: 'Укажите название(обязательно):',
            1: 'Имя автора(обязательно):',
            2: 'Год издания:',
            3: 'Жанр(обязательно):',
            4: 'Цену, за которую хотели бы продать(руб.):',
        }

        for i in range(5):
            template = Label(self._win, text=titles[i], font=font.Font(size=13), bg=main_bg)
            self._titles_list.append(template)

        y = 85
        for i in range(len(self._titles_list)):
            self._titles_list[i].place(x=20, y=y)

            self._win.update()
            if i == len(self._titles_list) - 1:
                self._canv.create_line(0, y + self._titles_list[i].winfo_height() + 10, 600,
                                       y + self._titles_list[i].winfo_height() + 10, width=2)
            else:
                self._canv.create_line(0, y+self._titles_list[i].winfo_height()+10, 600,
                                   y+self._titles_list[i].winfo_height()+10)
            y += 55

    def __create_entry_fields(self):
        self._entry_list = []

        for i in range(5):
            template = Entry(self._win, bg=button_bg, border=0, highlightthickness=0)
            self._entry_list.append(template)

        y = 89
        for i in range(len(self._entry_list)):
            x = 20 + self._titles_list[i].winfo_width() + 5
            width = 600 - x - 10

            self._entry_list[i].config(width=width)
            self._entry_list[i].place(x=x, y=y)

            y += 55

    def __add_info_to_database(self):
        pass


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
        for i in range(upper_iteration_index-1, 0, -1):
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
        self.__button_frame.destroy()


class CreateItemsGroup:
    def __init__(self,  master, all_items_on_page: tuple = None, bg: str = 'white',
                 active_bg: str = '#f2f2f2', items: tuple = None):
        if items:
            self._items = items
        else:
            self._items = all_items_on_page

        self._master = master
        self.__bg = bg
        self._active_bg = active_bg

        self.__x = 0
        self.__y = 160

        self.__buttons_group = []
        for i in range(len(self._items)):
            button = self.__create_button(self._items[i])
            self.__buttons_group.append(button)

        for i in range(len(self.__buttons_group)):
            self.__buttons_group[i].place_button()

    def __get_easter_eggs(self):
        self._suns = []

        for item in self._items:
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


def add_line_to_database():
    win = Toplevel()
    win.geometry('600x400')
    win.resizable(width=False, height=False)
    win.title('Продать книгу')
    win.config(bg=main_bg)

    canv = Canvas(win, width=600, height=400, highlightthickness=0, bg=main_bg)
    canv.pack()
    canv.create_line(0, 70, 600, 70, fill='black', width=2)

    title_font = font.Font(size=15, family='Times', slant='roman')
    head_title = Label(canv, text='Здесь вы можете продать свои книги.', bg=main_bg, font=title_font)
    x, y = center_by(center_in_area=[600, 70], widget=head_title, center_coordinate='xy')
    head_title.place(x=x, y=y)

    Label(win, text='Укажите имя автора(обязательно): ', font=font.Font(size=12), bg=main_bg).place(x=20, y=100)


app = App(root)

root.bind('<Button-1>', get_cursor_cords)
root.mainloop()
