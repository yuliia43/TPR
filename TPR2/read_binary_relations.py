import numpy as np
from TPR2.binary_relation import BinaryRelation


def read_from_file(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()

    bin_relations = []
    bin_rel_matr = []
    bin_rel_name = ""
    for line in lines:
        if any(ch.isalpha() for ch in line):
            if len(bin_rel_matr) != 0:
                matrix = np.array(bin_rel_matr, dtype="int32")
                b_r = BinaryRelation(bin_rel_name, matrix)
                bin_relations.append(b_r)
            bin_rel_matr = []
            bin_rel_name = line.split()[0].strip()
        else:
            bin_rel_matr.append(line.split())
    if len(bin_rel_matr) != 0:
        matrix = np.array(bin_rel_matr, dtype="int32")
        b_r = BinaryRelation(bin_rel_name, matrix)
        bin_relations.append(b_r)
    return bin_relations

