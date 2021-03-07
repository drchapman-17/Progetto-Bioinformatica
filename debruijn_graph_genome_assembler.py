#!/usr/bin/env python
# coding: utf-8

# In[166]:


from Bio import SeqIO


# In[175]:


class Km1MerTrieNode:
    def __init__(self, label):
        self.children = {}
        self.label = label

class Km1MerTrie:
    def __init__(self):
        self.root = Km1MerTrieNode(-1)
        self.dictionary_size = 0
    
    def get_km1mer_code(self, km1mer):
        curr_node = self.root
        freshly_added = False
        
        for base in km1mer:
            if base not in curr_node.children:
                curr_node.children[base] = Km1MerTrieNode(self.dictionary_size)
                freshly_added = True
                
            curr_node = curr_node.children[base]
        
        if freshly_added: self.dictionary_size += 1
        return curr_node.label, freshly_added


# In[176]:


def build_debruijn_graph(fasta_fname, k):
    km1mers_trie = Km1MerTrie()
    idx_km1mer_map = []
    adjacency_list = []
    nodes_balance = []
    
    for record in SeqIO.parse(fasta_fname, 'fasta'):
        sequence = str(record.seq)
        left_km1mer = None
        
        for i in range(0, len(sequence) + 2 - k):
            right_km1mer_repr = sequence[i : i - 1 + k]
            #troviamo il codice per il km1mero
            right_km1mer, freshly_added = km1mers_trie.get_km1mer_code(right_km1mer_repr)
            
            #se abbiamo trovato un nuovo km1mero aggiungiamolo alla mappa ed alla 
            #lista di adiacenza, e inizializziamo il suo bilancio a 0
            if freshly_added:
                idx_km1mer_map.append(right_km1mer_repr)
                adjacency_list.append([])
                nodes_balance.append(0)
            
            #Viene poi creato un arco uscente dal km1mero sinistro ed entrante in quello 
            #destro, sempre che il km1mero sinistro esista.
            #I bilanci di entrambi i km1meri vengono poi aggiornati.
            #Notare come il reference alle due liste dovrà necessariamente funzionare, essendo
            #i kmeri ordinati per scoperta.
            if left_km1mer is not None:
                adjacency_list[left_km1mer].append(right_km1mer)
                nodes_balance[right_km1mer] -= 1
                nodes_balance[left_km1mer] += 1
            
            #Adesso cambiamo il kmero. Cosa notiamo? Il km1mero destro dovrà essere estratto 
            #dalla sequenza, mentre quello sinistro non sarà che quello destro del kmero 
            #precedente!
            #In genere, si configurano due casi: o stiamo analizzando il primo km1mero della 
            #stringa e non facciamo nulla se non annotarne l'esistenza, oppure stiamo 
            #analizzando implicitamente un kmero, caso in cui lo si aggiunge
            # al grafo come arco.
            left_km1mer = right_km1mer
    
    return adjacency_list, nodes_balance, idx_km1mer_map


# In[177]:


def check_node_balance_condition(nodes_balance):
    
    #la condizione da controllare è che il bilanciamento (outdegree - indegree) dei nodi sia
    #0 per ogni nodo, salvo che per esattamente due nodi, in cui deve valere rispettivamente 
    #1 e -1
    
    start_node = None
    end_node = None
    
    for (node, balance) in enumerate(nodes_balance):
        
        #se uno dei bilanci non è nel range ammesso, es|B|lodiamo istantaneamente
        if balance > 1 or balance < -1:
            print(
                'il grafo non è semi euleriano essendoci un nodo con bilancio: ' + str(balance)
            )
            return None
        #se il bilancio è 1, allora abbiamo trovato il nodo di partenza... ma se non è unico
        #si es|B|lode.
        elif balance == 1:
            if start_node is None:
                start_node = node
            else:
                print(
                    'il grafo non è semi euleriano essendoci più di un nodo sorgente'
                )
                return None
        #ragionamento simile per il nodo di arrivo.
        elif balance == -1:
            if end_node is None:
                end_node = node
            else:
                print(
                    'il grafo non è semi euleriano essendoci più di un nodo pozzo'
                )
                return None
        #altrimenti il bilancio è esattamente 0 e non si fa nulla
        
    #dobbiamo aver trovato esattamente un nodo di partenza ed un nodo di arrivo!
    if start_node is None or end_node is None:
        return None
    else:
        return start_node


# In[178]:


def attempt_semi_eulerian_path(adjacency_list, start_node):
    
    #il percorso dovrà percorrere ogni arco una ed una sola volta
    expected_path_length = sum([len(adjl) for adjl in adjacency_list]) + 1
    
    #applichiamo l'algoritmo di Hohenzoller (check spelling). 
    semi_eulerian_path = []
    hohenzoller_stack =  []
    
    def top(stack):
        return stack[-1]
    
    #manteniamo uno stack con i nodi da visitare; partiamo visitando il nodo con bilancio 1.
    hohenzoller_stack.append(start_node)
    while hohenzoller_stack:
        current_node = top(hohenzoller_stack)
        #se la lista degli archi del nodo corrente non è ancora stata visitata del tutto,
        #attraversiamo uno dei possibili archi e poniamo come prossimo nodo da esaminare 
        #quello in cui incide l'arco; poi coloriamo l'arco.
        if adjacency_list[current_node]:
            next_node = adjacency_list[current_node].pop()
            hohenzoller_stack.append(next_node)
        #se non ci sono più archi da visitare, inseriamo quel nodo all'inizio del cammino.
        else:
            semi_eulerian_path.append(hohenzoller_stack.pop())

    if len(semi_eulerian_path) == expected_path_length:
        return semi_eulerian_path[::-1]
    else:
        print(
            'il grafo non è composto da una sola componente connessa.'
        )
        return None
            


# In[179]:


def extract_genome_assembly(semi_eulerian_path, idx_km1mer_map):
    
    genome_assembly = ""
    
    #per ogni km1mero nel cammino semi-euleriano tranne l'ultimo, prendiamo il primo simbolo 
    #del km1mero.
    for km1mer in semi_eulerian_path[:-1]:
        genome_assembly += idx_km1mer_map[km1mer][0]
    
    #Nel caso dell'ultimo km1mero del cammino, prendiamo invece tutti i simboli.
    genome_assembly += idx_km1mer_map[semi_eulerian_path[-1]]
    
    return genome_assembly


# In[180]:


def main_prog(fasta_fname, kmer_length):
    
    adjacency_list, nodes_balance, idx_km1mer_map = (
        build_debruijn_graph(fasta_fname, kmer_length)
    )
    
    semi_eulerian_path_start = check_node_balance_condition(nodes_balance)
    if semi_eulerian_path_start is not None:
        semi_eulerian_path = (
            attempt_semi_eulerian_path(adjacency_list, semi_eulerian_path_start)
        )
        if semi_eulerian_path:
            return extract_genome_assembly(semi_eulerian_path, idx_km1mer_map)
        else:
            return None

