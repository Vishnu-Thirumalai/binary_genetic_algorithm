"""
Chromosomes : Intial
Ranked: Chromosomes sorted by weight + weights
Selected: Top n_keep chromosomes + weights
Parents: Binary strings of selected chromosomes
Costs: Normalised costs of chromosomes
Probs: Cumulative probabilities for chromosomes
Pairs: Pairs of parents
new_pop: Newly generated chromosomes
"""

import random
import math

chromosomes = [(3,4),(2,8),(4,7),(2,9)] #Student Number
for i in range(len(chromosomes)):
  chromosomes.append( (chromosomes[i][1],chromosomes[i][0],) )

def cost(chromosome):
  x = chromosome[0]
  y = chromosome[1] 
  return (-10*x**2 + 7*x*y - 7 * y**2 - 4)  #Cost Function


ranked = sorted(list(zip(chromosomes, list(map(cost,chromosomes)))), key = lambda c:c[1])

n_keep = 4
selected = ranked[:n_keep]
weight = ranked[n_keep][1]

precision = 5
bin_low = -7 #Lower point of range
bin_high = 14
bin_value = (bin_high - bin_low) / (2**precision-1) #Range of numbers
def encode(pair):
  x_val = round( (pair[0] - bin_low)/bin_value )  
  x = bin(x_val)[2:].rjust(precision,'0')
  y_val = round( (pair[1] - bin_low)/bin_value )  
  y = bin(y_val)[2:].rjust(precision,'0')
  return x+y

def decode(chromosome):
  x = round(int(chromosome[:precision], 2)*bin_value)  + bin_low
  y = round(int(chromosome[precision:], 2)*bin_value) + bin_low
  return (x,y)

parents = list(map(lambda c:encode(c[0]), selected))
costs = list(map(lambda c:c[1]-weight, selected))
total = sum(costs)


probs = []
run_sum = 0
for i in range(n_keep):
    run_sum += costs[i]/total
    probs.append(run_sum)


pairs = []
select_probs = [ 6/19, 1-(6/19)] #Selection Numbers
for i in range(len(select_probs)):
  for j in range(n_keep):
    if select_probs[i] < probs[j]:
      pairs.append(parents[j])
      break

for p in pairs:
  parents.remove(p)

if len(parents) > 2:
  print("Same parent picked")
  pairs.extend(random.sample(parents,2))
else:
  pairs.extend(parents)

pairs = [pairs[i:i+2] for i in range(0,len(pairs),2)]
split = [round(9/2), round(5/2)] #Crossover Points

new_pop = []
for i in range(len(split)):
  a = pairs[i][0]
  b = pairs[i][1]

  new_pop.append(a)
  new_pop.append(b)
  new_pop.append(a[:split[i]] + b[split[i]:])
  new_pop.append(b[:split[i]] + a[split[i]:])


mutation_rate = 0.25
n_bits = 3
pop = len(new_pop)
size = len(new_pop[0])
mutation = math.floor(mutation_rate * pop * n_bits)
mut_bits = random.sample(range (0,pop*size), mutation)


for bit in mut_bits: #To highlight bits, c is chromsome number, pos is index in chromsome
  pos = math.floor(bit % size)
  c = math.floor(bit / size)
  b = new_pop[c]
  new_pop[c] = b[:pos] + ('1' if b[pos]=='0' else '0') + b[pos+1:]



