import numpy
import ga

"""
The y=target is to maximize this equation ASAP:
    y = w1x1+w2x2+w3x3+w4x4+w5x5+6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7)
    What are the best values for the 6 weights w1 to w6?
    We are going to use the genetic algorithm for the best possible values after a number of generations.
"""

equation_inputs = [4,-2,3.5,5,-11,-4.7]

num_weights = 6

"""
Genetic algorithm parameters:
    Mating pool size
    Population size
"""
sol_per_pop = 8
num_parents_mating = 4

pop_size = (sol_per_pop,num_weights)
new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
print(new_population)

num_generations = 5
for generation in range(num_generations):
    print("Generation : ", generation)
    fitness = ga.cal_pop_fitness(equation_inputs, new_population)

    parents = ga.select_mating_pool(new_population, fitness, 
                                      num_parents_mating)

    offspring_crossover = ga.crossover(parents,
                                       offspring_size=(pop_size[0]-parents.shape[0], num_weights))

    offspring_mutation = ga.mutation(offspring_crossover)

    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    print("Best result : ", numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))

fitness = ga.cal_pop_fitness(equation_inputs, new_population)
best_match_idx = numpy.where(fitness == numpy.max(fitness))

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])







import numpy

def cal_pop_fitness(equation_inputs, pop):

    fitness = numpy.sum(pop*equation_inputs, axis=1)
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        parent1_idx = k%parents.shape[0]
        parent2_idx = (k+1)%parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value
    return offspring_crossover





def next_generation(gen, upper_limit, lower_limit):
    elit = {}
    next_gen = {}
    elit['Individuals'] = gen['Individuals'].pop(-1)
    elit['Fitness'] = gen['Fitness'].pop(-1)
    selected = selection(gen)
    parents = pairing(elit, selected)
    offsprings = [[[mating(parents[x])
                    for x in range(len(parents))]
                    [y][z] for z in range(2)] 
                    for y in range(len(parents))]
    offsprings1 = [offsprings[x][0]
                   for x in range(len(parents))]
    offsprings2 = [offsprings[x][1]
                   for x in range(len(parents))]
    unmutated = selected['Individuals']+offsprings1+offsprings2
    mutated = [mutation(unmutated[x], upper_limit, lower_limit) 
        for x in range(len(gen['Individuals']))]
    unsorted_individuals = mutated + [elit['Individuals']]
    unsorted_next_gen = \
        [fitness_calculation(mutated[x]) 
         for x in range(len(mutated))]
    unsorted_fitness = [unsorted_next_gen[x]
        for x in range(len(gen['Fitness']))] + [elit['Fitness']]
    sorted_next_gen = \
        sorted([[unsorted_individuals[x], unsorted_fitness[x]]
            for x in range(len(unsorted_individuals))], 
                key=lambda x: x[1])
    next_gen['Individuals'] = [sorted_next_gen[x][0]
        for x in range(len(sorted_next_gen))]
    next_gen['Fitness'] = [sorted_next_gen[x][1]
        for x in range(len(sorted_next_gen))]
    gen['Individuals'].append(elit['Individuals'])
    gen['Fitness'].append(elit['Fitness'])
    return next_gen






Result_file = 'GA_Results.txt'# Creating the First Generation
def first_generation(pop):
    fitness = [fitness_calculation(pop[x]) 
        for x in range(len(pop))]
    sorted_fitness = sorted([[pop[x], fitness[x]]
        for x in range(len(pop))], key=lambda x: x[1])
    population = [sorted_fitness[x][0] 
        for x in range(len(sorted_fitness))]
    fitness = [sorted_fitness[x][1] 
        for x in range(len(sorted_fitness))]
    return {'Individuals': population, 'Fitness': sorted(fitness)}pop = population(20,8,1,0)
gen = []
gen.append(first_generation(pop))
fitness_avg = np.array([sum(gen[0]['Fitness'])/
                        len(gen[0]['Fitness'])])
fitness_max = np.array([max(gen[0]['Fitness'])])
res = open(Result_file, 'a')
res.write('\n'+str(gen)+'\n')
res.close()finish = False
while finish == False:
    if max(fitness_max) > 6:
        break
    if max(fitness_avg) > 5:
        break
    if fitness_similarity_chech(fitness_max, 50) == True:
        break
    gen.append(next_generation(gen[-1],1,0))
    fitness_avg = np.append(fitness_avg, sum(
        gen[-1]['Fitness'])/len(gen[-1]['Fitness']))
    fitness_max = np.append(fitness_max, max(gen[-1]['Fitness']))
    res = open(Result_file, 'a')
    res.write('\n'+str(gen[-1])+'\n')
    res.close()







