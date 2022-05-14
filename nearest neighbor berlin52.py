import math
import random
berlin52 = []
with open("berlin52.txt", 'r') as f:
    for line in f:
        list = line.split()
        berlin52.append(list)

for i in range(len(berlin52)):
    n = 0
    for j in range(len(berlin52[0])):
        if n == 0:
            berlin52[i][j] = int(berlin52[i][j])
        else:
            berlin52[i][j] = float(berlin52[i][j])
        n += 1


def distance_calculator(cord1, cord2):
    dist = math.sqrt((math.pow((cord2[1]-cord1[1]), 2) + math.pow((cord2[2]-cord1[2]), 2)))
    return round(dist, 4)


distance_vec = []
for _ in range(len(berlin52)):
    tt = []
    for __ in range(len(berlin52)):
        tt.append(distance_calculator(berlin52[_], berlin52[__]))
    distance_vec.append(tt)

for _ in distance_vec:
    print(_)


def minimum_funct(t):
    eq_zero = True
    while eq_zero:
        minimum = random.choice(t)
        if minimum != 0:
            eq_zero = False

    i = 0
    for _ in t:

        if (_ > 0) and (_ <= minimum):
            minimum = _
            v = i
        i += 1
    return minimum, v


def path_finder(tab, start):
    s = start
    p = 0
    visited_cities = [start]
    cities_num = len(tab)
    for _ in range(1, cities_num):
        visited = True
        print("trip number: ", _)
        cord = []
        cord = minimum_funct(tab[s])
        minimum = cord[0]
        visited_city = cord[1]
        print("outside", minimum, visited_city)
        while visited:
            if visited_city not in visited_cities:
                visited = False
            else:
                tab[s][visited_city] = 0
                cord = []
                cord = minimum_funct(tab[s])
                minimum = cord[0]
                visited_city = cord[1]
                print("inside",minimum,visited_city)
        print("path cost: ",minimum)
        p += minimum
        print("total cost:", p)
        s = visited_city
        print("next city chosen: ", s)
        visited_cities.append(visited_city)
        print("cities visited: ", visited_cities)

    visited_cities.append(start)
    p += tab[visited_city][start]

    return ("path: ", visited_cities," cost: ", p)


start = 0
print(path_finder(distance_vec, 0))
