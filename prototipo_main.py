import prova_lettura_fasta as pf
import prototipo_costruzione_grafo as cg
import calcolo_indegree_outdegree as cio
import prototipo_controllo_connessione as pcc
import classe_per_km1mero

kmer_list = pf.read_fasta()
graph = cg.make_de_bruijn_graph(kmer_list)
indegree, outdegree = cio.find_indegrees_and_outdegrees(graph)

#print(indegree.items())
for (node, degree) in indegree.items():
    if((degree-outdegree[node])!=0):
        print(node)
        print("diverso da zero")
        print((degree-outdegree[node]))

for line in [(str(node), [str(anode) for anode in adj]) for node, adj in graph.items()]:
    print(line)
#print((degree-outdegree[node]))
if not pcc.is_strongly_connected(graph):
    print("A Non e' euleriano")
else:
    nodes = indegree.keys()
    unbalanced_nodes=[(node, outdegree[node] - indegree[node]) for node in nodes if outdegree[node] - indegree[node] !=0]
    if len(unbalanced_nodes)==2:
        if (unbalanced_nodes[0][1]==1 and unbalanced_nodes[1][1]==-1) or (unbalanced_nodes[0][1]==-1 and unbalanced_nodes[1][1]==1):
            print("B E' euleriano")
    else:
        print("C Non e' euleriano")