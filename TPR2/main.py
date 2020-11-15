from TPR2.read_binary_relations import *
from TPR2.binary_relation import *
from TPR2.neiman_morgenshtern_optimization import *
from TPR2.k_optimization import *


if __name__ == '__main__':
    binary_relations = read_from_file("Варіант №21.txt")
    for binary_relation in binary_relations:
        acyclic = binary_relation.is_acyclic()
        if not acyclic:
            print(binary_relation.name, "is not acyclic. Searching with k-optimization algorithm...")
            find_all_k_opt_solutions(binary_relation.matrix)
        else:
            print(binary_relation.name, "is acyclic. Searching with Neiman-Morgenshtern algorithm...")
            find_neiman_morgenshtern_solution(binary_relation.matrix)
        binary_relation.print_graph()
