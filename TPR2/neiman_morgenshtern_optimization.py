import numpy as np


def find_neiman_morgenshtern_solution(matrix):
    upper_intersections = _find_upper_intersections(matrix)
    s_sets = _find_s_sets(upper_intersections)
    solution = _find_solution(upper_intersections, s_sets)
    solution.sort()
    #print("Xnm = {", ", ".join('{}'.format(el) for el in solution), "}")
    return solution


def _find_upper_intersections(matrix):
    non_zero_rows, non_zero_columns = np.nonzero(matrix)
    upper_intersections = {idx + 1: non_zero_rows[non_zero_columns == idx] + 1
                           for idx in range(len(matrix))}
    return upper_intersections


def _find_s_sets(upper_intersections):
    intersections = []
    all_sets = []
    while len(intersections) != len(upper_intersections):
        sets = []
        for row in upper_intersections:
            if row not in intersections:
                in_intersections = True
                for x in upper_intersections[row]:
                    if x not in intersections:
                        in_intersections = False
                        break
                if in_intersections:
                    sets.append(row)
        intersections.extend(sets)
        all_sets.extend([sets])
    return all_sets


def _find_solution(upper_intersections, s_sets):
    q_set = []
    for s_set in s_sets:
        for element in s_set:
            in_q_set = True
            for x in upper_intersections[element]:
                if x in q_set:
                    in_q_set = False
                    break
            if in_q_set:
                q_set.append(element)
    return q_set

