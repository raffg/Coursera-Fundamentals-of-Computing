# Application #2 - Analysis of a Computer Network

'''
Graph exploration (that is, "visiting" the nodes and edges of a graph) is a 
powerful and necessary tool to elucidate properties of graphs and quantify 
statistics on them. For example, by exploring a graph, we can compute its 
degree distribution, pairwise distances among nodes, its connected components, 
and centrality measures of its nodes and edges. As we saw in the Homework and 
Project, breadth-first search can be used to compute the connected components 
of a graph.

In this Application, we will analyze the connectivity of a computer network as 
it undergoes a cyber-attack. In particular, we will simulate an attack on this 
network in which an increasing number of servers are disabled. In computational 
terms, we will model the network by an undirected graph and repeatedly delete 
nodes from this graph. We will then measure the resilience of the graph in 
terms of the size of the largest remaining connected component as a function 
of the number of nodes deleted.
'''

import project2
import alg_application2_provided as provided
import matplotlib.pyplot as plt
import random
import alg_upa_trial
import time
import numpy as np

def load_network_graph():
    '''
    Helper function to load the provided undirected network graph
    '''
    network_graph = provided.load_graph(provided.NETWORK_URL)
    
    return network_graph
    

def make_er_graph(num_nodes, probability):
    '''
    Helper function to implement the undirected ER graph pseudo-code. Takes a 
    number of nodes and a probability and creates a graph in which each node
    is connected to neighbors according to the probability given.
    '''
    
    graph = {}
    if num_nodes <= 0:
        return graph
    for node in range(num_nodes):
        graph[node] = set([])
    for node in range(num_nodes):
        for neighbor in range(node + 1, num_nodes):
            connection_chance = random.random()
            if connection_chance < probability:
                graph[node].add(neighbor)
                graph[neighbor].add(node)
        
    return graph
    
    
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
    Copied from Project 1
    '''
    
    if num_nodes < 0:
        return {}
    graph = {}
    for node in range(num_nodes):
        graph[node] = set(range(num_nodes))
        graph[node].remove(node)
    return graph
    
    
def upa(n_nodes, m_nodes):
    '''
    Helper function to implement the UPA algorithm
    '''
    graph = make_complete_graph(m_nodes)
    upa_alg = alg_upa_trial.UPATrial(m_nodes)
    for node in range(m_nodes, n_nodes):
        new_node_neighbors = upa_alg.run_trial(m_nodes)
        graph[node] = new_node_neighbors
        for neighbor in new_node_neighbors:
            graph[neighbor].add(node)
    return graph

    
    
def random_order(graph):
    '''
    Helper function for question 1 that takes a graph and returns a list of the 
    nodes in the graph in some random order
    '''
    nodes = list(graph.keys())
    random.shuffle(nodes)
    return nodes
    
    
def question_1():
    '''
    To begin our analysis, we will examine the resilience of the computer 
    network under an attack in which servers are chosen at random. We will 
    then compare the resilience of the network to the resilience of ER and UPA 
    graphs of similar size.
    '''
    
    # set constants to make the three graphs the same num nodes and edges
    num_nodes = 1239
    p = .004
    m = 2
    
    # create the three graphs
    network = load_network_graph()
    er_graph = make_er_graph(num_nodes, p)
    upa_graph = upa(num_nodes, m)
    
    # set the order of node attacks
    network_attack = random_order(network)
    er_attack = random_order(er_graph)
    upa_attack = random_order(upa_graph)
    
    # compute resilience of each network
    network_resilience = project2.compute_resilience(network, network_attack)
    er_resilience = project2.compute_resilience(er_graph, er_attack)
    upa_resilience = project2.compute_resilience(upa_graph, upa_attack)
    
    # plot results
    plt.plot(network_resilience, 'b-', label='Computer network')
    plt.plot(er_resilience, 'r-', label='ER graph, p=0.004')
    plt.plot(upa_resilience, 'g-', label='UPA graph, m=2')
    plt.legend(loc='upper right')

    plt.title('Resilience of networks under a random attack');
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.show()
    
    return
    

def fast_targeted_order(ugraph):
    """
    Helper function for Question 3
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    new_graph = dict(ugraph)  
    degree_sets = []
    order = []
    n = len(new_graph)
    degree_sets = [set() for _ in xrange(n)]
    for node in new_graph:
        node_deg = len(new_graph[node])
        degree_sets[node_deg].add(node)
        
    for degree in range(n-1, -1, -1):
        while len(degree_sets[degree]) != 0:
            max_degree_node = degree_sets[degree].pop()
            neighbors = new_graph[max_degree_node]
            for neighbor in neighbors:
                neighbor_degree = len(new_graph[neighbor])
                degree_sets[neighbor_degree].discard(neighbor)
                degree_sets[neighbor_degree-1].add(neighbor)
                new_graph[neighbor].remove(max_degree_node)
            order.append(max_degree_node)
            new_graph.pop(max_degree_node)
    return order

    
def running_time_best():
    '''
    Helper function for Question 3
    '''
    
    running_times_norm = []
    running_times_fast = []
    for n in range (10, 1000, 10):
        upa_graph = upa(n, 5)
        start = time.clock()
        provided.targeted_order(upa_graph)   
        stop = time.clock()
        elapsed_time = stop - start
        running_times_norm.append(elapsed_time)
        start = time.clock()
        fast_targeted_order(upa_graph)   
        stop = time.clock()
        elapsed_time = stop - start
        running_times_fast.append(elapsed_time)
    
    return running_times_norm, running_times_fast
    
    
def question_3():
    '''
    For this question, your task is to implement fast_targeted_order and then 
    analyze the running time of these two methods on UPA graphs of size n with m=5.
    '''
    
    time_norm, time_fast = running_time_best()
    
    x = np.arange(10, 1000, 10)
    plt.plot(x, time_norm, 'b-', label='targeted_order')
    plt.plot(x, time_fast, 'r-', label='fast_targeted_order')

    plt.legend(loc='upper right')

    plt.title('Order of Growth of Target Functions using Spyder (Python 2.7)\n');
    plt.xlabel('Number of Nodes of UPA Graph, m = 5')
    plt.ylabel('Running Time in seconds')
    plt.show()
    
    return
    
    
def question_4():
    '''
    Using targeted_order (or fast_targeted_order), your task is to compute a 
    targeted attack order for each of the three graphs (computer network, ER, 
    UPA) from Question 1. Then, for each of these three graphs, compute the 
    resilience of the graph using compute_resilience. Finally, plot the 
    computed resiliences as three curves (line plots) in a single standard 
    plot. As in Question 1, please include a legend in your plot that 
    distinguishes the three plots. The text labels in this legend should 
    include the values for p and m that you used in computing the ER and UPA 
    graphs, respectively.
    '''
    
    # set constants to make the three graphs the same num nodes and edges
    num_nodes = 1239
    p = .004
    m = 2
    
    # create the three graphs
    network = load_network_graph()
    er_graph = make_er_graph(num_nodes, p)
    upa_graph = upa(num_nodes, m)
    
    # set the order of node attacks
    network_attack = provided.targeted_order(network)
    er_attack = provided.targeted_order(er_graph)
    upa_attack = provided.targeted_order(upa_graph)
    
    # compute resilience of each network
    network_resilience = project2.compute_resilience(network, network_attack)
    er_resilience = project2.compute_resilience(er_graph, er_attack)
    upa_resilience = project2.compute_resilience(upa_graph, upa_attack)
    
    # plot results
    plt.plot(network_resilience, 'b-', label='Computer network')
    plt.plot(er_resilience, 'g-', label='ER graph, p=0.004')
    plt.plot(upa_resilience, 'r-', label='UPA graph, m=2')
    plt.legend(loc='upper right')

    plt.title('Resilience of networks under a targeted attack');
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.show()
    
    return
    
    
#question_1()
#question_3()
#question_4()
    
# Testing
#print make_er_graph(10, .1)
#print random_order({0: set([4]), 1: set([8, 4]), 2: set([]), 3: set([8]), 4: set([0, 1, 9]), 5: set([8]), 6: set([]), 7: set([]), 8: set([1, 3, 5]), 9: set([4])})