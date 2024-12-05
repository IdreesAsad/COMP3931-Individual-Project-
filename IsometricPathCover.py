# Author: Idrees Asad
# Individual Project
# Description : An approximation algorithm which contructs an ISP of a DAG.

import networkx as nx
import matplotlib.pyplot as plt

def isometric_path_cover(graph, start_vertex):
    
    def modified_bfs(graph, start_vertex):
        '''Executes a modified BFS algorithm which produces a directed acyclic graph'''

        dag_graph = nx.DiGraph()
        distances = nx.single_source_shortest_path_length(graph, start_vertex)

        for x, y in graph.edges(): # orients the edges from top to bottom. 
            if distances[x] < distances[y]:
                dag_graph.add_edge(x, y)
            elif distances[y] < distances[x]:
                dag_graph.add_edge(y, x)

        '''if distances are equal then the edges are on the same layer and are not added to the DAG'''

        #print("DAG Nodes:", dag_graph.nodes())
        #print("DAG Edges:", dag_graph.edges())

        return dag_graph

    def bipartite(dag_graph):

        '''Tranforms the DAG to a bipartite graph and then finds the maximum matching'''

        bipartite_graph = nx.Graph()
        left_partition = set()
        right_partition = set()

        for x, y in dag_graph.edges():
            left_partition.add(f"L-{x}")
            right_partition.add(f"R-{y}")
            bipartite_graph.add_edge(f"L-{x}", f"R-{y}") # each edge now connects the left and right partition

        # Ensures the graph is connected by partitioning correctly
        nx.set_node_attributes(bipartite_graph, {node: 0 for node in left_partition}, "bipartite") 
        nx.set_node_attributes(bipartite_graph, {node: 1 for node in right_partition}, "bipartite")

        #print("Bipartite Graph Nodes:", bipartite_graph.nodes())
        #print("Bipartite Graph Edges:", bipartite_graph.edges())

        max_matching = nx.bipartite.maximum_matching(bipartite_graph, top_nodes=left_partition)
        #print("Maximum Matching:", max_matching)

        # Finding paths from maximum matching set by skipping (L\R -)
        matched_edges = {int(u[2:]): int(v[2:]) for u, v in max_matching.items() if u.startswith("L-")}
        #print("matched edges:", matched_edges)

        return matched_edges

    def matching_paths(dag_graph, matched_edges):

        '''Finds the paths in the DAG from the maximum matching'''
        '''The value of matched_edges is the match of it's index'''

        paths = []
        visited = set()

        for node in dag_graph.nodes():
            # Start a path if the node hasn't been visited and is not the target of a node (the corresponding match)
            if node not in visited and node not in matched_edges.values():
                path = [node]
                visited.add(node)
                current = node

                # Follow the matching to construct the path
                while current in matched_edges:
                    next_node = matched_edges[current]
                    if next_node in visited:
                        break
                    path.append(next_node)
                    visited.add(next_node)
                    current = next_node

                paths.append(path)


        return paths

        
    dag = modified_bfs(graph, start_vertex)
    matched_edges = bipartite(dag)
    pathcover_dag = matching_paths(dag, matched_edges)

    isometric_paths = []
    for path in pathcover_dag:
        isometric_paths.append(path)

    return isometric_paths


def draw_path(graph, paths):
    ''' Highlightd the IPC on the graph'''

    colors = plt.cm.get_cmap("tab10", len(paths))  # Uses distinct colours

    pos = nx.spring_layout(graph) 
    nx.draw(graph, pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=500)

    # Highlighting paths
    for i, path in enumerate(paths):
        path_edges = [(path[j], path[j+1]) for j in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color=[colors(i)], width=2)
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color=[colors(i)], node_size=600)

    plt.title("Isometric Paths")
    plt.show()


def best_start_node(graph):
    """ Finds the IPC at all nodes and returns the one of smallest size"""
    best_paths = None
    best_start = None
    best_size = float('inf')

    for start_node in graph.nodes():
        paths = isometric_path_cover(graph, start_node)

        # Check if this is the best result so far
        if len(paths) < best_size:
            best_size = len(paths)
            best_paths = paths
            best_start = start_node

    print(f"Best start node: {best_start} with {best_size} paths")

    return best_start, best_paths


#Input data
G = nx.Graph()
G.add_edges_from([(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])

best_start, best_paths = best_start_node(G)
print(f"Optimal Isometric Path Cover starting from node {best_start}:")
for path in best_paths:
    print(path)
draw_path(G, best_paths)


