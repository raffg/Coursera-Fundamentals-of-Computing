# Application #3 - Comparison of Clustering Algorithms
'''
In Project 3, you implemented two methods for clustering sets of data. In this 
Application, we will analyze the performance of these two methods on various 
subsets of our county-level cancer risk data set. In particular, we will 
compare these two clustering methods in three areas:

Efficiency - Which method computes clusterings more efficiently?
Automation - Which method requires less human supervision to generate 
reasonable clusterings?
Quality - Which method generates clusterings with less error?
'''

import project3
import alg_cluster
import matplotlib.pyplot as plt
import random
import time
import urllib2



DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def gen_random_clusters(num_clusters):
    '''
    creates a list of clusters where each cluster in this list corresponds to 
    one randomly generated point in the square with corners (±1,±1)
    '''
    
    cluster_list = []
    for cluster in xrange(num_clusters):
        x = random.choice([1, -1]) * random.random()
        y = random.choice([1, -1]) * random.random()
        cluster_list.append(alg_cluster.Cluster(set([]), x, y, 1, 0))
    return cluster_list
    
    
def question_1():
    '''
    Computes the running times of the functions slow_closest_pair and 
    fast_closest_pair for lists of clusters of size 2 to 200.

    Once you have computed the running times for both functions, plot the 
    result as two curves combined in a single plot. (Use a line plot for each 
    curve.) The horizontal axis for your plot should be the the number of 
    initial clusters while the vertical axis should be the running time of the 
    function in seconds. Please include a legend in your plot that 
    distinguishes the two curves.
    '''

    xvals = range(2, 200)
    slow_yvals = []
    fast_yvals = []
    for num in xvals:
        cluster_list = gen_random_clusters(num)
        initial = time.time()
        result1 = project3.slow_closest_pair(cluster_list)
        final = time.time()
        slow_yvals.append((final - initial))
    for num in xvals:
        cluster_list = gen_random_clusters(num)
        initial = time.time()
        result2 = project3.fast_closest_pair(cluster_list)
        final = time.time()
        fast_yvals.append((final - initial))
    plt.plot(xvals, slow_yvals, color='r', label="Slow Closest Pair")
    plt.plot(xvals, fast_yvals, color='b', label="Fast Closest Pair")
    plt.legend(loc=2)
    plt.title("Efficiency of Slow and Fast Closest Pairs Algorithms")
    plt.xlabel("Number of Initial Clusters")
    plt.ylabel("Running Time in Seconds")
    plt.show()
    
    return result1, result2
    
    
def compute_distortion(cluster_list, data_table):
    '''
    takes a list of clusters and uses cluster_error to compute its distortion
    '''
    
    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion
    
    
def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
    
    
def question_7():
    '''
    Write a function compute_distortion(cluster_list) that takes a list of 
    clusters and uses cluster_error to compute its distortion. Now, use 
    compute_distortion to compute the distortions of the two clusterings in 
    questions 5 and 6. Enter the values for the distortions (with at least 
    four significant digits) for these two clusterings in the box below. 
    Clearly indicate the clusterings to which each value corresponds.

    As a check on the correctness of your code, the distortions associated with 
    the 16 output clusters produced by hierarchical clustering and k-means 
    clustering (with 5 iterations) on the 290 county data set are approximately 
    2.575×1011 and 2.323×1011, respectively.
    '''
    
    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], 
                                                  line[2], line[3], line[4]))
        
    cluster_list_h = project3.hierarchical_clustering(singleton_list, 9)
    print "Distortion of", len(cluster_list_h), "hierarchical clusters"
    print compute_distortion(cluster_list_h, data_table)
    
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], 
                                                  line[2], line[3], line[4]))
        
    cluster_list_k = project3.kmeans_clustering(singleton_list, 9, 5)	
    print "Distortion of", len(cluster_list_k), "k-means clusters"
    print compute_distortion(cluster_list_k, data_table)
    
    return
    
    
def question_10(data_set):
    '''
    Compute the distortion of the list of clusters produced by hierarchical 
    clustering and k-means clustering (using 5 iterations) on the 111, 290, 
    and 896 county data sets, respectively, where the number of output clusters 
    ranges from 6 to 20 (inclusive).Important note:To compute the distortion 
    for all 15 output clusterings produced by hierarchical_clustering, you 
    should remember that you can use the hierarchical cluster of size 20 to 
    compute the hierarchical clustering of size 19 and so on. Otherwise, you 
    will introduce an unnecessary factor of 15 into the computation of the 15 
    hierarchical clusterings.

    Once you have computed these distortions for both clustering methods, create 
    three separate plots (one for each data set) that compare the distortion of the 
    clusterings produced by both methods. Each plot should include two curves drawn 
    as line plots. The horizontal axis for each plot should indicate the number of 
    output clusters while the vertical axis should indicate the distortion 
    associated with each output clustering. For each plot, include a title that 
    indicates the data set used in creating the plots and a legend that 
    distinguishes the two curves.
    
    Takes a data set of either 3108, 896, 290, or 111 points
    '''
    
    xvals = xrange(20, 5, -1)
    kmeans_y = []
    hierarchical_y = []

    # load data by county
    data_urls = {3108:DATA_3108_URL, 896:DATA_896_URL, 290:DATA_290_URL, 111:DATA_111_URL}
    data_table = load_data_table(data_urls[data_set]) 
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    # compute k-means cluster distortion
    for num_clusters in xvals:
        print "Computing", num_clusters, "k-means clusters"
        kmeans = project3.kmeans_clustering(singleton_list, num_clusters, 5)
        kmeans_y.append(compute_distortion(kmeans, data_table))

    # compute hierarchical cluster distortion
    hierarchical = singleton_list
    for num_clusters in xvals:
        print "Computing", num_clusters, "hierarchical clusters"
        hierarchical = project3.hierarchical_clustering(hierarchical, num_clusters)
        hierarchical_y.append(compute_distortion(hierarchical, data_table))
    
    # plot results
    plt.plot(xvals, kmeans_y, color='r', label="K-Means Clustering")
    plt.plot(xvals, hierarchical_y, color='b', label="Hierarchical Clustering")
    plt.legend()
    plt.title("Distortion Comparison Between Clustering Methods on " + 
              str(data_set) + " County Data Set")
    plt.xlabel("Number of Output Clusters")
    plt.ylabel("Distortion")
    plt.show()
    
    return
    
    
    
#question_1()
#question_7()
#question_10(111)
#question_10(290)
#question_10(896)
#question_10(3108)