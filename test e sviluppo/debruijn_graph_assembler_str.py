from Bio import SeqIO
import argparse

def build_debruijn_graph(fasta_fname, k):
    # il grafo sara' rappresentato come una lista di adiacenza; verranno anche mantenute le
    # informazioni sul bilancio (outdegree - indegree) dei nodi.
    adjacency_list = dict([])
    nodes_balance = dict([])

    for record in SeqIO.parse(fasta_fname, 'fasta'):
        sequence = str(record.seq)
        left_km1mer = None

        for i in range(0, len(sequence) + 2 - k):
            right_km1mer = sequence[i: i - 1 + k]

            # Se non esiste un nodo nel grafo per il km1mero destro, questo viene creato con
            # lista di adiacenza nulla. Naturalmente il bilancio del nuovo nodo introdotto non
            # puo' che essere pari a 0.
            #Setdefault aggiunge chiave a un dizionario con un valore specificato sse la chiave non esiste
            adjacency_list.setdefault(right_km1mer, [])
            nodes_balance.setdefault(right_km1mer, 0)

            # Viene poi creato un arco uscente dal km1mero sinistro ed entrante in quello
            # destro, sempre che il km1mero sinistro esista.
            # I bilanci di entrambi i km1meri vengono poi aggiornati.
            if left_km1mer is not None:
                adjacency_list[left_km1mer].append(right_km1mer)
                nodes_balance[right_km1mer] -= 1
                nodes_balance[left_km1mer] += 1

            # Adesso cambiamo il kmero. Cosa notiamo? Il km1mero destro dovra' essere estratto
            # dalla sequenza, mentre quello sinistro non sarà che quello destro del kmero
            # precedente!
            # In genere, si configurano due casi: o stiamo analizzando il primo km1mero della
            # stringa e non facciamo nulla se non annotarne l'esistenza, oppure stiamo
            # analizzando implicitamente un kmero, caso in cui lo si aggiunge
            # al grafo come arco.
            left_km1mer = right_km1mer

    print(adjacency_list)
    return adjacency_list, nodes_balance


def check_node_balance_condition(nodes_balance):
    # la condizione da controllare è che il bilanciamento (outdegree - indegree) dei nodi sia
    # 0 per ogni nodo, salvo che per esattamente due nodi, in cui deve valere rispettivamente
    # 1 e -1
    start_node = None
    end_node = None

    for (node, balance) in nodes_balance.items():

        # se uno dei bilanci non è nel range ammesso, es|B|lodiamo istantaneamente
        if balance > 1 or balance < -1:
            print(
                'il grafo non è semi euleriano essendoci un nodo con bilancio: ' + str(balance)
            )
            return None
        # se il bilancio è 1, allora abbiamo trovato il nodo di partenza, ma se non è unico
        #allora il grafo non è semi euleriano
        elif balance == 1:
            if start_node is None:
                start_node = node
            else:
                print(
                    'il grafo non è semi euleriano essendoci più di un nodo sorgente'
                )
                return None
        # ragionamento simile per il nodo di arrivo.
        elif balance == -1:
            if end_node is None:
                end_node = node
            else:
                print(
                    'il grafo non è semi euleriano essendoci più di un nodo pozzo'
                )
                return None
        # altrimenti il bilancio è esattamente 0 e non si fa nulla

    # dobbiamo aver trovato esattamente un nodo di partenza ed un nodo di arrivo!
    if start_node is None or end_node is None:
        return None
    else:
        return start_node


def attempt_semi_eulerian_path(adjacency_list, start_node):
    # il percorso dovrà percorrere ogni arco una ed una sola volta
    expected_path_length = sum([len(adjl) for adjl in adjacency_list.values()]) + 1

    # applichiamo l'algoritmo.
    semi_eulerian_path = []
    hohenzoller_stack = []

    def top(stack):
        return stack[-1]

    # manteniamo uno stack con i nodi da visitare; partiamo visitando il nodo con bilancio 1.
    hohenzoller_stack.append(start_node)
    while hohenzoller_stack:
        current_node = top(hohenzoller_stack)
        # se la lista degli archi del nodo corrente non e' ancora stata visitata del tutto,
        # attraversiamo uno dei possibili archi e poniamo come prossimo nodo da esaminare
        # quello in cui incide l'arco; poi coloriamo l'arco.
        if adjacency_list[current_node]:
            next_node = adjacency_list[current_node].pop()
            hohenzoller_stack.append(next_node)
        # se non ci sono piu' archi da visitare, inseriamo quel nodo all'inizio del cammino.
        else:
            semi_eulerian_path.append(hohenzoller_stack.pop())

    if len(semi_eulerian_path) == expected_path_length:
        return semi_eulerian_path[::-1]
    else:
        print(
            "il grafo non e' composto da una sola componente connessa."
        )
        return None


def extract_genome_assembly(semi_eulerian_path):
    genome_assembly = ""

    # per ogni km1mero nel cammino semi-euleriano tranne l'ultimo, prendiamo il primo simbolo
    # del km1mero.
    for km1mer in semi_eulerian_path[:-1]:
        genome_assembly += km1mer[0]

    # Nel caso dell'ultimo km1mero del cammino, prendiamo invece tutti i simboli.
    genome_assembly += semi_eulerian_path[-1]

    return genome_assembly

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--fastafile', required=True, help='Fasta File')
ap.add_argument('-k', '--kmer', required=True, help='Kmer Length')
args = vars(ap.parse_args())
fasta_fname = args['fastafile']
kmer_length = int(args['kmer'])

#adjacency_list = DeBrujinGraph representation
#nodes_balance = indegree-outdegree for each node
adjacency_list, nodes_balance = build_debruijn_graph(fasta_fname, kmer_length)

semi_eulerian_path_start = check_node_balance_condition(nodes_balance)
if semi_eulerian_path_start is not None:
    semi_eulerian_path = (
        attempt_semi_eulerian_path(adjacency_list, semi_eulerian_path_start)
    )
    if semi_eulerian_path:
        print(extract_genome_assembly(semi_eulerian_path))
    else:
        print(None)
