import tkinter as tk
from tkinter import ttk
from .core import serum_titer_calculate, virus_titer_calculate
from .logger import keep_records
import textwrap as tw


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Калькулятор для расчета реакции нейтрализации по методу Рида и Менча")

        self.entries = []
        self.labels = []

        self.add_btn = ttk.Button(self, text="Добавить ряд", command=self.add_row)
        self.remove_btn = ttk.Button(self, text="Удалить ряд", command=self.remove_row)

        self.help_button = ttk.Button(self, text="Помощь/О программе", command=self.create_help_window)
        self.reference_button = ttk.Button(self, text="Определить активность в международных единицах",
                                           command=self.create_window)

        self.dilut_ratio_lbl = ttk.Label(self, text="Кратность разведения:")
        self.diluttion_ratio = ttk.Combobox(self, font='Times 14')
        self.diluttion_ratio['values'] = (2, 3, 4, 5, 10)
        self.diluttion_ratio.current(1)

        self.init_dilution_lbl = ttk.Label(self, text="Начальное разведение:")
        self.init_dilution = ttk.Entry(self, font='Times 14')
        self.init_dilution.insert(0, "50")

        self.result_lbl = ttk.Label(self, text="", font='Times 14')

        self.serum_result_btn = ttk.Button(self, text="Определить титр антител", command=self.ed_calculate)
        self.virus_result_btn = ttk.Button(self, text="Определить титр вируса", command=self.id_calculate)

        # Packing
        self.result_lbl.pack()
        self.serum_result_btn.pack(side=tk.LEFT, fill=tk.BOTH)
        self.virus_result_btn.pack(side=tk.LEFT, fill=tk.BOTH)

        self.help_button.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.reference_button.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.add_btn.pack()
        self.remove_btn.pack()

        self.dilut_ratio_lbl.pack()
        self.diluttion_ratio.pack()

        self.init_dilution_lbl.pack()
        self.init_dilution.pack()

        self.add_row()

    def add_row(self):
        n = len(self.entries)
        label = ttk.Label(self, text=f'Введите значения для образца {n + 1}')
        label.pack()
        entry = ttk.Entry(self, font='Times 14')
        entry.pack()
        self.entries.append(entry)
        self.labels.append(label)

    def remove_row(self):
        if len(self.entries) > 1:
            self.entries.pop().destroy()
            self.labels.pop().destroy()

    def ed_calculate(self):
        try:
            init_dilution = int(self.init_dilution.get())
            dilution_ratio = int(self.diluttion_ratio.get())
            rows_data = [list(e.get().strip()) for e in self.entries]

            for row in rows_data:
                if not all(c in '+-' for c in row):
                    raise ValueError("Все значения должны быть '+' или '-'.")

            result = serum_titer_calculate(init_dilution, dilution_ratio, rows_data)
            keep_records(result, "./ED50.txt")
            self.result_lbl.config(text=f"Титр антител {result}")
        except Exception as e:
            self.result_lbl.config(text=f"Ошибка: {e}")

    def id_calculate(self):
        try:
            init_dilution = int(self.init_dilution.get())
            dilution_ratio = int(self.diluttion_ratio.get())
            rows_data = [list(e.get().strip()) for e in self.entries]

            for row in rows_data:
                if not all(c in '+-' for c in row):
                    raise ValueError("Все значения должны быть '+' или '-'.")

            result = virus_titer_calculate(init_dilution, dilution_ratio, rows_data)
            keep_records(result, "./ID50.txt")
            self.result_lbl.config(text=f"Титр вируса {result}")
        except Exception as e:
            self.result_lbl.config(text=f"Ошибка: {e}")

    def create_help_window(self):
        help_text = tw.dedent("""
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
Авторы: Генералов С.В., Гаврилова Ю.К., Абрамова Е.Г.
        """)
        window = tk.Toplevel(self)
        tk.Label(window, text=help_text, justify=tk.LEFT).pack()

    def create_window(self):
        win = tk.Toplevel(self)
        tk.Label(win, text="Титр стандартного образца:").pack()
        tr = tk.Entry(win)
        tr.pack()

        tk.Label(win, text="Активность стандарта в МЕ/мл:").pack()
        ur = tk.Entry(win)
        ur.pack()

        tk.Label(win, text="Титр исследуемого образца:").pack()
        ta = tk.Entry(win)
        ta.pack()

        res_label = tk.Label(win, text="")
        res_label.pack()

        def calculate():
            try:
                t_ref = int(tr.get())
                u_ref = int(ur.get())
                t_analit = int(ta.get())
                if t_ref == 0:
                    raise ValueError("Титр не может быть равен 0.")
                ui = t_analit * u_ref / t_ref
                res_label.config(text=f"{ui:.2f} МЕ/мл")
                keep_records(f"{ui:.2f} МЕ/мл", "./activity_in_UI.txt")
            except Exception as e:
                res_label.config(text=f"Ошибка: {e}")

        tk.Button(win, text="Рассчитать", command=calculate).pack()
