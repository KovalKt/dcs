#coding:utf-8

from math import log
from dijkstra import dijkstra


def fill_adjacency_matrix_for_cluster_mash(cluster_number, adj_matrix, N):
    n_sufix = cluster_number*9
    for n in range(9):
        adj_matrix[n+n_sufix][(n+3)%9+n_sufix] = adj_matrix[(n+3)%9+n_sufix][n+n_sufix] = 1
        if n not in [2,5,8]:
            adj_matrix[n+n_sufix][n+1+n_sufix] = adj_matrix[n+1+n_sufix][n+n_sufix] = 1
        else: 
            adj_matrix[n+n_sufix][((n-2)+9+n_sufix)%N] = adj_matrix[((n-2)+9+n_sufix)%N][n+n_sufix] = 1
        if (cluster_number+1) % 2 == 0 and n in [0, 1, 2]:
            adj_matrix[n+n_sufix][n+(cluster_number/2*9)+6] = adj_matrix[n+(cluster_number/2*9)+6][n+n_sufix] = 1


def calc_power(adj_matrix):
    return max(map(sum, adj_matrix))

def calc_diametr(dest_matrix):
    return max(map(max, dest_matrix))

def calc_average_diametr(dest_matrix):
    n = len(dest_matrix)
    return float(sum(map(sum, dest_matrix)))/(n*(n-1))

if __name__ == "__main__":
    iter_number = 0
    N = 0
    s = []
    d = []
    av_d = []
    ds = []
    t = []
 
    print "-"*91
    print " | ".join([
        'Iter. number',
        'Nodes number',
        'D'.rjust(6),
        'S'.rjust(6),
        'DS'.rjust(6),
        'avD'.rjust(10),
        'T'.rjust(10),
         'Cost'.rjust(6)
    ])
    print "-"*91
    while N <= 200:
        N = (iter_number+1)*9
        adj_matrix = [[0 for x in range(N)] for x in range(N)]
        for i in range(iter_number+1):
            fill_adjacency_matrix_for_cluster_mash(i,adj_matrix, N)
        dest_matrix = dijkstra(adj_matrix)

        s.append(calc_power(adj_matrix))
        d.append(calc_diametr(dest_matrix))
        ds.append(d[-1]*s[-1])
        av_d.append(calc_average_diametr(dest_matrix))
        t.append(2*av_d[-1]/s[-1])
        
        print " | ".join([
            str(iter_number).rjust(12), 
            str(N).rjust(12),
            str(d[-1]).rjust(6), 
            str(s[-1]).rjust(6), 
            str(ds[-1]).rjust(6),
            ('%.5f'%(av_d[-1])).rjust(10), 
            ('%.5f'%(t[-1])).rjust(10),
            str(N*d[-1]*s[-1]).rjust(6)
        ])
        iter_number += 1
