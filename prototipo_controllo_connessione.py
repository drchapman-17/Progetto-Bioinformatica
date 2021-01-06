from classe_per_km1mero import Km1Mer
from collections import deque
import classe_per_km1mero as cpk
def is_strongly_connected(adj):
    
    nodes = [nodes for nodes in adj.keys()]
    
    visited = dict([(node, False) for node in nodes])
    
    visited[nodes[0]] = True
    Q = deque()
    Q.append(nodes[0])
    while len(Q)!=0:
        u = Q.pop()
        for v in adj[u]:
            if not visited[v]:
                Q.append(v)
                visited[v]=True
    print([(str(node), visited[node]) for node in visited.keys() if not visited[node] ])
    return all(visited.values())
    
        
