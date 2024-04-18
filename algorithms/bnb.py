import math
import threading
import time

maxsize = float('inf')


class BnB(threading.Thread):
    def __init__(self, matrix):
        threading.Thread.__init__(self)
        self.final_path = []
        self.curr_path = []
        self.N = len(matrix)
        self.curr_res = maxsize
        self.final_res = maxsize
        self.matrix = matrix
        self.stopped = True

    def copyToFinal(self, curr_path):
        self.final_path[:self.N + 1] = curr_path[:]
        self.final_path[self.N] = curr_path[0]

    # Function to find the minimum edge cost
    # having an end at the vertex i
    def firstMin(self, adj, i):
        min = maxsize
        for k in range(self.N):
            if adj[i][k] < min and i != k:
                min = adj[i][k]

        return min

    # function to find the second minimum edge
    # cost having an end at the vertex i
    def secondMin(self, adj, i):
        first, second = maxsize, maxsize
        for j in range(self.N):
            if i == j:
                continue
            if adj[i][j] <= first:
                second = first
                first = adj[i][j]

            elif (adj[i][j] <= second and
                  adj[i][j] != first):
                second = adj[i][j]

        return second

    # function that takes as arguments:
    # curr_bound -> lower bound of the root node
    # curr_weight-> stores the weight of the path so far
    # level-> current level while moving
    # in the search space tree
    # self.curr_path[] -> where the solution is being stored
    # which would later be copied to self.final_path[]
    def TSPRec(self, adj, curr_bound, curr_weight, level, visited):
        if self.stopped:
            return

        # base case is when we have reached level self.N
        # which means we have covered all the nodes once
        if level == self.N:

            # check if there is an edge from
            # last vertex in path back to the first vertex
            if adj[self.curr_path[level - 1]][self.curr_path[0]] != 0:

                self.curr_res = curr_weight + adj[self.curr_path[level - 1]] \
                    [self.curr_path[0]]
                if self.curr_res < self.final_res:
                    self.copyToFinal(self.curr_path)
                    self.final_res = self.curr_res
            return

        # for any other level iterate for all vertices
        # to build the search space tree recursively
        for i in range(self.N):

            # Consider next vertex if it is not same
            # (diagonal entry in adjacency matrix and
            #  not visited already)
            if (adj[self.curr_path[level - 1]][i] != 0 and
                    visited[i] == False):
                temp = curr_bound
                curr_weight += adj[self.curr_path[level - 1]][i]

                # different computation of curr_bound
                # for level 2 from the other levels
                if level == 1:
                    curr_bound -= ((self.firstMin(adj, self.curr_path[level - 1]) +
                                    self.firstMin(adj, i)) / 2)
                else:
                    curr_bound -= ((self.secondMin(adj, self.curr_path[level - 1]) +
                                    self.firstMin(adj, i)) / 2)

                # curr_bound + curr_weight is the actual lower bound
                # for the node that we have arrived on.
                # If current lower bound < self.final_res,
                # we need to explore the node further
                if curr_bound + curr_weight < self.final_res:
                    self.curr_path[level] = i
                    visited[i] = True

                    # call TSPRec for the next level
                    self.TSPRec(adj, curr_bound, curr_weight,
                                level + 1, visited)

                # Else we have to prune the node by resetting
                # all changes to curr_weight and curr_bound
                curr_weight -= adj[self.curr_path[level - 1]][i]
                curr_bound = temp

                # Also reset the visited array
                visited = [False] * len(visited)
                for j in range(level):
                    if self.curr_path[j] != -1:
                        visited[self.curr_path[j]] = True

    def run(self):
        self.stopped = False
        adj = [[0] * self.N for _ in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                adj[i][j] = self.matrix[i][j]
        curr_bound = 0
        self.curr_path = [-1] * (self.N + 1)
        visited = [False] * self.N

        # Compute initial bound
        for i in range(self.N):
            curr_bound += (self.firstMin(adj, i) +
                           self.secondMin(adj, i))

        # Rounding off the lower bound to an integer
        curr_bound = math.ceil(curr_bound / 2)

        # We start at vertex 1 so the first vertex
        # in self.curr_path[] is 0
        visited[0] = True
        self.curr_path[0] = 0

        # Call to TSPRec for curr_weight
        # equal to 0 and level 1
        self.TSPRec(adj, curr_bound, 0, 1, visited)
        print("Bnb thread stopped")
        # time.sleep(100)
