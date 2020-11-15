import numpy as np


def get_i_n_p_matrix(binary_relation_matrix):
    matrix = ["" for row in binary_relation_matrix for cell in row]
    matrix = np.reshape(matrix, binary_relation_matrix.shape)
    for i in range(len(binary_relation_matrix)):
        for j in range(i, len(binary_relation_matrix[0])):
            if binary_relation_matrix[i, j] == 0 and binary_relation_matrix[j, i] == 0:
                matrix[i][j] += "N"
                matrix[j][i] += "N"
            elif binary_relation_matrix[i, j] == binary_relation_matrix[j, i]:
                matrix[i][j] += "I"
                matrix[j][i] += "I"
            elif binary_relation_matrix[i, j] == 1:
                matrix[i][j] += "P"
            else:
                matrix[j][i] += "P"
    return matrix


def _search_for_maximality(i_n_p_matrix, s_matrix):
    all_rows = (np.sum(s_matrix, axis=0) > 0)
    counter = np.count_nonzero(all_rows)
    if counter == i_n_p_matrix.shape[0]:
        return []
    else:
        equality_vector = (s_matrix == all_rows)
        equality_vector = (np.count_nonzero(equality_vector, axis=1) == i_n_p_matrix.shape[0])
        return np.nonzero(equality_vector)[0]+1


def _find_k_solutions(i_n_p_matrix, s_matrix):
    counts = np.count_nonzero(s_matrix, axis=1)
    if np.max(counts) == i_n_p_matrix.shape[1]:
        _search_for_maximality(i_n_p_matrix, s_matrix)
        max_counts = (counts == np.max(counts))
        return True, np.nonzero(max_counts)[0]+1
    else:
        return False, _search_for_maximality(i_n_p_matrix, s_matrix)


def find_k1_solutions(i_n_p_matrix):
    s_matrix = ((i_n_p_matrix == "I") | (i_n_p_matrix == "N") | (i_n_p_matrix == "P"))
    return _find_k_solutions(i_n_p_matrix, s_matrix)


def find_k2_solutions(i_n_p_matrix):
    s_matrix = ((i_n_p_matrix == "N") | (i_n_p_matrix == "P"))
    return _find_k_solutions(i_n_p_matrix, s_matrix)


def find_k3_solutions(i_n_p_matrix):
    s_matrix = ((i_n_p_matrix == "I") | (i_n_p_matrix == "P"))
    return _find_k_solutions(i_n_p_matrix, s_matrix)


def find_k4_solutions(i_n_p_matrix):
    s_matrix = (i_n_p_matrix == "P")
    return _find_k_solutions(i_n_p_matrix, s_matrix)


def find_all_k_opt_solutions(matrix):
    i_n_p_matrix = get_i_n_p_matrix(matrix)
    k1_opt, k1_solutions = find_k1_solutions(i_n_p_matrix)
    k2_opt, k2_solutions = find_k2_solutions(i_n_p_matrix)
    k3_opt, k3_solutions = find_k3_solutions(i_n_p_matrix)
    k4_opt, k4_solutions = find_k4_solutions(i_n_p_matrix)

    if len(k1_solutions) == 0:
        print("1-max: \u00F8")
    else:
        print("1-max: {", ", ".join('{}'.format(el) for el in k1_solutions), "}")
    if k1_opt:
        print("1-opt: {", ", ".join('{}'.format(el) for el in k1_solutions), "}")

    if len(k2_solutions) == 0:
        print("2-max: \u00F8")
    else:
        print("2-max: {", ", ".join('{}'.format(el) for el in k2_solutions), "}")
    if k2_opt:
        print("2-opt: {", ", ".join('{}'.format(el) for el in k2_solutions), "}")

    if len(k3_solutions) == 0:
        print("3-max: \u00F8")
    else:
        print("3-max: {", ", ".join('{}'.format(el) for el in k3_solutions), "}")
    if k3_opt:
        print("3-opt: {", ", ".join('{}'.format(el) for el in k3_solutions), "}")

    if len(k4_solutions) == 0:
        print("4-max: \u00F8")
    else:
        print("4-max: {", ", ".join('{}'.format(el) for el in k4_solutions), "}")
    if k1_opt:
        print("4-opt: {", ", ".join('{}'.format(el) for el in k4_solutions), "}")
    return k1_opt, k1_solutions, k2_opt, k2_solutions, k3_opt, k3_solutions, k4_opt, k4_solutions
