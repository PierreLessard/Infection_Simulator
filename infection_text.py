import math, random
from turtle import *

class Person:

    def __init__(self):
        self.state = 'normal'
        self.incubation_state = 0
        self.quarintine_time = 0
        self.deathcounter = 0
    
    def infect(self):
        self.state = 'infected'

class Population:

    def __init__(self,size,rows,infect_chance, incubation_rate = 4, cure_time = 4, death_chance=25):

        self.rows = rows
        self.size = size
        self.pop_list = [[]for x in range(self.rows)]
        self.infect_chance = infect_chance
        self.incubation_rate = incubation_rate
        self.quarintine = []
        self.cure_time = cure_time
        self.death_chance = death_chance


        for r in self.pop_list:
            for x in range(self.size):
                person = Person()
                r.append(person)
    
    def classify(self):
        for r in range(0,len(self.pop_list),1):
            for x in range(0,len(self.pop_list[r]),1):
                self.pop_list[r][x].infectables = 0
                if x == 0:
                    if r == 0:
                        self.pop_list[r][x].place = 'top_left_corner'
                        self.pop_list[r][x].infectables = [[0,1],[1,0]]
                    if r == len(self.pop_list[r])-1:
                        self.pop_list[r][x].place = 'bottom_left_corner'
                        self.pop_list[r][x].infectables = [[len(self.pop_list)-2,0],[len(self.pop_list)-1,1]]
                    if self.pop_list[r][x].infectables == 0:
                        self.pop_list[r][x].place = 'left_edge'
                        self.pop_list[r][x].infectables = [[r,x+1],[r-1,x],[r+1,x]]

                if x == len(self.pop_list[r])-1:
                    if r == len(self.pop_list)-1:
                        self.pop_list[r][x].place = 'bottom_right_corner'
                        self.pop_list[r][x].infectables = [[r-1,x],[r,x-1]]
                    if r == 0:
                        self.pop_list[r][x].place = 'top_right_corner'
                        self.pop_list[r][x].infectables = [[r,x-1],[r+1,x]]
                    if self.pop_list[r][x].infectables == 0:
                        self.pop_list[r][x].place = 'right_edge'
                        self.pop_list[r][x].infectables = [[r,x-1],[r-1,x],[r+1,x]]
                
                if r == 0:
                    if x not in (0,len(self.pop_list[r])-1):
                        self.pop_list[r][x].place = 'top_edge'
                        self.pop_list[r][x].infectables = [[r,x+1],[r,x-1],[r+1,x]]
                
                if r == len(self.pop_list) - 1:
                    if x not in (0,len(self.pop_list[r])-1):
                        self.pop_list[r][x].place = 'bottom_edge'
                        self.pop_list[r][x].infectables = [[r,x+1],[r,x-1],[r-1,x]]
                
                if self.pop_list[r][x].infectables == 0:
                    self.pop_list[r][x].place = 'normal'
                    self.pop_list[r][x].infectables = [[r,x+1],[r,x-1],[r+1,x],[r-1,x]]

    def expose_friends(self,person):
        for i in person.infectables:
            if self.pop_list[i[0]][i[1]].state == 'normal':
                self.pop_list[i[0]][i[1]].state = 'exposed'
    
    def expose(self):
        for r in self.pop_list:
            for x in r:
                if x.state == 'infected':
                    self.expose_friends(x)

    def infect(self):
        for r in self.pop_list:
            for x in r:
                if x.state == 'exposed':
                    if random.randint(1,100) > 100-self.infect_chance:
                        x.state = 'infected'
    
    def print(self):
        for r in self.pop_list:
            summary =''
            for x in r:
                if x.state == 'exposed':
                    summary = str(summary) +'='
                if x.state == 'infected':
                    summary = str(summary) +'+'
                if x.state == 'normal':
                    summary = str(summary) +'-'
                if x.state == 'immune':
                    summary = str(summary) +'Φ'
                if x.state == 'quarintined':
                    summary = str(summary) +'&'
                if x.state == 'dead':
                    summary = str(summary) +'ᚙ'
            print(summary)
    
    def update_incubation_state(self):
        for r in range(0,len(self.pop_list),1):
            for x in range(0,len(self.pop_list[r]),1):
                if self.pop_list[r][x].state == 'infected':
                    self.pop_list[r][x].incubation_state += 1
                    if self.pop_list[r][x].incubation_state >= self.incubation_rate:
                        self.pop_list[r][x].state = 'quarintined'
                        self.quarintine.append([r,x])

    def quarintine_update(self):
        for g in range(len(self.quarintine)-1,-1,-1):
            i = self.quarintine[g]
            self.pop_list[i[0]][i[1]].quarintine_time += 1
            if random.randint(0,100) < 100 * (self.pop_list[i[0]][i[1]].quarintine_time/self.cure_time):
                self.pop_list[i[0]][i[1]].state = 'immune'
                self.quarintine.pop(g)

    def death_update(self):
        for r in range(0,len(self.pop_list),1):
            for x in range(0,len(self.pop_list[r]),1):
                if self.pop_list[r][x].state == 'quarintined':
                    self.pop_list[r][x].deathcounter += 1
                    if random.randint(0,100) <= self.death_chance:
                       self.pop_list[r][x].state = 'dead' 
        
        for r in range(len(self.quarintine)-1,-1,-1):
            i = self.quarintine[r]
            if self.pop_list[i[0]][i[1]].state == 'dead':
                self.quarintine.pop(r)



    def tick(self):
        self.infect()
        self.expose()
        self.death_update()
        self.update_incubation_state()
        self.quarintine_update()

