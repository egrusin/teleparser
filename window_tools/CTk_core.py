__all__ = ['MainWin', 'MainInterface']

import tkinter as tk
import customtkinter as ctk
import ctypes


# ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")
INTERFACE_COLOR = '#9000ff'
SECOND_COLOR = '#a600ff'


class PageObject:
    """Класс страницы сценария. Представляет собой шаблон и инструменты для создания эелеменов сценария"""
    def __init__(self, master: ctk.CTk | tk.Tk, size: tuple) -> None:
        self.__master = master      # Объект окна для наполнения
        self.__size = size          # Размер окна в формате (x, y)
        self.__init_objs = []       # Список инициализации объектов
        self.__place_objs = []      # Список размещенных объектов

    def add_element(self, element) -> None:
        """Метод для добавления элемента в init_objs.
        Принимает кортеж формата (element: ctk.CTkLabel | ..., coords: {'x': 123, 'y': 123})."""
        self.__init_objs.append(element)

    def add_elements(self, elements) -> None:
        """Декоратор для добавления элементов в init_objs.
        Принимает список кортежей формата [(element: ctk.CTkLabel | ..., coords: {'x': 123, 'y': 123}), ...]."""
        self.__init_objs.extend(elements)

    def clear(self):
        """Метод для удаления всех элементов со страницы"""
        if self.__place_objs:
            for item in self.__place_objs:
                item.destroy()

    def build_page(self) -> None:
        """Декоратор для добавления элементов в place_objs и расположении их на главном окне.
        Принимает кортеж формата (element: ctk.CTkLabel | ..., coords: {'x': 123, 'y': 123})."""
        if self.__init_objs:
            for elem in self.__init_objs:
                elem[0].place(**elem[1])
                self.__place_objs.append(elem[0])

    @property
    def size(self):
        """Метод для получения размера окна"""
        return self.__size

    @property
    def master(self):
        """Метод для получения объекта окна"""
        return self.__master


