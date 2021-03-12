**Progetto del corso "Elementi di Bioinformatica" Università degli Studi Milano Bicocca anno 2020/2021**

**Componenti del gruppo: Ciapponi, Colombo, Lucarella**



**Consegna:**
Sviluppare un piccolo Assemblatore che, preso come input un file FASTA contenente delle Read e un numeor intero K, costruisca il genoma corrispondente 
con l'ausilio di un grafo di De Bruijn.
Il programma deve:
  1. calcolare tutti k-meri distinti inclusi nelle read
  2. calcolare il grafo di de Bruijn corrispondente
  3. verificare che il grafo sia semi euleriano. In questo caso calcola un cammino euleriano
  4. analizzare il cammino per visualizzare il genoma assemblato



**Procedura per chiamare il programma da linea di comando:**

**$** python debruijn_graph_assembler.py  -f [file fasta] -k [dimensione kmero]
  
  
  
**Descrizione Funzioni del programma:**

  1. *build_debruijn_graph*(fasta_fname, k):
      Estrae i kmeri (di dimensione k) dalle read contenute nel file fasta "fasta_fname" e va a coustruire la lista di adiacenza di un grafo di De Bruijn
      calcolando contemporaneamente il bilanciamento di ogni nodo.
      
      *Output*: Dizionario che contiene la lista di adiacenza del grafo, Dizionario che associa ogni nodo al suo bilanciamento (Indigree-outdegree).
      
  2. *check_node_balance_condition*(nodes_balance):
      Controlla il bilanciamento dei nodi del Grafo costruito per verificare se esistono solo 2 nodi con bilanciamento = +1/-1 e i restanti con bilanciamento 0.
      Questa è una delle proprietà necessarie affinchè il grafo sia semi euleriano.\n
      La funzione effettua operazioni di conteggio e confronto dei valori dei bilanciamenti dei nodi nel dizionario "nodes_balance".
      
      *Output*: nodo iniziale del grafi euleriano.
      
  3. *attempt_semi_eulerian_path*(adjacency_list, start_node):
      la funzione calcola il cammino euleriano nel grafo implementando l'algoritmo di Hierholzer.
      Dopo aver applicato l'algoritmo il numero di nodi attraversati viene comparato con il numero di nodi attesi (cioè tutti i nodi).
      Nel caso in qui questa comparaziomne abbia esito negativo l'algoritmo si ferma perchè ciò significa che il grafo è formato da più componenti connesse e quindi non 
      è semi-euleriano.
      
      *Output*: Lista contenente l'ordine di visita dei nodi (ribaltata).
      
  4. *extract_genome_assembly*(semi_eulerian_path):
      Concatena i nodi del cammino in modo da ottenere la stringa che rappresenta il genoma.
      
      *Output*: Stringa che rappresenta il genoma.
