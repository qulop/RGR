from tkinter import *
from tkinter import ttk
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


root.geometry(geometry_for_main_frame)
root.resizable(height=False, width=False)
root.title('BC-AC.by')
root.config(bg=main_bg)

# class SearchingArea:
#     def __init__(self, x, y, area_width):
#         self._x = x
#         self._y = y
#         self.__width = area_width
#         self.__loupe_incon = Image.open('icons/icons/loupe.png')
#         self.__loupe_incon = self.__resize_image(self.__loupe_incon)
#
#
#         self._searching_area_width = int(area_width * 0.625)
#         self._search_button_width = int(area_width * 0.25)
#
#         self._searching_area = Entry(main_canvas,  border=0, width=self._searching_area_width, bg=button_bg,
#                                      highlightthickness=0)
#         self._searching_area.place(x=x, y=y)
#         self._searching_area.insert(0, 'Поиск по товарам')
#         root.update()
#
#         self._search_button = Button(main_canvas, border=0, image=self.__loupe_incon, width=self._search_button_width,
#                                      bg='#cc5200', highlightthickness=0, activebackground='#e65c00')
#         self._search_button.place(x=733, y=y)
#
#
#     def ivent_getter(self, event):
#         if (event.x >= self._x and event.x <= (self._x + self._searching_area.winfo_width())) and \
#         (event.y >= self._y and event.y <= (self._y + self._searching_area.winfo_height())):
#             self._searching_area.delete(first=0, last=END)
#         print(f'X: {event.x}; Y: {event.y}')
#         print(self._x, (self._x + self._searching_area.winfo_width()))
#         print(self._y, (self._y + self._searching_area.winfo_height()))
#
#     @staticmethod
#     def __resize_image(image):
#         image = image.resize((17, 17))
#         image = ImageTk.PhotoImage(image)
#
#         return image



# class ChangeBackground(ItemButton):
#     def _add_elements(self, *args):
#         self._elements = []
#         for element in args:
#             self._elements.append(element)
#
#     def _change_bg(self, background):
#         for element in self._elements:
#             element.config(bg=background)


class App:
    def __init__(self):
        self.__error_font = font.Font(size=20, family='Times', weight='bold')
        self.__database_error_image = PhotoImage(file='content/icons/database-error.png')
        self.__database_error_image_label = Label(root, image=self.__database_error_image, bg=main_bg)
        self.__database_error_image_text = Label(text="Ошибка подключения к базе данных: ошибка подключения 1-го уровня",
                                                 font=self.__error_font, bg=main_bg)
        root.update()
        print(self.__database_error_image_text.winfo_width())

        self._refresh_icon = Image.open('content/icons/refresh.png')
        self._refresh_icon = self._refresh_icon.resize((35, 35))
        self._refresh_icon = ImageTk.PhotoImage(self._refresh_icon)
        self.__refresh_button = Button(image=self._refresh_icon, highlightthickness=0, border=0, relief=RIDGE,
                                       bg=main_bg, activebackground=main_bg, command=self._refresh)

        self.__psql = sqlrequests.PsqlRequests()
        if not self.__psql.IS_CONNECT:
            self._database_connect_error()
        else:
            self._place_items()

    def _database_connect_error(self):
        self.__database_error_image_label.place(x=438, y=225)
        self.__database_error_image_text.place(x=122, y=570)    # 165
        self.__refresh_button.place(x=1022, y=565)

    def _refresh(self):
        self.__database_error_image_label.destroy()
        self.__database_error_image_text.destroy()
        self.__refresh_button.destroy()
        Amy()

    def _place_items(self):
        pass


class Amy(App):
    def __init__(self):
        App.__init__(self)
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
        image = Image.open(self._refresh_icon).resize((45, 45))
        print(self.process_next_frame)
        while 1:
            tkimage = ImageTk.PhotoImage(image.rotate(self.__angle))
            canvas_obj = self.canvas.create_image(25, 25, image=tkimage)
            root.after_idle(self.process_next_frame)
            yield
            self.canvas.delete(canvas_obj)
            self.__angle += 1
            self.__angle %= 360
            time.sleep(0.001)
            # if self.__angle >= 90:
            #     time.sleep(0.0001)
            # else:
            #     time.sleep(0.000000002)
            #
            # if self.__angle == 359:
            #     self.__full_revolutions += 1
            #
            # if self.__full_revolutions == 4:
            #     # self._place_widgets()
            #     raise StopIteration


app = App()

root.bind('<Button-1>', get_cursor_cords)
root.mainloop()






