# Author: Idrees Asad
# Individual Project
# Description : An approximation algorithm which contructs an ISP of a DAG.

import networkx as nx

def isometric_path_cover(graph, start_vertex):
    
    def modified_bfs(graph, start_vertex):
        '''Executes a modified BFS algorithm which produces a directed acyclic graph'''

        dag_graph = nx.digraph()
        distances = nx.single_source_shortest_path_length(graph, start_vertex)

        for x, y in graph.edges(): # orients the edges from top to bottom. 
            if distances[x] < distances[y]:
                dag_graph.add_edge(x, y)
            elif distances[y] < distances[x]:
                dag_graph.add_edge(y, x)

        '''if distances are equal then the edges are on the same layer and are not added to the DAG'''

        return dag_graph

    def bipartite(dag_graph):

        '''Tranforms the DAG to a bipartite graph and then finds the maximum matching'''

        bipartite_graph = nx.Graph()

        for x, y in dag_graph.edges():
            bipartite_graph.add_edge(f"L-{x}", f"R-{y}") # each edge now connects the left and right partition

        max_matching = nx.bipartite.maximum_matching(bipartite_graph)
