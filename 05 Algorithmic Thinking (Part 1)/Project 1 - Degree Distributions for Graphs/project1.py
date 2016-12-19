# Algorithmic Thinking
# Project #1

'''
Define three constants whose values are dictionaries 
corresponding to the three directed graphs shown in these 
linked diagrams: EX_GRAPH0, EX_GRAPH1, and EX_GRAPH2. Note 
that the label for each node in the diagrams should be 
represented as an integer. You should use these graphs in 
testing your functions that compute degree distributions.
http://storage.googleapis.com/codeskulptor-alg/alg_example_graph0.jpg
http://storage.googleapis.com/codeskulptor-alg/alg_example_graph1.jpg
http://storage.googleapis.com/codeskulptor-alg/alg_example_graph2.jpg
'''

EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}
EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    '''
    Takes the number of nodes num_nodes and returns a 
    dictionary corresponding to a complete directed graph 
    with the specified number of nodes. A complete graph 
    contains all possible edges subject to the restriction 
    that self-loops are not allowed. The nodes of the 
    graph should be numbered 0 to num_nodes - 1 when 
    num_nodes is positive. Otherwise, the function returns 
    a dictionary corresponding to the empty graph.
    '''
    
    if num_nodes < 0:
        return {}
    graph = {}
    for node in range(num_nodes):
        graph[node] = set(range(num_nodes))
        graph[node].remove(node)
    return graph

def compute_out_degrees(digraph):
    '''
    Takes a directed graph digraph (represented as a 
    dictionary) and computes the out-degrees for the nodes 
    in the graph. The function should return a dictionary 
    with the same set of keys (nodes) as digraph whose 
    corresponding values are the number of edges whose 
    tail matches a particular node.
    '''
    num_edges = {}
    for key in digraph:
        num_edges[key] = len(digraph[key])
    return num_edges

def compute_in_degrees(digraph):
    '''
    Takes a directed graph digraph (represented as a 
    dictionary) and computes the in-degrees for the nodes 
    in the graph. The function should return a dictionary 
    with the same set of keys (nodes) as digraph whose 
    corresponding values are the number of edges whose 
    head matches a particular node.
    '''
    num_edges = {}
    for node in digraph:
        count = 0
        for value in digraph.values():
            if node in value:
                count +=1
        num_edges[node] = count
    return num_edges

def in_degree_distribution(digraph):
    '''
    Takes a directed graph digraph (represented as a 
    dictionary) and computes the unnormalized distribution 
    of the in-degrees of the graph. The function should 
    return a dictionary whose keys correspond to in-degrees 
    of nodes in the graph. The value associated with each 
    particular in-degree is the number of nodes with that 
    in-degree. In-degrees with no corresponding nodes in 
    the graph are not included in the dictionary.
    '''
    
    values_dict = {}
    in_degrees = []
    graph = compute_in_degrees(digraph)
    for value in graph.values():
        if value not in in_degrees:
            in_degrees.append(value)
    for degree in sorted(in_degrees):
        count = 0
        for value in graph.values():
            if value == degree:
                count += 1
        values_dict[degree] = count
    return values_dict
        

# Testing
print make_complete_graph(3)
#print make_complete_graph(5)
#print make_complete_graph(0)
#print make_complete_graph(-3)
#print compute_in_degrees(EX_GRAPH0)
#print compute_in_degrees(EX_GRAPH1)
#print compute_in_degrees(EX_GRAPH2)
#print in_degree_distribution(EX_GRAPH2)