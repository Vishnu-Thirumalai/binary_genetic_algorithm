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

def generate_inital_chromosomes(length, max, min, num = 8):
  return [ [ int(random.uniform(min,max)) for j in range(length)] for i in range(num)]

def rank_chromosomes(cost, chromosomes):
  costs = list(map(cost, chromosomes))
  ranked  = sorted( list(zip(chromosomes,costs)), key = lambda c:c[1])
  chromosomes = list(map(lambda x:x[0], ranked))
  return chromosomes, costs

def natural_selection(ranked, n_keep):
  return ranked[:n_keep], ranked[n_keep:] 

def weight_pairing(chromosomes, costs, normal):
  """
  Accepts chromosomes with costs, returns pairs of chromosomes without costs
  """
  costs = costs[:len(chromosomes)]
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
  ret = ""
  for g in chromosome:
    val = round( (g - min_val)/bin_val )  
    ret+= bin(val)[2:].rjust(precision,'0')
  return ret

def bin_encode_chromosomes(chromosomes, precision, max_val, min_val):
  bin_val = (max_val - min_val) / (2**precision-1) #Range of numbers

  bin_chromosomes = [ bin_encode(c, bin_val, min_val, precision) for c in chromosomes]
  return bin_chromosomes

def bin_decode(chromosome, bin_val, min_val, precision):
  ret = []
  for idx in range(0,len(chromosome), precision):
    g = int(chromosome[idx:idx+precision], 2)
    ret.append(round(g*bin_val)+min_val)
  return ret

def bin_encode_chromosomes(chromosomes, precision, max_val, min_val):
  bin_val = (max_val - min_val) / (2**precision-1) #Range of numbers

  bin_chromosomes = [ bin_encode(c, bin_val, min_val, precision) for c in chromosomes]
  return bin_chromosomes

def one_point_crossover(pairs):
  length = len(pairs[0]) -1

  children = []
  for (a,b) in pairs:
    split = int(random.random()*length)
    children.append(a[:split] + b[split:])
    children.append(b[:split] + a[split:])

  return children  

def mutate(chromosomes, mutation_val):
  size = len(chromosomes[0])
  mut_bits = random.sample(range (0,len(chromosomes)*size), mutation_val)


  for bit in mut_bits: #To highlight bits, c is chromsome number, pos is index in chromsome
    pos = math.floor(bit % size)
    c = math.floor(bit / size)
    b = chromosomes[c]
    chromosomes[c] = b[:pos] + ('1' if b[pos]=='0' else '0') + b[pos+1:]

  return chromosomes  



def main(cost_func, chromosome_length, max_val, min_val, **options):
  chromosomes = generate_inital_chromosomes(chromosome_length, max_val, min_val)

  precision = 5
  n_keep = 4
  mutation_rate = 0.25
  n_bits = 3
  mutation = math.floor(mutation_rate * len(chromosomes) * n_bits)


  ranked, costs = rank_chromosomes(cost_func, chromosomes)  
  parents, discarded = natural_selection(ranked, n_keep)
  
  parents = bin_encode_chromosomes(parents, precision, max_val, min_val)
  pairs = weight_pairing(parents, costs, costs[n_keep])
  children = one_point_crossover(pairs)

  chromosomes = parents + children
  chromosomes = mutate(chromosomes, mutation)

  print(chromosomes)

main(cost, 2, 0, 10)








