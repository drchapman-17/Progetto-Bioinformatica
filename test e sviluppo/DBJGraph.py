class DBJGraph:
    def __init__(self, adj):
        self.adj = adj
        self.nodes = adj.keys()
        self.indegreeOutdegree()

    def indegreeOutdegree(self):
        indegree = dict([(node, 0) for node in self.nodes])
        outdegree = dict([(node, 0) for node in self.nodes])
        
        for (outbound, adjacency_list) in self.adj.items():
            outdegree[outbound] = len(adjacency_list)
            for inbound in adjacency_list:
                indegree[inbound] = indegree[inbound] + 1

    def getIndegreeOutDegree(self):
        return self.indegree, self.outdegree
    