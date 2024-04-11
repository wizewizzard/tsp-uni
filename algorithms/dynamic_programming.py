from sys import maxsize
from itertools import permutations

class TravellingSalesmanProblem:
    def __init__(self, distance, start):
        self.distance_matrix = distance
        self.start_city = start
        self.total_cities = len(distance)

        self.end_state = (1 << self.total_cities) - 1
        self.memo = [[None for _col in range(1 << self.total_cities)] for _row in range(self.total_cities)]

        self.shortest_path = []
        self.min_path_cost = float('inf')

    def solve(self):
        self.__initialize_memo()

        for num_element in range(3, self.total_cities + 1):

            for subset in self.__initiate_combination(num_element):

                if self.__is_not_in_subset(self.start_city, subset):
                    continue

                for next_city in range(self.total_cities):

                    if next_city == self.start_city or self.__is_not_in_subset(next_city, subset):
                        continue

                    subset_without_next_city = subset ^ (1 << next_city)
                    min_distance = float('inf')

                    for last_city in range(self.total_cities):

                        if last_city == self.start_city or \
                                last_city == next_city or \
                                self.__is_not_in_subset(last_city, subset):
                            continue

                        new_distance = \
                            self.memo[last_city][subset_without_next_city] + self.distance_matrix[last_city][next_city]

                        if new_distance < min_distance:
                            min_distance = new_distance

                    self.memo[next_city][subset] = min_distance

        # self.__calculate_min_cost()
        self.__find_shortest_path()
        self.shortest_path = self.shortest_path + [0, ]
        prev = None
        cost = 0
        for n in self.shortest_path:
            if prev != None:
                cost += self.distance_matrix[prev][n]
            prev = n
        self.min_path_cost = cost

    def __find_shortest_path(self):
        state = self.end_state

        for i in range(1, self.total_cities):
            best_index = -1
            best_distance = float('inf')

            for j in range(self.total_cities):

                if j == self.start_city or self.__is_not_in_subset(j, state):
                    continue

                new_distance = self.memo[j][state]

                if new_distance <= best_distance:
                    best_index = j
                    best_distance = new_distance

            self.shortest_path.append(best_index)
            state = state ^ (1 << best_index)

        self.shortest_path.append(self.start_city)
        self.shortest_path.reverse()

    def __initialize_memo(self):
        for destination_city in range(self.total_cities):

            if destination_city == self.start_city:
                continue

            self.memo[destination_city][1 << self.start_city | 1 << destination_city] = \
                self.distance_matrix[self.start_city][destination_city]

    def __initiate_combination(self, num_element):
        subset_list = []
        self.__initialize_combination(0, 0, num_element, self.total_cities, subset_list)
        return subset_list

    def __initialize_combination(self, subset, at, num_element, total_cities, subset_list):

        elements_left_to_pick = total_cities - at
        if elements_left_to_pick < num_element:
            return

        if num_element == 0:
            subset_list.append(subset)
        else:
            for i in range(at, total_cities):
                subset |= 1 << i
                self.__initialize_combination(subset, i + 1, num_element - 1, total_cities, subset_list)
                subset &= ~(1 << i)

    @staticmethod
    def __is_not_in_subset(element, subset):
        return ((1 << element) & subset) == 0

MAX = 999999

def tsp(mask, pos, graph, dp,n, visited):
	if mask == visited:
		return graph[pos][0]
	if dp[mask][pos] != -1:
		return dp[mask][pos]
	
	ans = MAX 
	for city in range(0, n):
		if ((mask & (1 << city)) == 0):
            tsp(mask|(1<<city),city, graph, dp, n, visited)
			new = graph[pos][city] + tsp(mask|(1<<city),city, graph, dp, n, visited)
			ans = min(ans, new)
	
	dp[mask][pos]=ans
	return [], dp[mask][pos]

class DynamicProgramming:
    def tsp(self, matrix, start = 0):
        n = len(matrix)
        visited = (1 << n) - 1
        r,c=16,len(matrix)
        dp=[[-1 for j in range(c)]for i in range(r)]
        for i in range(0, (1<<n)):
            for j in range(0, n):
                dp[i][j] = -1

        return tsp(1, 0, matrix, dp, n, visited)


dp_algorithm = DynamicProgramming()
matrix = [
    [0, 2.5, 0.3], 
    [2.5, 0, 4], 
    [0.3, 4, 0]
]
route, dist = dp_algorithm.tsp(matrix)
print(dist)
print(route)

assert dist == 6.8, "Should be 6.8"

matrix = [
    [0, 2, 1, 2], 
    [2, 0, 4, 2], 
    [1, 4, 0, 3],
    [2, 2, 3, 0]
]
route, dist = dp_algorithm.tsp(matrix)
print(route)
assert dist == 8, "Should be 8"

matrix = [
    [0, 1, 1, 1], 
    [1, 0, 1, 1], 
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
route, dist = dp_algorithm.tsp(matrix)
print(route)
assert dist == 4, "Should be 4"

distance_matrix = [
        [0, 328, 259, 180, 314, 294, 269, 391],
        [328, 0, 83, 279, 107, 131, 208, 136],
        [259, 83, 0, 257, 70, 86, 172, 152],
        [180, 279, 257, 0, 190, 169, 157, 273],
        [314, 107, 70, 190, 0, 25, 108, 182],
        [294, 131, 86, 169, 25, 0, 84, 158],
        [269, 208, 172, 157, 108, 84, 0, 140],
        [391, 136, 152, 273, 182, 158, 140, 0],
]

print(dp_algorithm.tsp(distance_matrix))
assert dp_algorithm.tsp(distance_matrix)[1] == 1072