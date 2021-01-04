import prova_lettura_fasta as pf
import prototipo_costruzione_grafo as cg
import calcolo_indegree_outdegree as cio
import classe_per_km1mero

kmer_list = pf.read_fasta()
graph = cg.make_de_bruijn_graph(kmer_list)
indegree, outdegree = cio.find_indegrees_and_outdegrees(graph)

#print(indegree.items())
#for (node, degree) in indegree.items():
#    if((degree-outdegree[node])!=0):
#        print(node)
#        print("diverso da zero")
#        print((degree-outdegree[node]))
# 
# 
# 
# #print((degree-outdegree[node]))

nodes = indegree.keys()
unbalanced_nodes=dict([(node, outdegree[node] - indegree[node]) for node in nodes if outdegree[node] - indegree[node] !=0 ])
if len(unbalanced_nodes)==2:
    if (unbalanced_nodes.values[0]==1 and unbalanced_nodes.values[1]==-1) or (unbalanced_nodes.values[0]==-1 and unbalanced_nodes.values[1]==-1):
        print("E' euleriano")
else:
    print("Non e' euleriano")
    
