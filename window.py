import textwrap as tw


from tkinter import *
from tkinter.ttk import Combobox


from virus_titer import serum_titer_calculate, virus_titer_calculate
from virus_titer import keep_records


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title(
            "Калькулятор для расчета реакции нейтрализации по методу Рида и Менча")

        self.entries = []
        self.labels = []

        self.add_btn = Button(self, text="Добавить ряд",
                              command=self.add_row)

        self.help_button = Button(
            self, text="Помощь/О программе",
            command=self.create_help_window)

        self.reference_button = Button(
            self, text="Определить активность в международных единицах",
            command=self.create_window)

        self.dilut_ratio_lbl = Label(text="Кратность разведения:")

        self.diluttion_ratio = Combobox(self, font='Times 14')
        self.diluttion_ratio['values'] = (2, 3, 4, 5, 10)
        self.diluttion_ratio.current(1)  # вариант по умолчанию

        self.init_dilution_lbl = Label(self,
                                       text="Начальное разведение:")
        self.init_dilution = Entry(self, font='Times 14')
        self.init_dilution.insert(0, "50")

        self.result_lbl = Label(self, text="", font='Times 14')
        self.serum_result_btn = Button(
            self,
            text="Определить титр антител",
            command=self.ed_calculate)

        self.virus_result_btn = Button(
            self,
            text="Определить титр вируса",
            command=self.id_calculate)
        self.remove_btn = Button(
            self,
            text="Удалить ряд",
            command=self.remove_row)

        self.result_lbl.pack()
        self.serum_result_btn.pack(side=LEFT, fill=BOTH)
        self.virus_result_btn.pack(side=LEFT, fill=BOTH)

        self.help_button.pack(side=RIGHT, fill=BOTH)
        self.reference_button.pack(side=RIGHT, fill=BOTH)

        self.add_btn.pack()
        self.remove_btn.pack()

        self.dilut_ratio_lbl.pack()
        self.diluttion_ratio.pack()

        self.init_dilution_lbl.pack()
        self.init_dilution.pack()

        self.add_row()


    def add_row(self):
        n = len(self.entries)
        self.label_1 = Label(
            self,
            text=f'Введите значения для образца {n+1}')

        self.label_1.pack()
        self.labels.append(self.label_1)
        self.entry = Entry(self, font='Times 14')
        self.entry.pack()
        self.entries.append(self.entry)


    def remove_row(self):
        if len(self.entries) > 1:
            self.entries.pop().destroy()
            self.labels.pop().destroy()
       

    def ed_calculate(self):
        init_dilution = int(self.init_dilution.get())
        dilution_ratio = int(self.diluttion_ratio.get())
        rows = []
        datas = self.entries
        for data in datas:
            row = list(data.get())
            rows.append(row)
        rows_data = rows
        result = serum_titer_calculate(init_dilution,
                                       dilution_ratio,
                                       rows_data)
        keep_records(result, "./ED50.txt")
        self.result_lbl.configure(text=f"Титр антител {result}")


    def id_calculate(self):
        init_dilution = int(self.init_dilution.get())
        dilution_ratio = int(self.diluttion_ratio.get())
        rows = []
        datas = self.entries
        for data in datas:
            row = list(data.get())
            rows.append(row)
        rows_data = rows
        result = virus_titer_calculate(init_dilution,
                                       dilution_ratio,
                                       rows_data)
        keep_records(result, "./ID50.txt")
        self.result_lbl.configure(text=f"Титр вируса {result}")


    def calculate_ui(self):
        titer_reference = int(self.titer_reference_entry.get())
        ui_reference = int(self.ui_reference_entry.get())
        titer_analit = int(self.analit_entry.get())
        ui_analit = titer_analit*ui_reference/titer_reference
        keep_records(ui_analit, "./activity in UI.txt")
        self.ui_analit_lbl.configure(text=ui_analit)


    def create_help_window(self):
        read_me = tw.dedent("""
О программе

Программа предназначена для расчета специфической активности сывороток и иммуноглобулина,
а также активности вируса на основе результатов, полученных методом флуоресцирующих антител,
или другим аналогичным методом.

Расчет осуществляется по методу Рида и Менча.

Для расчета данных необходимо ввести обратное значение
исходного разведения образца (например, если начальное разведение 1:50,
то вводим значение 50), во вкладке "Кратность разведения"
выбираем соответствующее значение (по умолчанию задано 3).

Графу "Введите значения для образца" заполняем исходными данными в виде символов + и -.
При этом символ + соответствует лунке, в которой наблюдается флуоресценция,
символ - обозначает, что явление флуоресценции в лунке отсутствует.
Ряд символов + и - вводится для каждого раститрованного образца по отдельности.
При этом первый символ соответствует исходному (минимальному) разведению,
а последний - максимальному.
Общее количество символов + и - должно быть одинаковым для каждого ряда.

Для добавления результатов исследования используется кнопка "Добавить ряд".
Кнопка "Удалить ряд" используется для удаления ряда данных.

Для расчета титра антител используется кнопка "Определить титр антител",
и, соответственно для определения инфицирующей дозы вируса - кнопка "Определить титр вируса".

Для определения специфической активности в Международных единицах, используется соответствующая кнопка, при нажатии которой появляется новое окно
для ввода необходимых данных и получения результата.


Разработана во ФКУН Российский противочумный институт "Микроб", 2022 г.
Авторы: Генералов С.В., Гаврилова Ю.К., Абрамова Е.Г.""")

        self. help_window = Toplevel(self)
        self.help_lbl = Label(
            self.help_window,
            text = read_me, font='Times 14')
        self.help_lbl.pack()


    def create_window(self):
        self.window = Toplevel(self)
        self.titer_reference_lbl = Label(
            self.window,
            text="Титр антител стандартного образца:")
        self.ui_reference_lbl = Label(
            self.window,
            text="Активность стандартного образца в МЕ/мл:")
        self.analit_lbl = Label(
            self.window,
            text="Титр антител определяемого образца:")
        self.ui_analit_lbl = Label(self.window, text="")
        self.ui_analit_btn = Button(self.window,
                                    text="Титр антител в МЕ",
                                    command=self.calculate_ui)

        self.titer_reference_entry = Entry(self.window)
        self.titer_reference_entry.insert(0, "")
        self.ui_reference_entry = Entry(self.window)
        self.ui_reference_entry.insert(0, "")
        self.analit_entry = Entry(self.window)
        self.analit_entry.insert(0, "")

        self.titer_reference_lbl.pack()
        self.titer_reference_entry.pack()
        self.ui_reference_lbl.pack()
        self.ui_reference_entry.pack()
        self.analit_lbl.pack()
        self.analit_entry.pack()

        self.ui_analit_lbl.pack()
        self.ui_analit_btn.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
