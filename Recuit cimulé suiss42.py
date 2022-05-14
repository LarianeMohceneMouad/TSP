import time
import random
import math
fri26 = []
with open("suiss42.txt", 'r') as f:
    for line in f:
        liste = line.split()
        fri26.append(liste)

for i in range(len(fri26)):
    for j in range(len(fri26[0])):
        fri26[i][j] = int(fri26[i][j])


def cost_calculator(solution, s, distance_vec):
    cost = 0
    for _ in range(len(solution)-1):
        i = _+1
        if i > len(distance_vec)-1:
            i = s
        cost += distance_vec[solution[_]][solution[i]]
    return cost


def neighbor_generator(solution, s):
    neighbor = solution.copy()
    correct_values = False
    size = len(neighbor)-2
    while not correct_values:
        v1 = random.randint(1, size)
        v2 = random.randint(1, size)
        if v1 != v2 and v1 != s and v2 != s:
            correct_values = True
    index1 = neighbor.index(v1)
    index2 = neighbor.index(v2)
    # print(v1, index1)
    # print(v2, index2)
    neighbor[index1] = v2
    neighbor[index2] = v1
    return neighbor


def random_sol_generator(dv, s):
    for _ in range(10):
        solution = [s]
        while len(solution) < len(dv):
            i = random.randint(0, len(dv)-1)
            if (i not in solution) and (i != s):
                solution.append(i)
        solution.append(s)
    return solution


start = 0


def best_sol():
    solutions = []
    costs = []
    for _ in range(10000):
        sol = random_sol_generator(fri26, start)
        solutions.append(sol)
        costs.append(cost_calculator(sol, start, fri26))
    best_cost = min(costs)
    best_sol_index = costs.index(best_cost)
    best_random_sol = solutions[best_sol_index]
    return best_random_sol


start = 0
t_initial = 100
t_final = 0.0001
alpha = 0.9999
n = 1000000
i = 1
r = random.random()
h = True
if h:
    initial_sol = random_sol_generator(fri26, start)
    while t_initial > t_final and i < n:
        neighbhor_sol = neighbor_generator(initial_sol, start)
        print(f" initial sol : {initial_sol} cost {cost_calculator(initial_sol, start, fri26)} ")
        print(f" neighbor sol : {neighbhor_sol} cost {cost_calculator(neighbhor_sol, start, fri26)} ")
        delta = cost_calculator(neighbhor_sol, start, fri26) - cost_calculator(initial_sol, start, fri26)
        print("delta : ", delta)
        if delta < 0:
            print("neighbor better than initial")
            initial_sol = neighbhor_sol
        else:
            print(f"initial better than neighbor T-initial {t_initial}  delta {delta}  r : {r} value {math.exp((-delta/t_initial))}")
            r = random.random()
            if math.exp((-delta/t_initial)) > r:
                print("accepting bad neighbor")
                initial_sol = neighbhor_sol
        t_initial *= alpha
        i = i + 1
        print(f"finish: {i} with  temp {t_initial} sol {initial_sol} cost : {cost_calculator(initial_sol, start, fri26)} ")
