from tkinter import *
from tkinter import messagebox as mb
from wheel import RandomWheel


class MainWindow(Tk):
    def __init__(self, start_values: tuple[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = start_values
        assert len(self._values) > 0

        self.__init_settings()
        self.__create_widgets()
        self.__place_widgets()

    def __init_settings(self):
        self.title('Случайное колесо Лукаса')
        self.resizable(False, False)

    def __create_widgets(self):
        handle_func = lambda m: mb.showinfo('Результат', f'Выпал сектор "{m}"')
        self._wheel = RandomWheel((188, 140), 100, handle_func, (300, 700), self._values, self)
        self._launch_button = Button(self, text='Вращать', command=lambda: self._wheel.launch(30, 0.1))
        
        self._lb_frame = Frame(self)
        self._values_list = Listbox(self._lb_frame, listvariable=self._values)
        self._lb_entry = Entry(self._lb_frame)

        self._lb_apply_button = Button(self._lb_frame, text='Применить', command=self.__choise_values)
        self._lb_add_button = Button(self._lb_frame, text='Добавить', command=self.__add)
        self._lb_remove_but = Button(self._lb_frame, text='Убрать', command=self.__remove)

        self._wheel.flip_wheel_state()

    def __place_widgets(self):
        glob = dict(sticky=NSEW)

        self._wheel.grid(column=0, row=0, **glob)
        self._launch_button.grid(column=0, row=1, **glob)
        
        self._lb_frame.grid(column=1, row=0, rowspan=2, **glob)
        self._values_list.grid(column=0, row=0, columnspan=2, **glob)
        self._lb_entry.grid(column=0, row=1, columnspan=2, **glob)
        self._lb_add_button.grid(column=0, row=2, **glob)
        self._lb_remove_but.grid(column=1, row=2, **glob)
        self._lb_apply_button.grid(column=0, row=3, columnspan=2, **glob)
    
    def __add(self):
        text = self._lb_entry.get()

        if text:
            self._values_list.insert(0, text)
            self._lb_entry.delete(0, END)
        else:
            mb.showwarning('Внимание', 'Сначала введите текст в поле.')

    def __remove(self):
        index = self._values_list.curselection()

        if index:
            self._values_list.delete(index)
        else:
            mb.showwarning('Внимание', 'Сначала выберите элемент в списке.')

    def __choise_values(self):
        values = self._values_list.get(0, END)

        if len(values) > 0:
            self._wheel.set_values(values)
            self._wheel.flip_wheel_state()
        else:
            mb.showwarning('Внимание', 'Нельзя использовать пустой список.')


def main():
    win = MainWindow(('A', 'B', 'C'))
    win.mainloop()


if __name__ == '__main__':
    main()
