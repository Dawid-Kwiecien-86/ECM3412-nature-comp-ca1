import random

# runs 5 trials of the ACO algorithm with a different value of 'p' and 'e'
def run_trial(bpp, p, evap_rate):
    results = []

    # retrives the weights and num of bins for bin-packing problems 1 and 2
    if bpp == 1:
        weight_list, bins = get_bbp1_values()
    else:
        weight_list, bins = get_bbp2_values()

    # each trial is seeded with a set seed and the ACO algorithm is ran
    print(f"Starting Trials for Bin-Packing Problem {bpp}, where p={p} and e={evap_rate}")
    for trial in range(5):
        random.seed(trial)
        trial_best_fit = run_algo(weight_list, bins, p, evap_rate)
        results.append(trial_best_fit)
        print(f"Trial {trial+1} best fitness: {trial_best_fit}")

    # extra variables that I think are important are printed out along with the best fitness
    print("--------------------------")
    print(f"Average fitness: {sum(results)/len(results)}")
    print(f"Best overall fitness: {min(results)}")
    print(f"Fitness range: {max(results)-min(results)}")
    print()

# executes the entire ACO algorithm, as outlined in the CA description
def run_algo(weight_list, bins, ants, evap_rate):
    # we start by distributing pheromone values between 0 and 1 for every edge on the path
    items = len(weight_list)
    phero = distrib_phero(bins, items)
    eval_count = 0
    best_fit = 0

    # we evaluate the path fitness 10000 times before picking the optimal solution
    while eval_count < 10000:
        ant_paths = []
        ant_fitnesses = []

        # we pick the optimal path, initially based on the random pheromone distribution
        for ant in range(ants):
            path = get_ant_path(phero, bins)
            fitness = get_fitness(path, weight_list, bins)
            ant_paths.append(path)
            ant_fitnesses.append(fitness)
            eval_count+=1

        # we update the pheromone based on the path and its fitness
        for ant in range(ants):
            update_phero(phero, ant_paths[ant], ant_fitnesses[ant])

        evap_phero(phero, evap_rate) # some pheromone is evaporated, depending on the 'e' value
        best_fit = min(ant_fitnesses) # we pick the smallest fitness to find the optimal solution

    return best_fit

# distributes random amounts of pheromone for each 'edge' of the 2D graph
def distrib_phero(bins, items):
    phero = []

    for x in range(items):
        row = []
        for y in range(bins):
            row.append(random.random()) # double loop adds a rand value between 0 and 1 into every cell of the 2D list
        phero.append(row)

    return phero

# generates the path that the ant will followed, based on the number of pheromone on each edge
def get_ant_path(phero, bins):
    path = []

    for x in range(len(phero)):
        # we pick a random value between 0 and the total amount of pheromone for a given set of edges
        total_phero = sum(phero[x])
        rand_phero = random.random() * total_phero
        curr_total = 0

        # we add the phero value for each edge until it's greater than the random value, which we then pick as the next path edge
        for y in range(bins):
            curr_total += phero[x][y]
            if rand_phero < curr_total:
                path.append(y)
                break

    return path

# returns the fitness of a path, given a list of valid weights and bins
def get_fitness(path, weight_list, bins):
    bin_weights = []

    # set all bins to 0 initially (because all bins are empty at the start)
    for x in range(bins):
        bin_weights.append(0)

    # If the path picks that bin, it has weight added onto it
    for x in range(len(path)):
        curr_bin = path[x]
        bin_weights[curr_bin] += weight_list[x]

    # we return the difference between the smallest and biggest bin sizes like in the specification
    return (max(bin_weights) - min(bin_weights)) # fitness

# all edges have their pheromone updated based on how good their fitness is
def update_phero(phero, path, fitness):
    for x in range(len(path)):
        curr_bin = path[x]
        phero[x][curr_bin] += (100 / (fitness+1)) # higher fitness = more phero added to edge

# all edges have some pheromone evaporated based on 'e'
def evap_phero(phero, evap_rate):
    for x in range(len(phero)):
        for y in range(len(phero[x])):
            phero[x][y] *= (1-evap_rate) 

# helper method that initialises the weights and bins for the bbp1 problem in the specification
def get_bbp1_values():
    weight_list = []
    bins = 12

    for x in range(1, 601):
        weight = (2*x) + 1
        weight_list.append(weight)

    return weight_list, bins

# same as above but for bbp2
def get_bbp2_values():
    weight_list = []
    bins = 40

    for x in range(1, 401):
        weight = (x**2) / 4
        weight_list.append(weight)

    return weight_list, bins

# runs all of the trials as described in the CA specification
def run_spec_trial():
    # (x, y, z) = 'bpp', 'p' and 'e'
    run_trial(1, 50, 0.05)
    run_trial(1, 50, 0.30)
    run_trial(1, 10, 0.05)
    run_trial(1, 10, 0.30)

    # (x, y, z) = 'bpp', 'p' and 'e'
    run_trial(2, 50, 0.05)
    run_trial(2, 50, 0.30)
    run_trial(2, 10, 0.05)
    run_trial(2, 10, 0.30)

# extra trial using the example given in the coursework
def run_example_trial():
    weight_list = [17, 12, 19, 6, 4, 28]
    path = [0, 0, 1, 1, 1, 2]
    bins = 3
    print(get_fitness(path, weight_list, bins)) # should return '1' like in the 

def run_further_trials():
    # more trials for the 'further work' section
    run_trial(1, 5, 0.05)
    run_trial(1, 5, 0.3)
    run_trial(1, 10, 0.5)
    run_trial(1, 10, 0.7)

    run_trial(2, 5, 0.05)
    run_trial(2, 5, 0.3)
    run_trial(2, 10, 0.5)
    run_trial(2, 10, 0.7)

# runs all trials
def main():
    run_further_trials()

main()