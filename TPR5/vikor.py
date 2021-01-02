import TPR.TPR4.read_from_file as read
from TPR.TPR5.topsis import normalize_weights
import numpy as np
import pandas as pd


def find_max_and_min(alternatives):
    max_k = np.max(alternatives, axis=0)
    min_k = np.min(alternatives, axis=0)
    return max_k, min_k


def count_weighted_intervals(alternatives, weights, min_k, max_k):
    intervals = np.abs(max_k - alternatives) / np.abs(max_k - min_k)
    weighted_intervals = weights*intervals
    return weighted_intervals


def find_S_and_R(weighted_intervals):
    S = np.sum(weighted_intervals, axis=1)
    R = np.max(weighted_intervals, axis=1)
    return S, R


def count_Q(S, R, niu = 0.5):
    min_S = np.min(S)
    max_S = np.max(S)
    min_R = np.min(R)
    max_R = np.max(R)
    Q = niu*(S-min_S)/(max_S-min_S)+(1-niu)*(R-min_R)/(max_R-min_R)
    return Q


def find_best_alternatives(Q, S, R):
    best_Q = np.min(Q)
    DQ = 1 / (len(Q) - 1)
    deltas = pd.Series.sort_values(Q - best_Q)
    best_alternatives = deltas[deltas < DQ].index
    if len(best_alternatives) == 1:
        best_Q_idx = best_alternatives[0]
        best_S = np.min(S)
        best_R = np.min(R)
        if best_S != S[best_Q_idx] and best_R != R[best_Q_idx]:
            best_alternatives.append(deltas[1])
    return list(best_alternatives)


if __name__ == '__main__':
    alternatives, weights, _, _ = read.read_from_file("Варіант №21 умова.txt")
    # alternatives = pd.DataFrame(data={'K1': [5, 7, 8, 7], 'K2': [8, 6, 8, 4], 'K3': [4, 8, 6, 6]},
    #                             index=['A1', 'A2', 'A3', 'A4'])
    # weights = [0.3, 0.4, 0.3]
    max_k, min_k = find_max_and_min(alternatives)
    weighted_intervals = count_weighted_intervals(alternatives, weights, min_k, max_k)
    S, R = find_S_and_R(weighted_intervals)
    Q = count_Q(S, R)
    best_alternatives = find_best_alternatives(Q, S, R)
    print("Множина найкращих альтернатив наступна:", best_alternatives)

