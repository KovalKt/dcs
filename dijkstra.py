#coding:utf-8

def dijkstra(adj_matrix):
    N = len(adj_matrix)
    dest_matrix = [[-1 for x in range(N)] for x in range(N)]

    for n in range(N):
        dist = [10**10 for x in range(N)]
        dist[n] = 0
        unvisit_nodes = range(N)
        
        while unvisit_nodes:
            unvis_dist = filter(lambda x: x[0] in unvisit_nodes, enumerate(dist))
            min_d_node, min_dist = min(unvis_dist, key=lambda x: x[1])
            unvisit_nodes.remove(min_d_node)
            for indx, weight in enumerate(adj_matrix[min_d_node]):
                alt_dist = 10**10
                if weight:
                    alt_dist = dist[min_d_node]+adj_matrix[min_d_node][indx]
                if alt_dist < dist[indx]:
                    dist[indx] = alt_dist
        dest_matrix[n] = dist
    return dest_matrix
