from time import sleep
import math, random
from turtle import *
speed(0)
tracer(0,0)
hideturtle()

class Person:

    def __init__(self):
        self.state = 'normal'
        self.incubation_state = 0
        self.quarintine_time = 0
        self.deathcounter = 0
        self.infectables = []
        self.sicko_state = 0
    
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
        self.important_list = []
        self.scale = 2
        self.tick_counter = 0


        for r in self.pop_list:
            for x in range(self.size):
                person = Person()
                r.append(person)
    
    def classify(self):
        for r in range(0,len(self.pop_list),1):
            for x in range(0,len(self.pop_list[r]),1):
                if x == 0:
                    if r == 0:
                        self.pop_list[r][x].place = 'top_left_corner'
                        self.pop_list[r][x].infectables = [[0,1],[1,0]]
                    if r == len(self.pop_list[r])-1:
                        self.pop_list[r][x].place = 'bottom_left_corner'
                        self.pop_list[r][x].infectables = [[len(self.pop_list)-2,0],[len(self.pop_list)-1,1]]
                    if self.pop_list[r][x].infectables == []:
                        self.pop_list[r][x].place = 'left_edge'
                        self.pop_list[r][x].infectables = [[r,x+1],[r-1,x],[r+1,x]]

                if x == len(self.pop_list[r])-1:
                    if r == len(self.pop_list)-1:
                        self.pop_list[r][x].place = 'bottom_right_corner'
                        self.pop_list[r][x].infectables = [[r-1,x],[r,x-1]]
                    if r == 0:
                        self.pop_list[r][x].place = 'top_right_corner'
                        self.pop_list[r][x].infectables = [[r,x-1],[r+1,x]]
                    if self.pop_list[r][x].infectables == []:
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
                
                if self.pop_list[r][x].infectables == []:
                    self.pop_list[r][x].place = 'normal'
                    self.pop_list[r][x].infectables = [[r-1,x],[r,x+1],[r,x-1],[r+1,x]]

    def change_state(self,r_value,x_value,new_state):
        self.pop_list[r_value][x_value].state = new_state
        self.important_list.append([r_value,x_value])

    def expose_friends(self,person):
        for i in person.infectables:
            if self.pop_list[i[0]][i[1]].state == 'normal':
                self.change_state(i[0],i[1],'exposed')
    
    def expose(self):
        for r_ind,r in enumerate(self.pop_list):
            for x_ind,x in enumerate(r):
                if x.state == 'infected':
                    self.expose_friends(x)

    def infect(self):
        for r_ind,r in enumerate(self.pop_list):
            for x_ind,x in enumerate(r):
                if x.state == 'exposed':
                    if random.randint(1,100) > 100-self.infect_chance:
                        self.change_state(r_ind,x_ind,'infected')
    
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
                        self.change_state(r,x,'quarintined')
                        self.quarintine.append([r,x])

    def quarintine_update(self):
        for g in range(len(self.quarintine)-1,-1,-1):
            i = self.quarintine[g]
            self.pop_list[i[0]][i[1]].quarintine_time += 1
            if random.randint(0,100) < 100 * (self.pop_list[i[0]][i[1]].quarintine_time/self.cure_time):
                self.change_state(i[0],i[1],'immune')
                self.quarintine.pop(g)

    def death_update(self):
        for r in range(0,len(self.pop_list),1):
            for x in range(0,len(self.pop_list[r]),1):
                if self.pop_list[r][x].state == 'quarintined':
                    self.pop_list[r][x].deathcounter += 1
                    if random.randint(0,100) <= self.death_chance:
                       self.change_state(r,x,'dead')
        
        for r in range(len(self.quarintine)-1,-1,-1):
            i = self.quarintine[r]
            if self.pop_list[i[0]][i[1]].state == 'dead':
                self.quarintine.pop(r)

    def clear_effects(self):
        for r_ind,r in enumerate(self.pop_list):
            for x_ind,x in enumerate(r):
                if x.state == 'exposed':
                    self.change_state(r_ind,x_ind,'normal')

    def tick(self):
        self.infect()
        self.clear_effects()
        self.expose()
        self.death_update()
        self.update_incubation_state()
        self.quarintine_update()
        self.tick_counter += 1
    
    def drawgrid(self,xcord,ycord):
        color('grey')
        begin_fill()
        up()
        goto(xcord,ycord)
        down()
        scale = self.scale
        xcord += len(self.pop_list)*scale
        goto(xcord,ycord)
        ycord += len(self.pop_list)*scale
        goto(xcord,ycord)
        xcord -= len(self.pop_list)*scale
        goto(xcord,ycord)
        ycord -= len(self.pop_list)*scale
        goto(xcord,ycord)
        end_fill()
        
    def write_tick(self,xcord,ycord):
        up()
        goto(xcord+20,ycord-20)
        down()
        color('white')
        write(str(self.tick_counter-1))
        color('black')
        write(str(self.tick_counter))

    def draw(self,xcord,ycord):
        #print(self.important_list)
        for i in self.important_list:
            scale = self.scale
            up()
            goto(xcord+scale*(i[1]),ycord+scale*len(self.pop_list)-scale*(i[0]+1))
            down()
            #print(xcord+5*(i[1]+1),ycord+5*len(self.pop_list)-5*(i[0]+1))
            x=self.pop_list[i[0]][i[1]]
            if x.state not in ('exposed'):
                if x.state == 'normal':
                    color('grey')
                if x.state == 'exposed':
                    color('green')
                if x.state == 'infected':
                    color('red')
                if x.state == 'immune':
                    color('blue')
                if x.state == 'quarintined':
                    color('orange')
                if x.state == 'dead':
                    color('black')
                if x.sicko_state == 1:
                    color(x.color)
                    begin_fill()
                    for r in range(3):
                        forward(scale)
                        left(90)
                    end_fill()
                    setheading(0)
                forward(scale)


population = Population(250,250,40,3,10,20) #row, column, infection chance, days till incubation done, days till cured, chance die %
population.scale = 2
xcord,ycord = -250,-250

population.classify()


Jack_P = population.pop_list[random.randint(0,len(population.pop_list)-1)][random.randint(0,len(population.pop_list[0])-1)]
Jack_P.state = 'infected'
'''
Chris_S = population.pop_list[random.randint(0,len(population.pop_list)-1)][random.randint(0,len(population.pop_list[0])-1)]
Alex_M = population.pop_list[random.randint(0,len(population.pop_list)-1)][random.randint(0,len(population.pop_list[0])-1)]
Phil_K = population.pop_list[random.randint(0,len(population.pop_list)-1)][random.randint(0,len(population.pop_list[0])-1)]
Pierre_L = population.pop_list[random.randint(0,len(population.pop_list)-1)][random.randint(0,len(population.pop_list[0])-1)]
'''
sickos = [Jack_P]
colors = ['cyan','darkgreen','darkblue','purple','magenta']
for i,r in enumerate(sickos):
    r.state = 'infected'
    r.sicko_state = 1
    r.color = colors[i]



amount_infected = 1
population.drawgrid(xcord,ycord)
up()
goto(xcord,ycord-20)
down()
color('black')
write("Day #:")

while amount_infected != 0:
    population.tick()
    population.draw(xcord,ycord)
    update()
    population.important_list = []
    amount_infected = 0
    #population.write_tick(xcord,ycord)

    for r in population.pop_list:
        for x in r:
            if x.state in ('infected','quarintined','exposed'):
                amount_infected += 1
#population.print()


mainloop()