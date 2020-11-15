import numpy as np
import graphviz
import os
from TPR2.neiman_morgenshtern_optimization import *
from TPR2.k_optimization import *
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz\bin'


class BinaryRelation:

    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.relations = {idx+1: np.nonzero(row)[0]+1 for idx, row in enumerate(matrix)}
        self.acyclic = None

    def is_acyclic(self):
        if self.acyclic is None:
            self.acyclic = True
            prev_nodes_stack = []
            for x in self.relations:
                (found_cycle, acyclic_nodes) = self.search_for_acyclic_nodes(x, prev_nodes_stack)
                if found_cycle:
                    self.acyclic = False
                    break
        return self.acyclic

    def search_for_acyclic_nodes(self, node, prev_nodes_stack):
        found_cycle = False
        node = int(node)
        acyclic_nodes = []
        if node in prev_nodes_stack:
            """
            print("There is a cycle in relation " + self.name + ": ")
            cycle = [node] + prev_nodes_stack
            cycle = cycle[-1::-1]
            print(cycle)
            """
            found_cycle = True
        else:
            if self.relations[node].shape == (0,):
                return False, [node]
            new_arr = [next_node for next_node in np.nditer(self.relations[node]) if next_node in prev_nodes_stack]
            if len(new_arr) != 0:
                """
                print("There is a cycle in relation " + self.name + ": ")
                cycle = [int(new_arr[0])] + prev_nodes_stack
                cycle = cycle[-1::-1]
                print(cycle)
                """
                return True, []

            for child_node in np.nditer(self.relations[node]):
                (found_cycle, acyclic_nodes) = self.search_for_acyclic_nodes(
                                    child_node,
                                    [node] + prev_nodes_stack)
                if found_cycle:
                    break
        return found_cycle, acyclic_nodes

    def print_graph(self):
        graph = graphviz.Digraph(name=self.name)
        for x in self.relations:
            if self.relations[x].shape != (0,):
                for y in np.nditer(self.relations[x]):
                    graph.edge(str(x), str(y))
        graph.view(filename=("res/" + self.name))
