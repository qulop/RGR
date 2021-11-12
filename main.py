from tkinter import *
import tkinter.font as font

'''
режимы доступа в Python (синтаксис): 
    1) с двумя подчеркиваниями перед именем пер-й (self.__PerName) - режим доступа private;
    2) с одним (self._PerName) - protected;
    3) без подчеркиваний - public.
'''

root = Tk()     # создаем непосредственно само окно программы


height = root.winfo_screenwidth()   # узнаем ширину экрана
width = root.winfo_screenheight()   # и высоту

height = (height // 2) - 450    # рассчитываем середину экрана (по x-координате)
width_for_main_frame = (width // 2) - 320   # по координате y

geometry_for_main_frame = f'900x600+{height}+{width_for_main_frame}'

main_bg = '#4d4d4d'
text_fg = '#b3b3b3'
button_bg = '#666666'
button_ab = '#8c8c8c'  # ab - (active background)
text_label_bg = button_bg
table_bg = '#808080'
lines_fill = '#404040'
#   ^ - цвета для конкретных элементов (областей) приложения


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


class MainScreen:
    def __init__(self):
        pass

    def __add_content_to_frame(self):
        pass

    def place(self):
        pass

class StatisticScreen:
    def __init__(self, root):
        self.__root = root
        self. __frame = None
    
    def destroy_frame(self):
        pass

    def __add_content_to_frame(self):
        pass

    def place(self):
        pass

class Table:
    def __init__(self, **kwargs):
        height_of_label = 21
        width_of_label = 12

        if len(kwargs) > 7:
            raise 'too many keyword arguments'

        available_keys = ['columns', 'rows', 'height', 'width', 'frame_x', 'frame_y', 'root']
        keys = kwargs.keys()

        for key in keys:
            if key not in available_keys:
                raise 'unidentified key'

        self.__column_quantity = kwargs.get('columns')
        self.__row_quantity = kwargs.get('rows')

        self.__width = kwargs.get('width')
        self.__height = kwargs.get('height')

        if kwargs.get('frame_x') or kwargs.get('frame_y'):
            if not kwargs.get('frame_x'):
                raise 
        self.__frame_x = kwargs.get('frame_x')
        self.__frame_y = kwargs.get('frame_y')
        self.__root = root

        self.__frame = Canvas(self.__root, width=self.__width, height=self.__height, bg=table_bg, highlightthickness=0)

        line_height = self.__height * 0.04
        self.__frame.create_line(0, 0, self.__width, 0, width=line_height, fill=lines_fill)
        self.__frame.create_line(0, self.__height, self.__width, self.__height, width=line_height, fill=lines_fill)

        self.__frame.place(x=self.__frame_x, y=self.__frame_y)

    def place(self):
        column_step = self.__width / self.__column_quantity
        row_step = self.__height / self.__row_quantity

        for step in range(1, self.__column_quantity+1):
            step *= column_step
            self.__frame.create_line(step, 0, step, self.__height, width=2, fill=lines_fill)

        for step in range(1, self.__row_quantity+1):
            step *= row_step
            self.__frame.create_line(0, step, self.__width, step, width=2, fill=lines_fill)


root.geometry(geometry_for_main_frame)
root.resizable(height=False, width=False)
root.title('*app title*')
root.config(bg=main_bg)
a = Table(columns=10, rows=5, height=200, width=720, frame_x=45, frame_y=20, root=root)

root.bind('<Button-1>', get_cursor_cords)
root.mainloop()






