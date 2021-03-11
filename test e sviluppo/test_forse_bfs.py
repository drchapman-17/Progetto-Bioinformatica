
from collections import deque
adj={"1":["2","3"],
     "2":["4","5"],
     "3":["6"],
     "4":[],
     "5":[],
     "6":[]}
    
s="1"
nodes = [nodes for nodes in adj.keys()]

visited = dict([(node, False) for node in nodes])
visited[s] = True
Q = deque()
Q.appendleft(s)
while Q:
    u = Q.pop()
    for v in adj[u]:
        if not visited[v]:
            Q.appendleft(v)
            print(v)
            visited[v]=True