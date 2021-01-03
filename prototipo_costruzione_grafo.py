def make_de_bruijn_graph(k_mers_list):
    #Left and right (k-1)-mers are extracted from the k_mers list. 
    #The left (k-1)-mer is obtained by taking the k-mer without its last base, 
    #and the right (k-1)-mer is obtained by leaving out the first base instead.
    #For instance, given the k-mer 'gatta', the left (k-1)-mer is 'gatt', and 
    #the right (k-1)-mer is 'atta'. 
    left_km1_mers = [k_mer[:-1] for k_mer in k_mers_list]
    right_km1_mers = [k_mer[1:] for k_mer in k_mers_list]
    
    '''
    The graph will be represented as a dictionary where each pair represents
    a node: the key will be the label of the node, and the value associated 
    to it will be its adjacency list.
    The following code could probably be optimised by making it work on 
    a single cycle, but for this prototype version I'm trying to keep the code 
    as compact and as terse as possible.
    '''
    
    #Each (k-1)-mer, be it left or right, is associated with a  single node
    #in the graph. 
    #For now their adjacency lists are left empty.
    nodes = [(km1_mer, []) for km1_mer in set(left_km1_mers + right_km1_mers)]
    #The graph is made from the node list.
    #Making it into a dictionary allows us to exploit the hash map data
    #structure for constant-time access to each node.
    graph = dict(nodes)
    
    #Then, the arcs are added. For every left+right (k-1)-mer pair, an arc
    #is added to th #graph to represent the k-mer obtained by merging
    #the two (k-1)-mers back together.
    for index in range(0, len(k_mers_list)):
        graph[left_km1_mers[index]].append(right_km1_mers[index])

    
    return graph
