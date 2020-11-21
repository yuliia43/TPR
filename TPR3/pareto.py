import numpy as np
import pandas as pd


def check(alternatives, priorities, classes):
    alternatives_q = alternatives.shape[0]
    index = alternatives.index
    pareto_comparisons      = pd.DataFrame(index=index, columns=index)
    maj_comparisons         = pd.DataFrame(index=index, columns=index)
    leks_comparisons        = pd.DataFrame(index=index, columns=index)
    beresovskiy_comparisons = pd.DataFrame(data=np.zeros((index.shape[0], index.shape[0])),
                                           index=index, columns=index, dtype="int")
    podinovskiy_comparisons = pd.DataFrame(index=index, columns=index)
    for i in range(alternatives_q):
        alternative_a = alternatives.iloc[i]
        for j in range(alternatives_q):
            alternative_b = alternatives.iloc[j]
            sigma = alternative_a.astype(float) - alternative_b.astype(float)
            check_alternatives_with_pareto(alternative_a, alternative_b, sigma, pareto_comparisons)
            check_alternatives_with_maj(alternative_a, alternative_b, sigma, maj_comparisons)
            check_alternatives_with_leks(alternative_a, alternative_b, sigma, priorities, leks_comparisons)
            check_alternatives_with_beresovskiy(alternative_a, alternative_b, sigma, classes, beresovskiy_comparisons)
            check_alternatives_with_podinovskiy(alternative_a, alternative_b, podinovskiy_comparisons)

    return (pareto_comparisons[pareto_comparisons > 0].fillna(0), maj_comparisons, leks_comparisons,
           beresovskiy_comparisons, podinovskiy_comparisons[podinovskiy_comparisons > 0].fillna(0))


def check_alternatives_with_pareto(alternative_a, alternative_b, sigma, comparisons):
    max_val = np.max(sigma)
    min_val = np.min(sigma)
    if max_val >= 0 and min_val >= 0:   # positive
        comparisons[alternative_a.name][alternative_b.name] = 1
    elif max_val <= 0 and min_val < 0:  # negative
        comparisons[alternative_a.name][alternative_b.name] = -1
    else:                               # incomparable
        comparisons[alternative_a.name][alternative_b.name] = 0


def check_alternatives_with_maj(alternative_a, alternative_b, sigma, comparisons):
    sum = np.sum(sigma)
    if sum > 0:
        comparisons[alternative_a.name][alternative_b.name] = 1
    else:
        comparisons[alternative_a.name][alternative_b.name] = 0


def check_alternatives_with_leks(alternative_a, alternative_b, sigma, classes, comparisons):
    sorted_sigma = sigma.reindex(classes)
    for i in sorted_sigma:
        if i < 0:
            comparisons[alternative_a.name][alternative_b.name] = 0
            return
        elif i > 0:
            comparisons[alternative_a.name][alternative_b.name] = 1
            return
    comparisons[alternative_a.name][alternative_b.name] = 0


def check_alternatives_with_beresovskiy(alternative_a, alternative_b, sigma, classes, comparisons):
    alternative_a_name = alternative_a.name
    alternative_b_name = alternative_b.name
    cols = set([alternative_a_name, alternative_b_name])
    i_n_p_prev = pd.DataFrame(index=cols, columns=cols)
    i = 0
    for kriteria_class in classes:
        i_n_p = fill_i_n_p(alternative_a,  alternative_b, cols, sigma.reindex(kriteria_class))
        if i > 0:
            bool_var = (((i_n_p == "P") & (i_n_p_prev is not None)) | ((i_n_p == "I") & (i_n_p_prev == "P")))
            if bool_var[alternative_a_name][alternative_b_name]:
                comparisons[alternative_a_name][alternative_b_name] = 1
            if bool_var[alternative_b_name][alternative_a_name]:
                comparisons[alternative_b_name][alternative_a_name] = 1
        i_n_p_prev = i_n_p
        i+=1


def fill_i_n_p(alternative_a, alternative_b, cols, sigma):
    i_n_p = pd.DataFrame(index=cols, columns=cols)
    alternative_a_name = alternative_a.name
    alternative_b_name = alternative_b.name
    check_alternatives_with_pareto(alternative_a, alternative_b, sigma, i_n_p)
    if i_n_p[alternative_a_name][alternative_b_name] == 1:
        i_n_p[alternative_a_name][alternative_b_name] = "P"
    elif i_n_p[alternative_a_name][alternative_b_name] == -1:
        i_n_p[alternative_b_name][alternative_a_name] = "P"
    else:
        i_n_p[alternative_a_name][alternative_b_name] = "N"
        i_n_p[alternative_b_name][alternative_a_name] = "N"
    i_n_p[alternative_a_name][alternative_a_name] = "I"
    i_n_p[alternative_b_name][alternative_b_name] = "I"
    return i_n_p


def check_alternatives_with_podinovskiy(alternative_a, alternative_b, podinovskiy_comparisons):
    sorted_a = alternative_a.astype(float).sort_values(ascending=False)
    sorted_b = alternative_b.astype(float).sort_values(ascending=False)
    sigma = sorted_a - sorted_b
    check_alternatives_with_pareto(alternative_a, alternative_b, sigma, podinovskiy_comparisons)
