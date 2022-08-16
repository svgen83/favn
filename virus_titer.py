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
      infection_percent = round((k * 100 / (k + m)))
      infection_percent_list.append(infection_percent)
      dilution = initial_reciproc_dilution * dilution_ratio**index
      dilution_list.append(dilution)
      index += 1
    print(dilution_list)
    print(infection_percent_list)
    return dict(zip(dilution_list, infection_percent_list))


def count_serum_titer(dilution_infection_dict, dilution_ratio):
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
    print(min_value)
    print(max_value)
    print(logs_diff)
    minimum_log = round(math.log10(min_value),4)
    print(minimum_log)
    lg_titer = round((minimum_log + logs_diff),5)
    titer = int(10**lg_titer)
    return titer,lg_titer


def count_virus_titer(dilution_infection_dict, dilution_ratio):
    for key, value in dilution_infection_dict.items():
        if value < 50:
            less_50 = value
            min_value = key
            break
    for key, value in dilution_infection_dict.items():
        if value >= 50:
            more_50 = value
            max_value = key
            
    k = (more_50 - 50)/(more_50 - less_50)
    logs_diff = math.log10(dilution_ratio) * k
    print(min_value)
    print(max_value)
    print(logs_diff)
    max_log = round(math.log10(max_value),4)
    print(max_log)
    lg_titer = round((max_log + logs_diff),5)
    titer = int(10**lg_titer)
    return titer,lg_titer


def serum_titer_calculate(init_dilution,dilution_ratio,rows_data):
    pprint(rows_data)

    rev_rows = get_reverse_rows(rows_data)
    pprint(rev_rows)

    infected_cum = get_cumulative_for_dilutions (rows_data, '+')
    uninfected_cum = (get_cumulative_for_dilutions (rev_rows,'-'))
    uninfected_cum = uninfected_cum[::-1]

    print(infected_cum)
    print(uninfected_cum)
    dictionary = get_dilution_infection_dict(infected_cum, uninfected_cum,
                                             init_dilution, dilution_ratio)
    print(dictionary)
    ED_50 = count_serum_titer(dictionary, dilution_ratio)
    return ED_50


def virus_titer_calculate(init_dilution,dilution_ratio,rows_data):
    pprint(rows_data)

    rev_rows = get_reverse_rows(rows_data)
    pprint(rev_rows)

    infected_cum = get_cumulative_for_dilutions (rev_rows, '+')
    uninfected_cum = (get_cumulative_for_dilutions (rows_data,'-'))
    infected_cum = infected_cum[::-1]

    print(infected_cum)
    print(uninfected_cum)
    dictionary = get_dilution_infection_dict(infected_cum, uninfected_cum,
                                             init_dilution, dilution_ratio)

    
    ID_50 = count_virus_titer(dictionary, dilution_ratio)
    print(ID_50)
    return ID_50
