
# N - numner of nodes

# distination_matrix = []

def fill_adjacency_matrix_for_cluster(cluster_number, adj_matrix, N):
    n_sufix = cluster_number*9

    for n in range(9):
        adj_matrix[n+n_sufix][(n+3)%9+n_sufix] = adj_matrix[(n+3)%9+n_sufix][n+n_sufix] = 1
        if n not in [2,5,8]:
            adj_matrix[n+n_sufix][n+1+n_sufix] = adj_matrix[n+1+n_sufix][n+n_sufix] = 1
        else: 
            adj_matrix[n+n_sufix][((n-2)+9+n_sufix)%N] = adj_matrix[((n-2)+9+n_sufix)%N][n+n_sufix] = 1


if __name__ == "__main__":
    iter_number = N = 0

    while N <= 100:
        N = iter_number*9
        adj_matrix = [[0 for x in range(N)] for x in range(N)]
        for i in range(iter_number):
            fill_adjacency_matrix_for_cluster(i,adj_matrix, N)
        iter_number += 1
