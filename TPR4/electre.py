import pandas as pd
import numpy as np
from TPR4.read_from_file import *
import TPR2.neiman_morgenshtern_optimization as neiman
from TPR2.binary_relation import BinaryRelation
import matplotlib.pyplot as plt


def get_c_and_d_matrices(alternatives, weights):
    c_matrix = pd.DataFrame(index=alternatives.index, columns=alternatives.index)
    d_matrix = pd.DataFrame(index=alternatives.index, columns=alternatives.index)
    d_koefs = weights*(np.max(alternatives, axis=0)-np.min(alternatives, axis=0))
    alternatives = alternatives.transpose()
    i = 0
    for alternative1 in alternatives:
        for alternative2 in alternatives[i:]:
            if alternative1 == alternative2:
                c_matrix[alternative1][alternative2] = 0
                d_matrix[alternative1][alternative2] = 1
            else:
                diffs = alternatives[alternative1]-alternatives[alternative2]
                better = diffs[diffs > 0]
                worse = diffs[diffs < 0]
                equal = diffs[diffs == 0]
                c_matrix[alternative1][alternative2] = \
                    np.sum(weights[np.append(better.index, equal.index)])/np.sum(weights)
                c_matrix[alternative2][alternative1] = \
                    np.sum(weights[np.append(worse.index, equal.index)])/np.sum(weights)
                d_matrix[alternative1][alternative2] = \
                    np.max(-weights[worse.index]*worse)/np.max(d_koefs[worse.index])
                d_matrix[alternative2][alternative1] = \
                    np.max(weights[better.index]*better)/np.max(d_koefs[better.index])
        i+=1
    return c_matrix.astype(float).round(3), d_matrix.astype(float).round(3)


def relations(c_matrix, d_matrix, c, d):
    c_s = (c_matrix >= c)
    d_s = (d_matrix <= d)
    return np.where(c_s & d_s, 1, 0)


def d_analysis(c_matrix, d_matrix):
    c = 0.5
    ds = []
    core_sizes = []
    for d in range(0, 50, 5):
        rels = relations(c_matrix, d_matrix, c, d/100)
        bin_rel = BinaryRelation("Task4", rels)
        if bin_rel.is_acyclic():
            ds.append(d/100)
            sol = neiman.find_neiman_morgenshtern_solution(rels)
            core_sizes.append(len(sol))
    plt.xlabel('d values')
    plt.ylabel("core size")
    plt.xlim(0, 0.5)
    plt.ylim(0,16)
    plt.plot(ds, core_sizes)
    plt.show()



def c_analysis(c_matrix, d_matrix):
    d = 0.49
    cs = []
    core_sizes = []
    for c in range(50, 101, 5):
        rels = relations(c_matrix, d_matrix, c/100, d)
        bin_rel = BinaryRelation("Task4", rels)
        if bin_rel.is_acyclic():
            cs.append(c/100)
            sol = neiman.find_neiman_morgenshtern_solution(rels)
            core_sizes.append(len(sol))
    plt.xlabel('c values')
    plt.ylabel("core size")
    plt.xlim(0.5, 1)
    plt.plot(cs, core_sizes)
    plt.show()


def c_and_d_analysis(c_matrix, d_matrix):
    d = 0
    c = 1
    cs = []
    core_sizes = []
    for i in range(0, 50, 5):
        rels = relations(c_matrix, d_matrix, c, d)
        bin_rel = BinaryRelation("Task4", rels)
        if bin_rel.is_acyclic():
            cs.append("c"+str(round(c, 1))+" d"+str(round(d, 1)))
            sol = neiman.find_neiman_morgenshtern_solution(rels)
            core_sizes.append(len(sol))
        d += 0.05
        c -= 0.05
    plt.ylabel("core size")
    plt.plot(cs, core_sizes)
    plt.ylim(0,16)
    plt.show()

def write_in_file(c_matrix, d_matrix, c, d, solution, core):
    with open("output.txt", 'a', encoding="utf-8") as f:
        f.truncate(0)
        f.write("Матриця індексів узгодження\n")
        f.write(c_matrix.to_string(header=False, index=False))
        f.write("\nМатриця індексів неузгодження\n")
        f.write(d_matrix.to_string(header=False, index=False))
        f.write("\nЗначення с, d\n"+str(c)+" "+str(d)+"\n")
        f.write("Відношення  на  множині  альтернатив\n")
        solution = pd.DataFrame(solution)
        f.write(solution.to_string(header=False, index=False))
        f.write("\nЯдро для відношення\n")
        f.write(str(core))


if __name__ == '__main__':
    alternatives, weights, c, d = read_from_file("Варіант №21 умова.txt")
    c_matrix, d_matrix = get_c_and_d_matrices(alternatives, weights)
    rels = relations(c_matrix, d_matrix, c, d)
    bin_rel = BinaryRelation("Task4", rels)
    bin_rel.print_graph()
    if bin_rel.is_acyclic():
        sol = neiman.find_neiman_morgenshtern_solution(rels)
        print(sol)
        write_in_file(c_matrix, d_matrix, c, d, rels, sol)
    d_analysis(c_matrix, d_matrix)