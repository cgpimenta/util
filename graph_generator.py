#!/usr/bin/env python3

__author__ = 'Cristiano G. Pimenta'

"""
Generates an edgelist of a graph whose connected components can be simple
paths, trees, complete bipartite graph or cyles. It also generates a
permutation of the vertices of each component.

Copyright (C) 2019  Cristiano G. Pimenta

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import copy
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

from networkx.algorithms.bipartite.generators import complete_bipartite_graph
from networkx.generators.classic import path_graph, cycle_graph
from networkx.generators.trees import random_tree


def get_graph(max_size):
    graph_type = np.random.randint(1, 5)
    num_nodes = np.random.randint(5, max(max_size, 5) + 1)

    if graph_type == 1:
        return path_graph(num_nodes), graph_type
    elif graph_type == 2:
        g = random_tree(num_nodes)

        max_degree = 0

        for n in g.degree:
            max_degree = max(max_degree, n[1])

        if max_degree <= 2:
            graph_type = 1

        return g, graph_type
    elif graph_type == 3:
        part1 = np.random.randint(2, max(max_size / 2, 2) + 1)
        part2 = np.random.randint(3, max(max_size / 2, 3) + 1)
        return complete_bipartite_graph(part1, part2), graph_type
    elif graph_type == 4:
        return cycle_graph(num_nodes), graph_type
    else:
        sys.exit('Something unexpected happened!')


def generate_graphs(max_num_nodes, max_num_edges, max_size):
    its_no_update = 0

    global num_nodes, num_edges, edges, permutation
    global path, tree, bipartite, cycle

    print('Max num nodes {:,}'.format(max_num_nodes))
    print('Max num edges {:,}\n'.format(max_num_edges))

    while num_nodes < max_num_nodes and num_edges < max_num_edges:
        if its_no_update > 50:
            break

        g, g_type = get_graph(max_size)
        g_nodes = g.number_of_nodes()
        g_edges = g.number_of_edges()

        if g_nodes + num_nodes <= max_num_nodes and g_edges + num_edges <= max_num_edges:
            for e in g.edges:
                edges.append(tuple(x+num_nodes+1 for x in e))
            
            nodes = [x+num_nodes+1 for x in g.nodes]
            nodes_perm = copy.deepcopy(nodes)
            np.random.shuffle(nodes_perm)

            for i in zip(nodes, nodes_perm):
                permutation.append(i)

            # print(list(zip(nodes, nodes_perm)))
            
            num_nodes += g_nodes
            num_edges += g_edges

            if g_type == 1:
                path += 1
            elif g_type == 2:
                tree += 1
            elif g_type == 3:
                bipartite += 1
            elif g_type == 4:
                cycle += 1
        else:
            its_no_update += 1
            max_size /= 2

    print("Num nodes: {:,}".format(num_nodes))
    print("Num edges: {:,}\n".format(num_edges))


def generate_permutation(num_nodes):
    nodes = [x for x in range(1, num_nodes + 1)]
    np.random.shuffle(nodes)
    return nodes


def main(max_num_nodes, max_num_edges, max_size, seed, output_file):
    np.random.seed(seed)

    # print(max_num_nodes)
    # print(max_num_edges)
    # print(max_size)

    global num_nodes, num_edges, edges, permutation
    num_nodes = 0
    num_edges = 0
    edges = []
    permutation = []

    global path, tree, bipartite, cycle
    path, tree, bipartite, cycle = 0, 0, 0, 0

    generate_graphs(max_num_nodes, max_num_edges, max_size)

    print('path: {} - tree: {} - bipartite: {} - cycle: {}' \
        .format(path,tree, bipartite, cycle))
    print('Total:', path+tree+bipartite+cycle)

    with open(output_file, 'w') as f:
        f.write('{} {}\n'.format(num_nodes, num_edges))

        for e in edges:
            f.write('{} {}\n'.format(e[0], e[1]))

        for p in permutation:
            f.write('{} {}\n'.format(p[0], p[1]))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--max-num-nodes', type=int, default=10**5,
                        help='Maximum number of nodes.')

    parser.add_argument('-m', '--max-num-edges', type=int, default=10**6,
                        help='Maximum number of edges.')

    parser.add_argument('-l', '--max-ship-size', required=True, type=int,
                        help='Maximum size of each ship.')

    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='Seed of the pseudo-random number generator.')

    parser.add_argument('-o', '--output-file', required=True, type=str,
                        help='File where output will be written.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if (args.max_num_nodes < 10 or args.max_num_nodes > 10**5):
        sys.exit('max_num_nodes must be >= 10 and <= 100000.')

    if args.max_num_edges < 8 or args.max_num_edges > 10**6:
        sys.exit('max_num_edges must be >= 8 and <= 1000000.')

    if args.max_ship_size < 5:
        sys.exit('max_ship_size must be >= 5.')
    # print(args)

    main(args.max_num_nodes, args.max_num_edges,
         args.max_ship_size, args.seed, args.output_file)
