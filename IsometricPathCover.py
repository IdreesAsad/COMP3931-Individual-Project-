# Author: Idrees Asad
# Individual Project
# Description : An approximation algorithm which contructs an ISP of a DAG.

from collections import deque

def modifiedBfs(graph, start_node):

    n = len(graph)                      # number of nodes in the graph
    visited = [False] * n               # array of visited nodes
    queue = deque([start_node])
    visited[start_node] = True
    traversal_order = []

    # begin bfs

    while queue:
        
        node = queue.popleft()
        traversal_order.append(node)
        
        # look at neighbours of the current node
        for neighbour in range(n):
            if graph[node][neighbour] == 1 and not visited[neighbour]:

                # If there is an edge and the neighbor is not visited
                queue.append(neighbour)
                visited[neighbour] = True

    return traversal_order

input_graph = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

print(modifiedBfs(input_graph, 0))