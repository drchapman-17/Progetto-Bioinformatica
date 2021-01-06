def is_strongly_connected(graph):
    
    nodes = graph.keys()
    
    visited = dict([(node, False) for node in nodes])
    
    visited[nodes[0]] = True
    for node in nodes:
        if(not visited[node]): return False
        dfs_visit(graph, node, visited)
        
    return True
    
def dfs_visit(adj, u, visited):
    
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            dfs_visit(adj, v, visited)
