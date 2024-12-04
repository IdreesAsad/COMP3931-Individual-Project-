# Author: Idrees Asad
# Individual Project
# Description : An approximation algorithm which contructs an ISP of a DAG.

import networkx as nx

def isometric_path_cover(graph, start_vertex):
    
    def modified_bfs(graph, start_vertex):
        '''Executes a modified BFS algorithm which produces a directed acyclic graph'''

        dag = nx.digraph()
        distances = nx.single_source_shortest_path_length(graph, start_vertex)

        for x, y in graph.edges(): # orients the edges from top to bottom. 
            if distances[x] < distances[y]:
                dag.add_edge(x, y)
            elif distances[y] < distances[x]:
                dag.add_edge(y, x)

        '''if distances are equal then the edges are on the same layer and are not added to the DAG'''

        return dag