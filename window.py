from tkinter import *
from tkinter.ttk import Combobox
##import tkinter as tk

from virus_titer import serum_titer_calculate, virus_titer_calculate


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Specific activity calculator")
##        self.geometry('600x400')

        self.entries = []
        self.labels = []
              
        self.add_btn = Button(self, text="Добавить ряд",
                             command=self.add_row)

        self.help_button = Button(self, 
              text="Помощь/О программе",
              command=self.create_help_window)

        self.reference_button = Button(self, 
              text="Определить активность в международных единицах",
              command=self.create_window)

        self.dilut_ratio_lbl = Label(text="Шаг разведения:")

        self.diluttion_ratio = Combobox(self)  
        self.diluttion_ratio['values'] = ( 2, 3, 4, 5, 10)  
        self.diluttion_ratio.current(1)  # вариант по умолчанию

        self.init_dilution_lbl = Label(self,text="Начальное разведение:")
        self.init_dilution = Entry(self)
        self.init_dilution.insert(0, "50")

        
        self.result_lbl = Label(self, text="")     
        self.serum_result_btn = Button(self, text="Определить титр антител", command=self.ed_calculate)
        self.virus_result_btn = Button(self, text="Определить титр вируса", command=self.id_calculate)
        self.remove_btn = Button(self, text="Удалить ряд", command=self.remove_row)

        self.result_lbl.pack()
        self.serum_result_btn.pack()
        self.virus_result_btn.pack()
        
        self.help_button.pack()
        self.reference_button.pack()
              
        self.add_btn.pack()
        self.remove_btn.pack()
        
        self.dilut_ratio_lbl.pack()
        self.diluttion_ratio.pack()
        
        self.init_dilution_lbl.pack()
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
        self.label_1 = Label(self, text=f'Введите значения для образца {n+1}')
        self.label_1.pack()
        self.labels.append(self.label_1)
        self.entry = Entry(self)
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
        res1 = serum_titer_calculate(init_dilution,dilution_ratio,rows_data)
        res2 = str(res1)
        res = f"Титр антител {res2}"
        self.result_lbl.configure(text=res)
        

    def id_calculate(self):
        init_dilution = int(self.init_dilution.get())
        dilution_ratio = int(self.diluttion_ratio.get())
        rows = []
        datas = self.entries
        for data in datas:
            row = list(data.get())
            rows.append(row)
        rows_data = rows
        res1 = virus_titer_calculate(init_dilution,dilution_ratio,rows_data)
        res2 = str(res1)
        res = f"Титр антител {res2}"
        self.result_lbl.configure(text=res) 


    def calculate_ui(self):
        titer_reference = int(self.titer_reference_entry.get())
        ui_reference = int(self.ui_reference_entry.get())
        titer_analit = int(self.analit_entry.get())
        ui_analit = titer_analit*ui_reference/titer_reference
        self.ui_analit_lbl.configure(text = ui_analit)
        

    def create_help_window(self):
        read_me = """Помощь.О программе
Программа предназначена для определения титра антител методом флуоресцирующих антител.

Разработана во ФКУН Российский научно-исследовательский институт "Микроб", 2022 г."""

        self. help_window = Toplevel(self)
        self.help_lbl = Label(self.help_window, text = read_me)
        self.help_lbl.pack()


    def create_window(self):
        self.window = Toplevel(self)
        self.titer_reference_lbl = Label(self.window,text="Титр антител стандартного образца:")
        self.ui_reference_lbl = Label(self.window,text="Активность стандартного образца в МЕ/мл:")
        self.analit_lbl = Label(self.window,text="Титр антител определяемого образца:")
        self.ui_analit_lbl = Label(self.window,text="")
        self.ui_analit_btn = Button(self.window, text="Титр антител в МЕ", command=self.calculate_ui)

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
