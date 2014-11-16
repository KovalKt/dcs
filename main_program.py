#coding:utf-8
import sys
from math import log, sqrt
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

def fill_adjacency_matrix_for_cluster_star(cluster_number, adj_matrix, iter_number=None):
    n_sufix = cluster_number*5
    for n in range(5):
        if n != 0:
            adj_matrix[n+n_sufix][0+n_sufix] = adj_matrix[0+n_sufix][n+n_sufix] = 1
    if cluster_number != 0:
        if cluster_number % 2 == 0: 
            dist_indx = (cluster_number-1)/2*5+4
            adj_matrix[1+n_sufix][dist_indx] = adj_matrix[dist_indx][1+n_sufix] = 1
        else:
            dist_indx = (cluster_number)/2*5+3
            adj_matrix[2+n_sufix][dist_indx] = adj_matrix[dist_indx][2+n_sufix] = 1
            adj_matrix[0+n_sufix][5+n_sufix] = adj_matrix[5+n_sufix][0+n_sufix] = 1
        
        row = int(log(cluster_number+1, 2))
        if cluster_number == (pow(2,row)-1):
            dist_indx = (pow(2,row+1)-2)*5
            adj_matrix[0+n_sufix][dist_indx] = adj_matrix[dist_indx][0+n_sufix] = 1 

def fill_adjacency_matrix_for_cluster_romb(cluster_number, adj_matrix, N=None):
    max_cluster_number = N/8
    n_sufix = cluster_number*8
    d = int(sqrt(max_cluster_number))
    for n in range(4):
        adj_matrix[n+n_sufix][(n+1)%4+n_sufix] = adj_matrix[(n+1)%4+n_sufix][n+n_sufix] = 1
        adj_matrix[n+n_sufix][n+n_sufix+4] = adj_matrix[n+n_sufix+4][n+n_sufix] = 1
        if n == 3:
            adj_matrix[n+n_sufix][4+n_sufix] = adj_matrix[4+n_sufix][n+n_sufix] = 1
        else:
            adj_matrix[n+n_sufix][n+n_sufix+5] = adj_matrix[n+n_sufix+5][n+n_sufix] = 1
    for n in [4, 5]:
        adj_matrix[n+n_sufix][n+n_sufix+2] = adj_matrix[n+n_sufix+2][n+n_sufix] = 1
    #intercluster connection
    for n in range(4):
        if n == 2 and (cluster_number+1) % (iter_number+1) != 0:
            adj_matrix[n+n_sufix][n+(cluster_number+1)*8-2] = 1
            adj_matrix[n+(cluster_number+1)*8-2][n+n_sufix] = 1
        if n == 1 and cluster_number not in range(d):
            dist_indx = (n+2) + (cluster_number-d)*8
            adj_matrix[n+n_sufix][dist_indx] = adj_matrix[dist_indx][n+n_sufix] = 1
    if (cluster_number+1) % (iter_number+1) != 0: #not rightest
        if cluster_number not in range(d): 
            dist_indx = 4+(cluster_number-d+1)*8
            adj_matrix[6+n_sufix][dist_indx] = adj_matrix[dist_indx][6+n_sufix] = 1
        if cluster_number not in range(max_cluster_number-d,max_cluster_number):
            dist_indx = 5+(cluster_number+d+1)*8
            adj_matrix[7+n_sufix][dist_indx] = adj_matrix[dist_indx][7+n_sufix] = 1


def calc_power(adj_matrix):
    return max(map(sum, adj_matrix))

def calc_diametr(dest_matrix):
    return max(map(max, dest_matrix))

def calc_average_diametr(dest_matrix):
    n = len(dest_matrix)
    return float(sum(map(sum, dest_matrix)))/(n*(n-1))

if __name__ == "__main__":

    input_data = {
        'ring': (9, fill_adjacency_matrix_for_cluster_mash),
        'tree': (5, fill_adjacency_matrix_for_cluster_star),
        'grid': (8, fill_adjacency_matrix_for_cluster_romb)
    }
    topology_type = sys.argv[1]
    iter_number = 0
    N,  cluster_fill_func = input_data[topology_type]

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
    while N <= 900:
        if topology_type == 'ring':
            max_cluster_number = iter_number+1
        elif topology_type == 'tree':
            max_cluster_number = N/5
        else:
            max_cluster_number = N/8
        adj_matrix = [[0 for x in range(N)] for x in range(N)]
        for i in range(max_cluster_number):
            top_kwargs = {}
            if topology_type == 'ring':
                top_kwargs['N'] = N
            elif topology_type == 'tree':
                top_kwargs['iter_number'] = iter_number
            else:
                top_kwargs['N'] = N

            cluster_fill_func(i,adj_matrix, **top_kwargs)
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
        if topology_type == 'ring':
            N = (iter_number+1)*9
        elif topology_type == 'tree':
            N+= pow(2, (iter_number))*5
        elif topology_type == 'grid':
            N = ((iter_number+1)*(iter_number+1))*8
