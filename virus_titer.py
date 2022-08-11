import math
from pprint import pprint


def get_reverse_rows (rows):
    rev_rows =[]
    for row in rows:
        rev_row = row[::-1]
        rev_rows.append(rev_row)
    return(rev_rows)

        
def get_cumulative_for_dilutions (rows,kind):
    cumulative_list = []
    i=0
    for wells in zip(*rows): # wells - это вертикальные ряды
        for well in wells:
            if well == kind:
                i += 1
        cumulative_list.append(i)
    return cumulative_list


def get_dilution_infection_dict(infected_cumulative, uninfected_cumulative,
                                initial_reciproc_dilution, dilution_ratio):
    index = 0
    infection_percent_list = []
    dilution_list = []
    for k,m in zip(infected_cumulative, uninfected_cumulative):
      infection_percent = int((k * 100 / (k + m)))
      infection_percent_list.append(infection_percent)
      dilution = initial_reciproc_dilution * dilution_ratio**index
      dilution_list.append(dilution)
      index += 1
    print(dilution_list)
    print(infection_percent_list)
    return dict(zip(dilution_list, infection_percent_list))


def count_titer(dilution_infection_dict, dilution_ratio):
    for key, value in dilution_infection_dict.items():
        if value < 50:
            less_50 = value
            min_value = key
    for key, value in dilution_infection_dict.items():
        if value >= 50:
            more_50 = value
            max_value = key
            break
    k = (50 - less_50)/(more_50 - less_50)
    logs_diff = math.log10(dilution_ratio) * k
    #print(min_value)
    minimum_log = round(math.log10(min_value),4)
    #print(minimum_log)
    lg_titer = round((minimum_log + logs_diff),5)
    titer = int(10**lg_titer)
    return titer,lg_titer

def titer_calculate(init_dilution,dilution_ratio,rows_data):
    pprint(rows_data)

    rev_rows = get_reverse_rows(rows_data)
    #pprint(rev_rows)

    infected_cum = get_cumulative_for_dilutions (rows_data, '+')
    uninfected_cum = (get_cumulative_for_dilutions (rev_rows,'-'))
    uninfected_cum = uninfected_cum[::-1]

    #print(infected_cum)
    #print(uninfected_cum)
    dictionary = get_dilution_infection_dict(infected_cum, uninfected_cum,init_dilution, dilution_ratio)
    #print(dictionary)
    ED_50 = count_titer(dictionary, dilution_ratio)
    return ED_50


##y = 1
##n = 0
##z = None
##initial_reciproc_dilution = 1000
##dilution_ratio = 2
##
##row1 = ['n', 'n', 'y', 'n', 'n']
##row2 = ['n', 'n', 'n', 'n', 'n']
##row3 = ['n', 'n', 'n', 'n', 'y']
##row4 = ['n', 'n', 'n', 'y', 'y']
##row5 = ['n', 'n', 'n', 'y', 'y']
##row6 = ['n', 'n', 'n', 'y', 'y']
##
##rows = [row1, row2, row3, row4, row5, row6]
##
##
##print(main(1000, 2, rows))
