"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a 
    list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices 
    for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), 
            max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
    clusters cluster_list[idx1] and cluster_list[idx2] have minimum distance 
    dist.       
    """
    
    # initialize variables
    result = (float('inf'), -1, -1)
    
    # compare distance of each cluster to each other cluster
    for cluster_i in range(len(cluster_list)):
        for cluster_j in range(len(cluster_list)):
            if cluster_i != cluster_j:
                distance = pair_distance(cluster_list, cluster_i, cluster_j)
                if distance < result:
                    result = distance
                
    return result



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal 
    positions of their centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
    clusters cluster_list[idx1] and cluster_list[idx2] have minimum distance 
    dist.       
    """
    
    # skip fast_closest_pair algorithm if cluster_list is small
    full = len(cluster_list)
    if full <= 3:
        return slow_closest_pair(cluster_list)
    
    midpoint = int(full / 2)
    list1 = [cluster_list[idx] for idx in xrange(midpoint)]
    list2 = [cluster_list[idx] for idx in xrange(midpoint, full)]
    dist1 = fast_closest_pair(list1)
    dist2 = fast_closest_pair(list2)
    dist = min(dist1, (dist2[0], dist2[1] + midpoint, dist2[2] + midpoint))
    mid = (list1[-1].horiz_center() + list2[0].horiz_center()) / 2
    
    return min(dist, closest_pair_strip(cluster_list, mid, dist[0]))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal 
    distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
    clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and 
    have minimum distance dist.       
    """
    
    # a set of all points with horizontal distance from centerline less than w
    mid = [idx for idx in xrange(len(cluster_list)) 
           if abs(cluster_list[idx].horiz_center() 
                  - horiz_center) < half_width]
    
    # sort indices in ascending order of vertical coordinates
    mid.sort(key = lambda idx: cluster_list[idx].vert_center())
    num = len(mid)
    result = (float('inf'), -1, -1)
    for idx1 in xrange(num - 1):
        for idx2 in xrange(idx1 + 1, min(idx1 + 4, num)):
            distance = pair_distance(cluster_list, mid[idx1], mid[idx2])
            if distance < result:
                result = distance
    
    return (result[0], min(result[1], result[2]), max(result[1], result[2]))
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    clusters = len(cluster_list)
    while clusters > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        pair = fast_closest_pair(cluster_list)
        cluster_list[pair[1]].merge_clusters(cluster_list[pair[2]])
        cluster_list.pop(pair[2])
        clusters -= 1
    
    return cluster_list

######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of 
    iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    cluster_n = len(cluster_list)

    centers = sorted(cluster_list,
              key=lambda c: c.total_population())[-num_clusters:]
    centers = [c.copy() for c in centers]

    # initialize num_clusters number of empty sets
    for _ in xrange(num_iterations):
        cluster_result = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(num_clusters)]
        
        # put the node into closet center node
        for idx in xrange(cluster_n):
            min_num_clusters = 0
            min_dist_clusters = float('inf')
            for number_clusters in xrange(len(centers)):
                dist = cluster_list[idx].distance(centers[number_clusters])
                if dist < min_dist_clusters:
                    min_dist_clusters = dist
                    min_num_clusters = number_clusters

            cluster_result[min_num_clusters].merge_clusters(cluster_list[idx])

        # re-compute the center node
        for idx in xrange(len(centers)):
            centers[idx] = cluster_result[idx]

    return cluster_result


# Testing
#print slow_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), 
#                         alg_cluster.Cluster(set([]), 1, 1, 1, 0), 
#                         alg_cluster.Cluster(set([]), 3, 2, 1, 0)])

#print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), 
#                         alg_cluster.Cluster(set([]), 1, 1, 1, 0), 
#                         alg_cluster.Cluster(set([]), 3, 2, 1, 0)])

#print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), 
#                         alg_cluster.Cluster(set([]), 1, 0, 1, 0), 
#                         alg_cluster.Cluster(set([]), 2, 0, 1, 0), 
#                         alg_cluster.Cluster(set([]), 3, 0, 1, 0)])

