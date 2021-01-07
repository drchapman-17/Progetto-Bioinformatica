import prova_lettura_fasta as pf
import prototipo_costruzione_grafo as cg
import calcolo_indegree_outdegree as cio
import prototipo_controllo_connessione as pcc
import classe_per_km1mero
import prototipo_controllo_grafo_euleriano as pcge

kmer_list = pf.read_fasta()
graph = cg.make_de_bruijn_graph(kmer_list)
if pcge.isSemiEulerian(graph):
    print("E' semi-euleriano")
else:
    print("Non e' semi-euleriano")