class MegaPopulation:

    def __init__(self,amount,size,rows,infect_chance, incubation_rate = 4, cure_time = 4, death_chance=25):
        self.amount = amount
        self.mega_pop_list = []
        self.area = size*rows

        for r in range(amount):
            population = Population(size,rows,infect_chance,incubation_rate,cure_time,death_chance)
            self.mega_pop_list.append(population)
    
    def run_simulations(self):
        print('Running Simulation: \n')
        tick_count = 0
        for i in self.mega_pop_list:
            i.classify()
            i.pop_list[random.randint(0,len(i.pop_list)-1)][random.randint(0,len(i.pop_list[0])-1)].state = 'infected'
            
            amount_infected = 1
            while amount_infected != 0:
                tick_count += 1
                i.tick()

                amount_infected = 0
                for r in i.pop_list:
                    for x in r:
                        if x.state in ('infected','quarintined'):
                            amount_infected += 1
            print('.',end='',flush=True)
        self.average_tick_count = tick_count / len(self.mega_pop_list)
    
    def find_diagnostics(self):
        dead_amount = 0
        normal_amount = 0
        immune_amount = 0
        min_dead_amount = self.area
        max_dead_amount = 0
        min_normal_amount = self.area
        max_normal_amount = 0
        min_immune_amount = self.area
        max_immune_amount = 0
        for i in self.mega_pop_list:
            local_dead_amount = 0
            local_normal_amount = 0
            local_immune_amount = 0
            for r in i.pop_list:
                for x in r:
                    if x.state == 'dead':
                        dead_amount += 1
                        local_dead_amount += 1
                    if x.state == 'normal':
                        normal_amount += 1
                        local_normal_amount += 1
                    if x.state == 'immune':
                        immune_amount += 1
                        local_immune_amount += 1
            if local_immune_amount < min_immune_amount:
                min_immune_amount = local_immune_amount
            if local_immune_amount > max_immune_amount:
                max_immune_amount = local_immune_amount
            if local_dead_amount < min_dead_amount:
                min_dead_amount = local_dead_amount
            if local_dead_amount > max_dead_amount:
                max_dead_amount = local_dead_amount
            if local_normal_amount < min_normal_amount:
                min_normal_amount = local_normal_amount
            if local_normal_amount > max_normal_amount:
                max_normal_amount = local_normal_amount


        self.dead_average = dead_amount/len(self.mega_pop_list)
        self.normal_average = normal_amount/len(self.mega_pop_list)
        self.immune_average = immune_amount/len(self.mega_pop_list)
        self.max_dead_amount = max_dead_amount
        self.max_normal_amount = max_normal_amount
        self.max_immune_amount = max_immune_amount
        self.min_dead_amount = min_dead_amount
        self.min_normal_amount = min_normal_amount
        self.min_immune_amount = min_immune_amount
        self.dead_amount = dead_amount
        self.normal_amount = normal_amount
        self.immune_amount = immune_amount
    
    def print_diagnostics(self):
        print('\nAmount Dead:  ' + str(self.dead_amount))
        print('Amount Immune:  ' + str(self.immune_amount))
        print('Amount Normal:  ' + str(self.normal_amount) + '\n')
        print('Average Dead:  ' + str(self.dead_average))
        print('Average Immune:  ' + str(self.immune_average))
        print('Average Normal:  ' + str(self.normal_average) + '\n')
        print('Maximum Dead:  ' + str(self.max_dead_amount))
        print('Maximum Immune:  ' + str(self.max_immune_amount))
        print('Maximum Normal:  ' + str(self.max_normal_amount) + '\n')
        print('Minimum Dead:  ' + str(self.min_dead_amount))
        print('Minimum Immune:  ' + str(self.min_immune_amount))
        print('Minimum Normal:  ' + str(self.min_normal_amount))
        print('Average Ticks:  ' + str(self.average_tick_count))





pop_numb = 2 # ^2
mega_population = MegaPopulation(100000,pop_numb,pop_numb,50,2,2,50)
'''
number of sims, 
amount of people (rows), 
(colmns), 
infect chance, 
amount of days until 100% chance of immune (chance goes up during other time (starts in quirintine)), 
amount of days until 100% chance of death (chance goes up during other time (starts in quirintine))
'''
mega_population.run_simulations()
mega_population.find_diagnostics()
mega_population.print_diagnostics()


''' 
several types of state
state 1: normal: just kinda there and can become exposed
state 2: infected: makes those around them exposed has a chance to become quarintined
state 3: exposed: has a chance to become infected
state 4: quarintined: can not infect others, has a chance to become immune or die
state 5: immune: put back into the population and can not become exposed/infected
state 6: dead: dead, can not interact with others
'''