import math


def get_reverse_rows(rows):
    return [row[::-1] for row in rows]


def get_cumulative_for_dilutions(rows, kind):
    cumulative_list = []
    for wells in zip(*rows):  # столбцы
        count = sum(1 for well in wells if well == kind)
        cumulative_list.append(count)
    return cumulative_list


def get_dilution_infection_dict(infected_cumulative, uninfected_cumulative,
                                initial_reciproc_dilution, dilution_ratio):
    dilution_list = []
    infection_percent_list = []
    for i, (k, m) in enumerate(zip(infected_cumulative, uninfected_cumulative)):
        total = k + m
        infection_percent = round((k * 100 / total)) if total > 0 else 0
        dilution = initial_reciproc_dilution * (dilution_ratio ** i)
        dilution_list.append(dilution)
        infection_percent_list.append(infection_percent)
    return dict(zip(dilution_list, infection_percent_list))


def count_serum_titer(dilution_infection_dict, dilution_ratio):
    items = list(dilution_infection_dict.items())
    less_50 = None
    more_50 = None
    min_value = None
    max_value = None

    for key, value in items:
        if value < 50:
            less_50 = value
            min_value = key
        else:
            more_50 = value
            max_value = key
            break

    if less_50 is None or more_50 is None:
        return "Невозможно рассчитать ED₅₀: недостаточно данных"

    k = (50 - less_50) / (more_50 - less_50)
    logs_diff = math.log10(dilution_ratio) * k
    minimum_log = round(math.log10(min_value), 4)
    lg_titer = round((minimum_log + logs_diff), 5)
    titer = int(10 ** lg_titer)
    return f"1 : {titer}, lg ED₅₀ {lg_titer}"


def count_virus_titer(dilution_infection_dict, dilution_ratio):
    items = list(dilution_infection_dict.items())
    less_50 = None
    more_50 = None
    min_value = None
    max_value = None

    for key, value in items:
        if value >= 50:
            more_50 = value
            max_value = key
        elif less_50 is None:
            less_50 = value
            min_value = key

    if less_50 is None or more_50 is None:
        return "Невозможно рассчитать ID₅₀: недостаточно данных"

    k = (more_50 - 50) / (more_50 - less_50)
    logs_diff = math.log10(dilution_ratio) * k
    max_log = round(math.log10(max_value), 4)
    lg_titer = round((max_log - logs_diff), 5)
    titer = int(10 ** lg_titer)
    return f"1 : {titer}, lg ID₅₀ {lg_titer}"


def serum_titer_calculate(init_dilution, dilution_ratio, rows_data):
    rev_rows = get_reverse_rows(rows_data)
    infected_cum = get_cumulative_for_dilutions(rows_data, '+')
    uninfected_cum = get_cumulative_for_dilutions(rev_rows, '-')
    uninfected_cum = uninfected_cum[::-1]
    dictionary = get_dilution_infection_dict(infected_cum, uninfected_cum, init_dilution, dilution_ratio)
    return count_serum_titer(dictionary, dilution_ratio)


def virus_titer_calculate(init_dilution, dilution_ratio, rows_data):
    rev_rows = get_reverse_rows(rows_data)
    infected_cum = get_cumulative_for_dilutions(rev_rows, '+')
    uninfected_cum = get_cumulative_for_dilutions(rows_data, '-')
    infected_cum = infected_cum[::-1]
    dictionary = get_dilution_infection_dict(infected_cum, uninfected_cum, init_dilution, dilution_ratio)
    return count_virus_titer(dictionary, dilution_ratio)