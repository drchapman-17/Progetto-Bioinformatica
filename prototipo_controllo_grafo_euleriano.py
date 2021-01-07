import calcolo_indegree_outdegree as cio
import prototipo_controllo_connessione as pcc
def isSemiEulerian(graph):

    indegree, outdegree = cio.find_indegrees_and_outdegrees(graph)

    for (node, degree) in indegree.items():
        if((degree-outdegree[node])!=0):
            print(node)
            print("diverso da zero")
            print((degree-outdegree[node]))

    for line in [(str(node), [str(anode) for anode in adj]) for node, adj in graph.items()]:
        print(line)

    nodes = indegree.keys()
    unbalanced_nodes=[(node, outdegree[node] - indegree[node]) for node in nodes if outdegree[node] - indegree[node] !=0]

    if len(unbalanced_nodes)==2:
        if (unbalanced_nodes[0][1]==1 and unbalanced_nodes[1][1]==-1) or (unbalanced_nodes[0][1]==-1 and unbalanced_nodes[1][1]==1):
            s = unbalanced_nodes[0][0] if unbalanced_nodes[0][1]==1 else unbalanced_nodes[1][0]
            if not pcc.is_strongly_connected(graph, s):
                return False
            else:
                return True
    else:
        return False