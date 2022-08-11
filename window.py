from tkinter import *
from tkinter.ttk import Combobox
##import tkinter as tk

from virus_titer import titer_calculate


class App(Tk):
    def __init__(self):
        super().__init__()

        self.entries = []
        self.labels = []
              
        self.add_btn = Button(self, text="Добавить ряд",
                             command=self.add_row)

        self.name_3 = Label(text="Шаг разведения:")

        self.diluttion_ratio = Combobox(self)  
        self.diluttion_ratio['values'] = ( 2, 3, 4, 5, 10)  
        self.diluttion_ratio.current(1)  # вариант по умолчанию

        self.name_4 = Label(self,text="Начальное разведение:")
        self.init_dilution = Entry(self)
        self.init_dilution.insert(0, "50")


        self.lbl = Label(self, text="")     
        self.result_btn = Button(self, text="Результат", command=self.calculate)

        self.remove_btn = Button(self, text="Удалить ряд", command=self.remove_row)

        self.lbl.pack()
        self.result_btn.pack()
        self.add_btn.pack()
        self.remove_btn.pack()
        self.name_3.pack()
        self.diluttion_ratio.pack()
        self.name_4.pack()
        self.init_dilution.pack()
        self.add_row()
        
        
    def print_data(self):
        rows = []
        datas = self.entries
        for data in datas:
            row = list(data.get())
            rows.append(row)
        print(rows)
        print("Шаг разведения: {}".format(self.diluttion_ratio.get()))
        print("Начальное разведение: {}".format(self.init_dilution.get()))
        res=self.diluttion_ratio.get(),self.init_dilution.get(),rows
        self.lbl.configure(text=res)
            

    def add_row(self):
        n = len(self.entries)
        self.label_1 = Label(self, text=f'Введите значения измерения {n+1}')
        self.label_1.pack()
        self.labels.append(self.label_1)
        self.entry = Entry(self)
        self.entry.pack()
        self.entries.append(self.entry)


    def remove_row(self):
        if len(self.entries) > 1:  
            self.entries.pop().destroy()
            self.labels.pop().destroy()
        

    def calculate(self):
        init_dilution = int(self.init_dilution.get())
        dilution_ratio = int(self.diluttion_ratio.get())
        rows = []
        datas = self.entries
        for data in datas:
            row = list(data.get())
            rows.append(row)
        rows_data = rows
        res1 = titer_calculate(init_dilution,dilution_ratio,rows_data)
        res2 = str(res1)
        res = f"Титр антител {res2}"
        self.lbl.configure(text=res)

if __name__ == "__main__":
    app = App()
    app.mainloop() 
