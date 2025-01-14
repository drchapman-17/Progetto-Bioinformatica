from collections import deque

def getEulerianPath(adj, s):
    path = []
    stack = []
    stack.append(s)
    while stack:
        u = stack[-1] #leggo ultimo elemento aggiunto
        if len(adj[u])!=0:
            v = adj[u].pop(0) #prendo il primo elemento
            stack.append(v) #elimino primo elemento lista adj
        else:
            path.append(stack.pop())
    return path[::-1]