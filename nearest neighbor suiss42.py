import random
suiss42 = []
with open("suiss42.txt", 'r') as f:
    for line in f:
        list = line.split()
        suiss42.append(list)

for i in range(len(suiss42)):
    for j in range(len(suiss42[0])):
        suiss42[i][j] = int(suiss42[i][j])
for _ in suiss42:
    print(_)


def minimum_funct(t):
    eq_zero = True
    i = 0
    while eq_zero:
        minimum = random.choice(t)
        if minimum != 0:
            eq_zero = False
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
    return ("path: ",visited_cities," cost: ", p)


start = 0
print(path_finder(suiss42, start))







