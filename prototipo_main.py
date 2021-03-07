import prova_lettura_fasta as pf
import prototipo_costruzione_grafo as cg
import calcolo_indegree_outdegree as cio
import prototipo_controllo_connessione as pcc
import classe_per_km1mero
import prototipo_controllo_grafo_euleriano as pcge
import prototipo_percorso_euleriano as ppe

kmer_list = pf.read_fasta("prova.fa", 3)
graph = cg.make_de_bruijn_graph(kmer_list)
isSemiEulerian, s = pcge.isSemiEulerian(graph)

if isSemiEulerian:
    print("E' semi-euleriano")
    path = ppe.getEulerianPath(graph, s)
    #print([str(node) for node in path])
    genome_bucket = [str(km1mero)[0] for km1mero in path[0:-1]]
    genome_bucket.append(str(path[-1]))
    genome = "".join(genome_bucket)
    print("Genoma:  "+genome)
else:
    print("Non e' semi-euleriano")