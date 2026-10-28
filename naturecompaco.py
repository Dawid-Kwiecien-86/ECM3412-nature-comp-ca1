import random

def run_trial(bbp, p, evap_rate):
    results = []

    if bbp == 1:
        weight_list, bins = get_bbp1_values()
    else:
        weight_list, bins = get_bbp2_values();

    for trial in range(5):
        random.seed(trial)
        trial_best_fit = run_algo(weight_list, bins, p, evap_rate)
        results.append(trial_best_fit)

    for result in results:
        print("Trial ", trial+1, " best fitness: ", result)

def run_algo(weight_list, bins, ants, evap_rate):
    items = len(weight_list)
    phero = distrib_phero(items, bins)
    eval_count = 0
    best_fit = 0

    while eval_count < 10000:
        ant_paths = []
        ant_fitnesses = []

        for ant in range(ants):
            path = get_ant_path(phero, bins)
            fitness = get_fitness(path, weight_list, bins)
            ant_paths.append(path)
            ant_fitnesses.append(fitness)
            eval_count+=1

        for ant in range(ants):
            update_phero(phero, ant_paths[ant], ant_fitnesses[ant])

        evap_phero(phero, evap_rate)
        best_fit = min(ant_fitnesses)

    return best_fit

def distrib_phero(bins, items):
    phero = []

    for x in range(items):
        row = []

        for y in range(bins):
            row.append(random.random())

        phero.append(row)

    return phero

def get_ant_path(phero, bins):
    path = []

    for x in range(len(phero)):
        total_phero = sum(phero[x])
        rand_phero = random.random() * total_phero
        curr_total = 0

        for y in range(bins):
            curr_total += phero[x][y]

            if rand_phero < curr_total:
                path.append(x)
                break

    return path

def get_fitness(path, weight_list, bins):
    bin_weights = []

    for x in range(bins):
        bin_weights.append(0)

    for x in range(len(path)):
        curr_bin = path[x]
        bin_weights[curr_bin] += weight_list[x]

    return (max(bin_weights) - min(bin_weights)) # fitness

def update_phero(phero, path, fitness):
    for x in range(len(path)):
        curr_bin = path[x]
        phero[x][curr_bin] += (100 / (fitness+1))

def evap_phero(phero, evap_rate):
    for x in range(len(phero)):
        for y in range(len(phero[x])):
            phero[x][y] *= (1-evap_rate)

def get_bbp1_values():
    weight_list = []
    bins = 12

    for x in range(1, 601):
        weight = (2*x) + 1
        weight_list.append(weight)

    return weight_list, bins

def get_bbp2_values():
    weight_list = []
    bins = 40

    for x in range(1, 401):
        weight = (x**2) / 4
        weight_list.append(weight)

    return weight_list, bins

def main():
    # p=50, e=0.05 
    run_trial(1, 50, 0.05)
    run_trial(2, 50, 0.05)

    # p=50, e=0.30 
    run_trial(1, 50, 0.30)
    run_trial(2, 50, 0.30)

    # p=10, e=0.05 
    run_trial(1, 10, 0.05)
    run_trial(2, 10, 0.05)

    # p=10, e=0.30 
    run_trial(1, 10, 0.30)
    run_trial(2, 10, 0.30)

main()