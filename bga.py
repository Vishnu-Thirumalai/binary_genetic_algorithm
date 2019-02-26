"""
Chromosomes : Intial
Ranked: Chromosomes sorted by weight + costs
Selected: Top n_keep chromosomes + costs
Parents: Binary strings of selected chromosomes
Costs: Normalised costs of chromosomes
Probs: Cumulative probabilities for chromosomes
Pairs: Pairs of parents
chromosomes: Newly generated chromosomes
"""
import random
import math


def cost(chromosome):
  x = chromosome[0]
  y = chromosome[1] 
  return (-10*x**2 + 7*x*y - 7 * y**2 - 4)  #Cost Function

def generate_inital_chromosomes(length, max, min, pop_size):
  """
  Generates pop_size sequences of integers between min and max, each of given length.
  """
  return [ [ int(random.uniform(min,max)) for j in range(length)] for i in range(pop_size)]

def rank_chromosomes(cost, chromosomes):
  """
  Sorted the given chromosomes ascending according to the given function. Returns the sorted chromosomes and their respective function values.
  """
  costs = list(map(cost, chromosomes))
  ranked  = sorted( list(zip(chromosomes,costs)), key = lambda c:c[1])
  return list(zip(*ranked))

def natural_selection(chromosomes, n_keep):
  """
  Splits the given chromosomes into lists of sized n_keep, len(chromosomes)-n_keep and returns both
  """
  return chromosomes[:n_keep], chromosomes[n_keep:] 

def weight_pairing(chromosomes, costs, normal):
  """
  Given a list of chromosomes and their assosciated costs, pairs them using random weighted pairing.
  """
  costs = list(map(lambda c:c-normal, costs))
  total = sum(costs)

  probs = []
  run_sum = 0
  for i in range(len(chromosomes)):
    run_sum += costs[i]/total
    probs.append(run_sum)

  pairs = []
  for i in range(len(chromosomes)):
    r = random.random()
    for k in range(len(probs)):
      if r < probs[k]:
        pairs.append(chromosomes[k])
        break 
  
  pairs = [pairs[i:i+2] for i in range(0,len(pairs),2)]
  return pairs

def bin_encode(chromosome, bin_val, min_val, precision):
  """
  Encodes the given list of numbers as a binary string, using the given precision.

  bin_val = (max_val - min_val) / (2**precision-1)
  """
  ret = ""
  for g in chromosome:
    val = round( (g - min_val)/bin_val )  
    ret+= bin(val)[2:].rjust(precision,'0')
  return ret

def bin_encode_chromosomes(chromosomes, precision, max_val, min_val):
  """
  Encodes the given chromosomes to binary strings, using the given values.
  """
  bin_val = (max_val - min_val) / (2**precision-1) #Range of numbers

  bin_chromosomes = [ bin_encode(c, bin_val, min_val, precision) for c in chromosomes]
  return bin_chromosomes

def bin_decode(chromosome, bin_val, min_val, precision):
  """
  Decodes the given binary string to a list of numbers, using the given precision.

  bin_val = (max_val - min_val) / (2**precision-1)
  """
  ret = []
  for idx in range(0,len(chromosome), precision):
    g = int(chromosome[idx:idx+precision], 2)
    ret.append(round(g*bin_val)+min_val)
  return ret

def bin_decode_chromosomes(chromosomes, precision, max_val, min_val):
  """
  Decodes the given binary chromosomes to real numbers, using the given values.
  
  """

  bin_val = (max_val - min_val) / (2**precision-1) #Range of numbers

  bin_chromosomes = [ bin_decode(c, bin_val, min_val, precision) for c in chromosomes]
  return bin_chromosomes

def one_point_crossover(pairs):
  """
  Generates offspring using the given pairs via one point crossovers. The point for each crossover is determined randomly.
  """

  length = len(pairs[0]) -1

  children = []
  for (a,b) in pairs:
    split = int(random.random()*length)
    children.append(a[:split] + b[split:])
    children.append(b[:split] + a[split:])

  return children  

def mutate(chromosomes, mutation_val):
  """
  Mutates 'mutation_val' bits in the given chromosomes
  """

  size = len(chromosomes[0])
  mut_bits = random.sample(range (0,len(chromosomes)*size), mutation_val)


  for bit in mut_bits: #To highlight bits, c is chromsome number, pos is index in chromsome
    pos = math.floor(bit % size)
    c = math.floor(bit / size)
    b = chromosomes[c]
    chromosomes[c] = b[:pos] + ('1' if b[pos]=='0' else '0') + b[pos+1:]

  return chromosomes  



def main(cost_func, max_val = 100, min_val = -100, chromosome_length = 2, precision = 5, population_size = 10,  n_keep = 4, mutation_rate = 0.25, mutation_bits = 3):
  """
  Given cost_func, returns a minimized solution. This solution is not guaranteed to be optimal.

  cost_func: function to be optimised. Return type must be comparable, and must accept a list of integers with len=chromosome_length (2 by default)
  max_val: maximum value permitted in the solution
  min_val: minimum value permitted in the solution
  chromosome_length: number of variables to be optimised
  precision: decimal precision for each variable

  population_size: number of chromosomes in the inital population. May change throughout the run of the algorithm
  n_keep: If using Xrate selection, the number of chromosomes that are selected for mating. Must be > 0.

  mutation_rate = %chance that an individual bit is mutated. Must be > 0
  mutation_bits = number of genes in a chromosome that are up for mutation  
  """
  chromosomes = generate_inital_chromosomes(chromosome_length, max_val, min_val, population_size)
  mutation = math.floor(mutation_rate * population_size * mutation_bits)

  x = 0
  while x < 5:
    
    ranked, costs = rank_chromosomes(cost_func, chromosomes)  
    if costs[n_keep] == costs[0]:
      break
    parents, discarded = natural_selection(ranked, n_keep)

    parents = bin_encode_chromosomes(parents, precision, max_val, min_val)

    
    pairs = weight_pairing(parents, costs[:len(parents)], costs[n_keep])
    children = one_point_crossover(pairs)
    chromosomes = parents + children

    if len(chromosomes)!= population_size:
        population_size = len(chromosomes)      
        mutation = math.floor(mutation_rate * population_size * mutation_bits)

    chromosomes = mutate(chromosomes, mutation)

    chromosomes = bin_decode_chromosomes(chromosomes, precision, max_val, min_val)

  return chromosomes[0]

val = main(cost)
print(val)








