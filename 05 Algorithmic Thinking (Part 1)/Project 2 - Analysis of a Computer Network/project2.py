'''
For the Project component of Module 2, you will first write Python code that 
implements breadth-first search. Then, you will use this function to compute 
the set of connected components (CCs) of an undirected graph as well as 
determine the size of its largest connected component. Finally, you will write 
a function that computes the resilience of a graph (measured by the size of its
largest connected component) as a sequence of nodes are deleted from the graph.
'''


from collections import deque

def bfs_visited(ugraph, start_node):
    '''
    Takes the undirected graph ugraph and the node start_node and returns the 
    set consisting of all nodes that are visited by a breadth-first search that
    starts at start_node.
    '''
    # initialize set of visited nodes and queue for checking
    visited = set([start_node])
    queue = deque(visited)
    # if queue is not empty, pop node and add node's neighbors to visited list
    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
    
    
def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets, where each 
    set consists of all the nodes (and nothing else) in a connected component, 
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.
    '''
    # initialize remaining nodes and connected_components
    remaining_nodes = set(ugraph.keys())
    connected_components = []
    
    # remove node from remaining_nodes queue, run BFS on it, and add results 
    # to connected_components list. Remove results from remaining_nodes
    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected_components.append(visited)
        remaining_nodes -= visited
    
    return connected_components
    
    
def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the size (an integer) of the 
    largest connected component in ugraph
    '''
    
    if not ugraph:
        return 0
    return max(map(len, cc_visited(ugraph)))
    

def compute_resilience(ugraph, attack_order):
    '''
    Takes the undirected graph ugraph, a list of nodes attack_order and 
    iterates through the nodes in attack_order. For each node in the list, the 
    function removes the given node and its edges from the graph and then 
    computes the size of the largest connected component for the resulting 
    graph. The function should return a list whose k+1th entry is the size of 
    the largest connected component in the graph after the removal of the first 
    k nodes in attack_order. The first entry (indexed by zero) is the size of 
    the largest connected component in the original graph.
    '''
    
    # initialize variables
    sizes = []
    attacked_graph = dict(ugraph)
    sizes.append(largest_cc_size(attacked_graph))
    
    # loop for calculating and removing nodes
    for item in attack_order:
        attacked_graph.pop(item)
        for node in attacked_graph:
            attacked_graph[node].discard(item)
        sizes.append(largest_cc_size(attacked_graph))
        
    return sizes
    

# TESTING
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

#print bfs_visited(EX_GRAPH1, 0)
#print cc_visited(EX_GRAPH1)
#print largest_cc_size(EX_GRAPH1)
#print compute_resilience(EX_GRAPH2, [6,5,2,0,9])