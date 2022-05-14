import random
import math
import time

start = 0
percentage = 50
size = 1000


def reader(txt_file):
    cities_list = []
    with open(txt_file, 'r') as f:
        for line in f:
            list = line.split()
            cities_list.append(list)

    for i in range(len(cities_list)):
        n = 0
        for j in range(len(cities_list[0])):
            if n == 0:
                cities_list[i][j] = int(cities_list[i][j])
            else:
                cities_list[i][j] = float(cities_list[i][j])
            n += 1

    return cities_list


def distance_calculator(cord1, cord2):
    dist = math.sqrt((math.pow((cord2[1]-cord1[1]), 2) + math.pow((cord2[2]-cord1[2]), 2)))
    return int(dist)


berlin52 = reader("berlin52.txt")
distance_vec = []
for _ in range(len(berlin52)):
    tt = []
    for __ in range(len(berlin52)):
        tt.append(distance_calculator(berlin52[_], berlin52[__]))
    distance_vec.append(tt)


distance_vector = distance_vec
sol_lenght = len(distance_vector)


def random_sol_generator(dv, s):
    for _ in range(10):
        solution = [s]
        while len(solution) < len(dv):
            i = random.randint(0, len(dv)-1)
            if (i not in solution) and (i != s):
                solution.append(i)
        solution.append(s)
    return solution


def fitness_func(solution, s, distance_vec):
    cost = 0
    for _ in range(len(solution)-1):
        i = _+1
        if i > len(distance_vec)-1:
            i = s
        cost += distance_vec[solution[_]][solution[i]]
    return cost


def initial_population_generator(size):
    population = []
    for _ in range(size):
        sol = random_sol_generator(distance_vector, start)
        population.append(sol)
    return population


def sorting_func(ppl):
    costs = []
    selected_individuals = []
    for individual in ppl:
        costs.append(fitness_func(individual, start, distance_vector))
    sorted_costs = costs.copy()
    sorted_costs.sort()
    for fittest in sorted_costs:
        selected_individuals.append(ppl[costs.index(fittest)])
    return selected_individuals


def parents_selection_function(p, ppl):
    new_parents = []
    sorted_individuals = sorting_func(ppl)
    for _ in range(int((p*size)/100)):
        new_parents.append(sorted_individuals[_])
    return new_parents


initial_population = initial_population_generator(size)


def breeding(init_pop):
    chldrn = []
    selected_parents = parents_selection_function(percentage, init_pop)
    chldrn.append(selected_parents[0])
    chldrn.append(selected_parents[1])
    length = int(len(selected_parents[0]))
    while len(chldrn) < size:
        child1 = []
        child2 = []
        crossover_point = random.randint(1, length)
        parent1 = random.choice(selected_parents)
        parent2 = random.choice(selected_parents)
        while parent1 == parent2:
            parent2 = random.choice(selected_parents)
        for gene in range(crossover_point):
            child1.append(parent1[gene])
            child2.append(parent2[gene])
        for gene in range(crossover_point, length):
            child1.append(parent2[gene])
            child2.append((parent1[gene]))
        chldrn.append(child1)
        chldrn.append(child2)
    return chldrn


def children_adjusting_func(child):
    missing_genes = []
    duplicated_genes = []
    for gene in range(sol_lenght):
        if gene != start:
            occurence = child.count(gene)
            if occurence == 0:
                missing_genes.append(gene)
            elif occurence > 1:
                duplicated_genes.append([gene, occurence])
    while missing_genes:
        target = random.choice(duplicated_genes)
        target_value = target[0]
        target_index = child.index(target_value)
        occ = target[1]
        if occ > 1:
            child.remove(target_value)
            child.insert(target_index, missing_genes[0])
            duplicated_genes[duplicated_genes.index(target)][1] -= 1
            if duplicated_genes[duplicated_genes.index(target)][1] == 1:
                duplicated_genes.remove(target)
            missing_genes.remove(missing_genes[0])
    return child


def mutation_func(child):
    child_genes = child.copy()
    probability = random.randrange(0, 100)
    if probability > 50:
        changes = random.randint(1, 3)
        for change in range(changes):
            gene1 = random.choice(child_genes)
            while gene1 == 0:
                gene1 = random.choice(child_genes)
            gene1_index = child_genes.index(gene1)
            gene2 = random.choice(child_genes)
            while gene2 == 0 or gene2 == gene1:
                gene2 = random.choice(child_genes)
            gene2_index = child_genes.index(gene2)
            child_genes[gene1_index] = gene2
            child_genes[gene2_index] = gene1
    else:
        pass
        #print("mutating :  False")
    return child_genes


def genetic_algo(initial_population):
    parents = parents_selection_function(percentage, initial_population)
    children = breeding(parents)
    fixed_children = []
    for child in children:
        fixed_children.append(children_adjusting_func(child))
    mutated_generation = []
    for fixed_child in fixed_children:
        mutated = mutation_func(fixed_child)
        mutated_generation.append(mutated)
    return mutated_generation


def fittest_child(generation):
    fitness = []
    for child in generation:
        fitness.append(fitness_func(child, start, distance_vector))
    return min(fitness)


start_time = time.time()
new_generation = genetic_algo(initial_population)
value = fittest_child(new_generation)
conv = 0
convergence = False
convergence_red_flag = 50
while not convergence:
    new_generation = genetic_algo(new_generation)
    new_value = fittest_child(new_generation)
    gen = sorting_func(new_generation)
    print(f"best solution found {gen[0]} with cost {fitness_func(gen[0], start, distance_vector)}")
    if new_value >= value:
        conv += 1
    else:
        conv = 0
    if conv == convergence_red_flag:
        convergence = True
    value = new_value

end = time.time()
gen = sorting_func(new_generation)
print(f"best solution found {gen[0]} with cost {fitness_func(gen[0], start, distance_vector)}")
print(f"Runtime of the program is {end - start_time}")

