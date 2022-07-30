import os
import sys
import re
import math
import traceback
from pprint import pprint

# def Titer(infectedwells, volume, dilution):
#     """Рассчитывает титр по формуле Рида-Менчаа.
#     infectedwells -> Это список списков. Количество списков
#         дает количество повторов, поэтому имеется len(infectedwells)
#         копирует. Каждый из списков записей описывает лунки, в которых наблюдали инфекцию в рядах 96-луночного планшета. Так, например, [[А, Б, В, Г], [А, Б, В], [А, В, В, Г]]
#         соответствует трем повторностям, оказывающим цитопатическое действие
#         в первых четырех рядах (первая повторность), первые три ряда
#         (вторая повторность) и первые четыре ряда (третья повторность).
#         Должно быть не менее двух повторений.
#     volume -> Это объем вируса в первой строке (строка A).
#     разбавление -> Это коэффициент разбавления между последовательными строками.
#         Например, 10 является типичным коэффициентом разбавления для этого анализа.
#     Этот метод возвращает число, которое дает титр как TCID50.
#         на единицу объема в любых единицах, используемых для указания
#         входной переменный объем.
#     Формула Рида-Мюнха реализуется, как описано в
#         http://whqlibdoc.who.int/monograph/WHO_MONO_23_(3ed)_appendices.pdf
#         http://www.fao.org/docrep/005/ac802e/ac802e0w.htm
#     """
#     rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] # row labels in order
#     reverserows = [row for row in rows]
#     reverserows.reverse()
#     nreplicates = len(infectedwells)
#     if nreplicates < 2:
#         raise ValueError("This implementation of the Reed-Muench formula requires at least two replicates. Only %d are provided." % nreplicates)
#     counts = dict([(r, 0) for r in rows]) # количество инфицированных лунок в каждом разведении
#     for replicatewells in infectedwells:
#         for well in replicatewells:
#             if well not in rows:
#                 raise ValueError("One of the rows is specified as %s, which is not a valid row." % well)
#             counts[well] += 1
#     infected = {} # cumulative totals of infected wells going up plate
#     uninfected = {} # cumulative totals of uninfected wells going down plate
#     n = 0
#     for row in rows:
#         uninfected[row] = n + nreplicates - counts[row]
#         n = uninfected[row]
#     n = 0
#     for row in reverserows:
#         infected[row] = n + counts[row]
#         n = infected[row]
#     percentinfected = {} # cumulative percent infected
#     for row in rows:
#         percentinfected[row] = 100.0 * infected[row] / (infected[row] + uninfected[row])
#     for irow in range(len(rows)):
#         if percentinfected[rows[irow]] < 50:
#             if irow == 0:
#                 raise ValueError("Even the first dilution has < 50% infected.")
#             else:
#                 rowabove50 = rows[irow - 1]
#                 break
#     else:
#         raise ValueError("No dilutions have < 50% infected.")
#     percentrowabove50 = percentinfected[rowabove50]
#     if rowabove50 != rows[-1]:
#         percentrowbelow50 = percentinfected[rows[rows.index(rowabove50) + 1]]
#     else:
#         percentrowbelow50 = 0
#     index = (percentrowabove50 - 50.0) / (percentrowabove50 - percentrowbelow50)
#     startdilution = rows.index(rowabove50)
#     titer = dilution**(startdilution + index) / volume
#     return titer

y = 1
n = 0
z = None
initial_reciproc_dilution = 50
dilution_ratio = 3

row1 = ['n', 'n', 'n', 'n', 'n', 'y']
row2 = ['n', 'n', 'n', 'n', 'y', 'y']
row3 = ['n', 'n', 'n', 'n', 'n', 'y']
row4 = ['n', 'n', 'n', 'n', 'y', 'y']

rows = [row1, row2, row3, row4]

def titer_count(rows, initial_reciproc_dilution, dilution_ratio):
    infected_wells = 0
    uninfected_wells = 0
    total_wells = 0
    less_50 = 0
    more_50 = 0
    index = 0
    infected_wells_in_dilution = []
    infected_perсent_list = []
    dilution_list = []
    infected_list = []
    uninfected_list = []
    infection_percent_list = []
    pprint(rows)
    for wells in zip(*rows):
      for well in wells:
        if well == 'y':
          infected_wells += 1
      infected_list.append(infected_wells)
    print(infected_list)
    print("razdel")
    for rwells in zip(*rows):
      for rwell in rwells:
        if rwell == 'n':
          uninfected_wells += 1
      uninfected_list.append(uninfected_wells)
    uninfected_list.reverse()
    print(uninfected_list)
    for k,m in zip(infected_list, uninfected_list):
      infection_percent = k * 100 / (k + m)
      infection_percent_list.append(infection_percent)
      dilution = initial_reciproc_dilution * dilution_ratio**index
      dilution_list.append(dilution)
      index += 1
    print(infection_percent_list)
    result_dict = dict(zip(dilution_list, infection_percent_list))
    print(result_dict)
    for key, value in result_dict.items():
        if value < 50:
            less_50 = value
            min_value = key
    for key, value in result_dict.items():
        if value >= 50:
            more_50 = value
            max_value = key
            break
    logs_diff = math.log10(dilution_ratio) * (50 - less_50) / (more_50 -
                                                               less_50)
    return int(10**(math.log10(min_value) + logs_diff))


id_50 = titer_count(rows, initial_reciproc_dilution, dilution_ratio)

print(id_50)

