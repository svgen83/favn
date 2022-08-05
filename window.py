from tkinter import *
from tkinter.ttk import Combobox

from virus_titer import main

def calculate():
    res1 = main(dilution, 1000, entries)
    res2 = str(res1)
    res = f"Титр антител {res2}"
    lbl.configure(text=res)

def add_row():
    n = len(entries)
    label = Label(window, text=f'Введите значения измерения {n+1}')
    label.grid(row=n+1, column=0)
    labels.append(label)
    entry = Entry(window)
    entry.grid(row=n+1, column=1)
    entries.append(entry)


def remove_row():
    if len(entries) > 1:  
        entries.pop().destroy()
        labels.pop().destroy()


            
window = Tk()
window.title("Specific activity calculator")
window.geometry('400x400')

labels = []
entries = []

Button(window, text="Добавить измерение", command=add_row).grid(row=0, column=0)
Button(window, text="Удалить измерение", command=remove_row).grid(row=0, column=1)
Button(window, text="Вычисления", command=calculate).grid(row=0, column=3)
Button(window, text="Начальное разведение").grid(row=0, column=2)
lbl = Label(window, text="")  
lbl.grid(column=0, row=15)

add_row()

combo = Combobox(window)  
combo['values'] = ( 2, 3, 4, 5, 10)  
combo.current(0)  # установите вариант по умолчанию  
combo.grid(column=1, row=14)
dilution = combo.get()

dilut_lbl = Label(window, text=f"Исходное развдение{dilution}")  
lbl.grid(column=0, row=25)




#frame = Frame(window, width=200, height=100)

#for i in range(1,12):
    #for n in range(1, 9):
        #cb = Checkbutton(window)
        #cb.grid(column=i, row=n)


#for i in range(1, 9):
    #lbl = Label(window, text=f"Ряд{i}")
    #lbl.grid(column=0, row=i)



#for n in range(list):
    #Label(window, text='Введите значения каждого измерения').grid(row=20, column=20)
    #Entry(window).grid(row=20, column=n+1)

#txt = Text(window,width=10)
#txt.grid(column=1, row=12)





#lbl = Label(window, text="")
#lbl.grid(column=5, row=15)
#btn = Button(window, text="Результат", command=clicked)  
#btn.grid(column=3, row=16)

#app = Example()
window.mainloop()