class LinkedPageObject(PageObject):
    """Класс-расширение базового для реализации функцианола связного графа приложения"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link = None        # Список конфигурируемых объектов (кнопки) для перехода по сценарию

    def init_link(self, button: ctk.CTkButton | tk.Button) -> None:
        """Метод для добавления кнопки перехода в список"""
        self.__link = button

    def build_link(self, func: callable):
        self.__link.configure(command=func)

    def execute_link(self):
        pass


class SessionPage(LinkedPageObject):
    def __init__(self, master, size):
        super().__init__(master, size)
        self.session_name = tk.StringVar()

    def init_page(self):
        name_session = ctk.CTkLabel(self.master,
                                    text='Введите Ваше имя',
                                    text_color=(INTERFACE_COLOR, SECOND_COLOR),
                                    corner_radius=5)
        name_session_coords = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 100)

        session_entry = ctk.CTkEntry(self.master,
                                     textvariable=self.session_name,
                                     placeholder_text='89991234567',
                                     text_color=INTERFACE_COLOR)
        session_entry_coords = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 80)

        get_name_button = ctk.CTkButton(self.master,
                                         command=self.get_session_name,
                                         text='Войти',
                                         fg_color=INTERFACE_COLOR,
                                         hover_color=SECOND_COLOR)
        get_name_button_coods = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 10)

        self.add_elements([(name_session, name_session_coords),
                           (session_entry, session_entry_coords),
                           (get_name_button, get_name_button_coods)])

        self.init_link(get_name_button)

    def get_session_name(self):
        print(self.session_name.get())
        self.clear()


class LoginPage(LinkedPageObject):
    def __init__(self, master, size):
        super().__init__(master, size)
        self.phone_number = tk.StringVar()
        self.auth_code = tk.StringVar()

    def init_page(self):
        phone_label = ctk.CTkLabel(self.master,
                                   text='Введите номер телефона',
                                   text_color=(INTERFACE_COLOR, SECOND_COLOR),
                                   corner_radius=5)
        phone_label_coords = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 100)

        phone_entry = ctk.CTkEntry(self.master,
                                   textvariable=self.phone_number,
                                   placeholder_text='89991234567',
                                   text_color=INTERFACE_COLOR)
        phone_entry_coords = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 80)

        get_phone_button = ctk.CTkButton(self.master,
                                         command=self.get_phone,
                                         text='Отправить',
                                         fg_color=INTERFACE_COLOR,
                                         hover_color=SECOND_COLOR)
        get_phone_button_coords = dict(x=self.size[0] // 2 - 70, y=self.size[1] // 2 - 10)
        self.add_elements([(phone_label, phone_label_coords),
                           (phone_entry, phone_entry_coords),
                           (get_phone_button, get_phone_button_coords)])
        self.init_link(get_phone_button)

    def get_phone(self):
        print(self.phone_number.get())
        self.clear()


class MainWin:
    def __init__(self):
        self.__monitor_size = self.__get_monitor_size()
        self.__size = (500, 700)
        self.__win = ctk.CTk()
        self.customize()
        # self.frame = SessionPage(self.__win, self.__size)   Вынести на уровень выше
        # self.frame.fill_page()

    @staticmethod
    def __get_monitor_size():
        """Возвращает размены экрана"""
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    def customize(self):
        """Задает главному окну необходимые параметры, задает нестираемый заголовок"""
        width, height = self.__size
        w, h = self.__monitor_size
        x = (w - width) // 2
        y = (h - height - 300) // 2

        self.__win.geometry(f'{width}x{height}+{x}+{y}')
        self.__win.title('Teleparser')
        self.__win.grid_rowconfigure(1, weight=0)
        self.__win.grid_columnconfigure(1, weight=0)

        label = ctk.CTkLabel(self.__win,
                             text='TELEPARSER',
                             font=('Arial', 30),
                             text_color=(INTERFACE_COLOR, SECOND_COLOR),
                             corner_radius=5)
        label.place(x=self.__size[0] // 2 - 100, y=0)

    def work(self):
        self.__win.mainloop()

    def read(self):
        return self.__win, self.__size


class MainInterface:
    """Класс-фабрика для управления и создания окна приложения"""
    def __init__(self):
        self.window = MainWin()
        self.head = None

    def add_page(self, obj, link_rule=None):
        """Метод для добавления страницы в граф."""
        if self.head is None:
            self.head = obj
            obj.build_link(link_rule)

    def run(self):
        self.head.build_page()
        self.window.work()


if __name__ == '__main__':

    gui = MainInterface()                             # Создаем объект окна, настраиваем его

    ses = SessionPage(*gui.window.read())             # Создаем объекты страниц
    ses.init_page()
    log = LoginPage(*gui.window.read())
    log.init_page()

    def go_link():
        ses.clear()
        log.build_page()

    gui.add_page(ses, link_rule=go_link)       # Упорядочиваем и связываем страницы
    gui.run()
    # win = MainWin()
    # win.work()



def check_monitor_size():
    win = ctk.CTk()
    print(win.winfo_screenwidth(), win.winfo_screenheight())


def scroll():
    app = ctk.CTk()
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    # create scrollable textbox
    tk_textbox = ctk.CTkTextbox(app, activate_scrollbars=False)
    tk_textbox.grid(row=0, column=0, sticky="nsew")

    # create CTk scrollbar
    ctk_textbox_scrollbar = ctk.CTkScrollbar(app, command=tk_textbox.yview)
    ctk_textbox_scrollbar.grid(row=0, column=1, sticky="we")

    # connect textbox scroll event to CTk scrollbar
    tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    app.mainloop()


def scroll1():
    class MyFrame(ctk.CTkScrollableFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            # add widgets onto the frame...
            self.label = ctk.CTkLabel(self)
            self.label.grid(row=0, column=0, padx=20)

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
            self.my_frame.grid(row=0, column=0, sticky="nsew")

    app = App()

    def segmented_button_callback(value):
        print("segmented button clicked:", value)

    segemented_button_var = ctk.StringVar(value="Value 1")
    segemented_button = ctk.CTkSegmentedButton(app, values=["Value 1", "Value 2", "Value 3"],
                                                    command=segmented_button_callback,
                                                    variable=segemented_button_var)
    segemented_button.place(x=0, y=0)

    app.mainloop()
