def find_indegrees_and_outdegrees(graph):
    
    indegree = dict([(node, 0) for node in graph.keys()])
    outdegree = dict([(node, 0) for node in graph.keys()])
    
    for (outbound, adjacency_list) in graph.items():
        outdegree[outbound] = len(adjacency_list)
        for inbound in adjacency_list:
            indegree[inbound] = indegree[inbound] + 1
    
    return indegree, outdegree