import numpy as np
import random
 
class Individ:
    def __init__(self):
        self.A=np.random.randint(0,2,30)    
        self.fit=0                          
    def fitness(self):                    
        summa=0
        for i in range(30):                 
            summa=summa+self.A[i]           
        self.fit=summa
 
    def info(self):                         
        print(self.A)                       
        self.fitness()                      
        print(self.fit)                     
 
class Population:
    def __init__(self):
        self.B = []                    
        for i in range(10):            
            c=Individ()               
            self.B.append(c)           
    def info(self):                    
        for i in range(10):            
            for j in range(30):        
                print(self.B[i].A[j], end ="") 
            print("=",end="")          
            self.B[i].fitness()        
            print(self.B[i].fit)       
 
pop1=Population()                      
pop1.info()                            
 
Mother = Individ()                     
Father = Individ()                     
Son1 = Individ()                       
Son2 = Individ()
ParAndSons = []
 
for j in range(20):                    
    ParAndSons.append(Individ())        
                                        
 
print("\n")                            
 
for p in range(60):                    
                                         
    for i in range(10):                
        for j in range(30):
            ParAndSons[i].A[j]=pop1.B[i].A[j]
 
    tt=0                                       
    for s in range(0,10,2):                    
        for j in range(30):                     
            Mother.A[j]=pop1.B[tt+5].A[j]      
            Father.A[j]=pop1.B[random.randint(0,9)].A[j] 
 
        tt=tt+1    
 
        ran=random.random()
 
        if (ran>0.8):                          
            for n in range(5):                 
                Son1.A[n]=Father.A[n]
                Son2.A[n]=Mother.A[n]
 
            for n in range(5,30):               
 
                Son1.A[n]=Mother.A[n]
                Son2.A[n]=Father.A[n]
 
        if ((ran>0.6) & (ran <=0.8)):          
            for n in range(15):                
                Son1.A[n]=Father.A[n]          
                Son2.A[n]=Mother.A[n]
            for n in range(16,30):
                Son1.A[n]=Mother.A[n]
                Son2.A[n]=Father.A[n]
 
        if ((ran <0.6) & (ran >=0.4)):          
            for n in range(25):
                Son1.A[n]=Father.A[n]
                Son2.A[n]=Mother.A[n]
            for n in range(25,30):
                Son1.A[n] = Mother.A[n]
                Son2.A[n] = Father.A[n]
 
        if ((ran <0.4) & (ran>=0.3)):          
            for n in range(15):
                Son1.A[n]=Father.A[14-n]
                Son2.A[n]=Mother.A[14-n]
            for n in range(15,30):
                Son1.A[n]=Mother.A[44-n]
                Son2.A[n]=Father.A[44-n]
 
        if (ran<0.3):                          
            for n in range(15):                
                Son1.A[n]=Father.A[n]
                Son1.A[n+15]=Mother.A[n]
                Son2.A[n]=Mother.A[n+15]
                Son2.A[n+15]=Father.A[n+15]
 
        for i in range(30):                    
            ParAndSons[10+s].A[i]=Son1.A[i]
            ParAndSons[11+s].A[i]=Son2.A[i]
 
    for r in range(17,18):                
        for w in range(30):               
            if random.random()<0.00001:   
                if ParAndSons[r].A[w]==1: 
                    ParAndSons[r].A[w]=0  
                if ParAndSons[r].A[w]==0:
                    ParAndSons[r].A[w]=1
 
    for i in range(20):                     
        ParAndSons[i].fitness()            
 
    for m in range(len(ParAndSons)-1,0,-1):             
        for b in range(m):                              
            if ParAndSons[b].fit > ParAndSons[b+1].fit: 
                mem = ParAndSons[b]                     
                ParAndSons[b] = ParAndSons[b+1]
                ParAndSons[b+1] = mem
 
    for i in range(10):                             
        for j in range(30):                         
            pop1.B[i].A[j]=ParAndSons[i+10].A[j]   
 
    pop1.info()                                    
    print()
