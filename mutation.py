import random


def bit_mutation(chromosome, mutation_factor):
    chromosome_length = len(chromosome) - 1
    for step in range(mutation_factor):
        random_gene = random.randint(0, chromosome_length)
        mutated_gene = '0' if chromosome[random_gene] else '1'
        chromosome = chromosome[:random_gene] + mutated_gene + chromosome[random_gene + 1:]
    return chromosome


def mutation_n_times_each_chromosome(offspring, mutation_rate, verbose=False):
    """Perform mutation on offspring individuals with a given mutation rate."""
    mutated_offspring = []
    for layout in offspring:
        mutated_layout = []
        for chromosome in layout:
            mutated_chromosome = bit_mutation(chromosome, int(mutation_rate * 10))
            mutated_layout.append(mutated_chromosome)
        mutated_offspring.append(mutated_layout)
    return mutated_offspring


def mutation_each_chromosome(offspring, mutation_rate, verbose=False):
    mutated_offspring = []
    mutation_counter = [0]

    for layout in offspring:
        mutated_layout = []
        for chromosome in layout:
            if random.random() < mutation_rate:
                random_gene = random.randint(0, len(chromosome)-1)
                mutated_gene = '0' if chromosome[random_gene] else '1'
                chromosome = chromosome[:random_gene] + mutated_gene + chromosome[random_gene + 1:]
                mutation_counter[-1] += 1
            mutated_layout.append(chromosome)
            mutation_counter.append(0)
        mutated_offspring.append(mutated_layout)

        if verbose:
            print('mutation_counter:', sum(mutation_counter)/(len(mutation_counter)-1))
    return mutated_offspring


def mutation_concatenated_layout(offspring, mutation_rate, verbose=False):
    """Perform mutation on offspring individuals with a given mutation rate."""
    mutation_counter = 0

    mutated_offspring_concatenated = []
    num_bits = len(offspring[0][0])
    offspring_concatenated = [''.join(layout) for layout in offspring]
    for layout in offspring_concatenated:
        mutated_layout = ''
        for gene in layout:
            if random.random() < mutation_rate:
                mutated_gene = '0' if gene == '1' else '1'
                mutation_counter += 1
            else:
                mutated_gene = gene
            mutated_layout += mutated_gene
        mutated_offspring_concatenated.append(mutated_layout)

    mutated_offspring = []
    for mutated_layout in mutated_offspring_concatenated:
        layout = []
        for i in range(len(offspring[0])):
            layout.append(mutated_layout[i:i+num_bits])
        mutated_offspring.append(layout)

    if verbose:
        print("mutation counter: ", mutation_counter)
    return mutated_offspring


def mutation(offspring, mutation_rate, verbose=False):
    return mutation_each_chromosome(offspring, mutation_rate, verbose)