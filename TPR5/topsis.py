import TPR.TPR4.read_from_file as read
import numpy as np
import pandas as pd


def normalize_weights(weights):
    return weights/np.sum(weights)


def normalize_alternatives(alternatives):
    sums = np.sum(alternatives**2, axis=0)
    sqrt = np.sqrt(sums)
    r = alternatives/sqrt
    return r


def weight_normalized_alternatives(normalized_alternatives, normalized_weights):
    return normalized_weights*normalized_alternatives


def find_PIS_and_NIS_maximization(w_n_alternatives):
    PIS = np.max(w_n_alternatives, axis=0)
    NIS = np.min(w_n_alternatives, axis=0)
    return PIS, NIS

def find_PIS_and_NIS_max_min(w_n_alternatives):
    maxim = np.max(w_n_alternatives, axis=0)
    minim = np.min(w_n_alternatives, axis=0)
    PIS = maxim[:7].append(minim[7:])
    NIS = minim[:7].append(maxim[7:])
    return PIS, NIS


def find_distances_to_PIS_and_NIS(w_n_alternatives, PIS, NIS):
    distance_to_PIS = np.sqrt(np.sum(
                        (w_n_alternatives-PIS)**2,
                        axis=1))
    distance_to_NIS = np.sqrt(np.sum(
        (w_n_alternatives - NIS) ** 2,
        axis=1))
    return distance_to_PIS, distance_to_NIS


def find_the_range(distance_to_PIS, distance_to_NIS):
    Ck = distance_to_NIS/(distance_to_PIS + distance_to_NIS)
    sorted = pd.Series.sort_values(Ck, ascending=False)
    return sorted


def find_topsis_optimization(alternatives, weights, mode=0):
    normalized_alternatives = normalize_alternatives(alternatives)
    normalized_weights = normalize_weights(weights)
    w_n_alternatives = weight_normalized_alternatives(normalized_alternatives, normalized_weights)
    if mode == 0:
        PIS, NIS = find_PIS_and_NIS_maximization(w_n_alternatives)
    else:
        PIS, NIS = find_PIS_and_NIS_max_min(w_n_alternatives)
    d_PIS, d_NIS = find_distances_to_PIS_and_NIS(w_n_alternatives, PIS, NIS)
    return find_the_range(d_PIS, d_NIS)

if __name__ == '__main__':
    alternatives, weights, _, _ = read.read_from_file("Варіант №21 умова.txt")
    # alternatives = pd.DataFrame(data={'K1': [5,7,8,7], 'K2': [8,6,8,4], 'K3': [4,8,6,6]},
    #                             index=['A1', 'A2', 'A3', 'A4'])
    # weights = [0.3, 0.4, 0.3]
    print("Всі критерії максимізуються. Результат:")
    print(find_topsis_optimization(alternatives, weights))
    print("Критерії k1-k7 підлягають максимізації, а критерії k8-k12 – мінімізації. Результат:")
    print(find_topsis_optimization(alternatives, weights, mode=1))

