import prova_lettura_fasta as pf
import prototipo_costruzione_grafo as cg
import calcolo_indegree_outdegree as cio
import classe_per_km1mero

kmer_list = pf.read_fasta()
graph = cg.make_de_bruijn_graph(kmer_list)
indegree, outdegree = cio.find_indegrees_and_outdegrees(graph)
print(indegree + " " +  outdegree)