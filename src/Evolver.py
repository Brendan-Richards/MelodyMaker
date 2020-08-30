#from Individual import Individual
#import SongFitness as fit
from MidiParse import save
from Song import Song
import random as rand
import matplotlib.pyplot as plt
import numpy as np

class Evolver:
    def __init__(self):

        # genetic algorithm parameters
        self.pop_size = 500
        self.curr_gen = 1
        self.max_gens = 100
        self.stop = False
        self.tourney_size = 5
        self.avg_fitness = 100000
        self.target_fitness = 0
        #self.chords = chords
        self.best = None
        self.pop = []
        self.new_pop = []

        # time series data
        self.fitness_data = []
        self.flow_data = []
        self.variety_data = []
        self.relevance_data = []
        self.num_notes = []

        # song parameters
        self.num_bars = 10
        self.tempo = 120
        self.time_sig = (4, 4)

    def eval_fitness(self):
        self.avg_fitness = sum(song.fitness for song in self.pop) / self.pop_size
        self.fitness_data.append(self.avg_fitness)
        self.flow_data.append(sum(song.flow for song in self.pop) / self.pop_size)
        self.variety_data.append(sum(song.variety for song in self.pop) / self.pop_size)
        self.relevance_data.append(sum(song.relevance for song in self.pop) / self.pop_size)
        self.num_notes.append(sum(song.num_notes for song in self.pop) / self.pop_size)
        print('average population fitness:', self.avg_fitness)

    def init_pop(self):
        for i in range(self.pop_size):
            self.pop.append(Song(self.tempo, self.time_sig, self.num_bars))
        self.best = min(self.pop, key=lambda x: x.fitness)
        #self.best = max(self.pop, key=lambda x: x.fitness)

    def check_condition(self):
        #print("in check_condition()")
        print("current generation is: " + str(self.curr_gen))
        if self.curr_gen >= self.max_gens:
            self.stop = True
            self.best = min(self.best, min(self.pop, key=lambda x: x.fitness), key=lambda x: x.fitness)
            #self.best = max(self.best, max(self.pop, key=lambda x: x.fitness), key=lambda x: x.fitness)
            print('stopping because max generations has been reached')
        else:
            for song in self.pop:
                if song.fitness <= self.target_fitness:
                #if song.fitness >= self.target_fitness:
                    print('stopping because fit enough individual was found')
                    self.stop = True
                    self.best = song
                    break

    def next_gen(self):
        #print("in next_gen()")
        self.new_pop = []
        for _ in self.pop:
            parents = self.select_parents()
            self.new_pop.append(Song(self.tempo, self.time_sig, self.num_bars, parents))
        self.pop = self.new_pop
        self.curr_gen += 1
        self.best = min(self.best, min(self.pop, key=lambda x: x.fitness), key=lambda x: x.fitness)

    def select_parents(self):
        participants = []
        for i in range(self.tourney_size):
            participants.append(self.pop[rand.randint(0, len(self.pop)-1)])
        participants.sort(key=lambda x: x.fitness, reverse=False)
        #participants.sort(key=lambda x: x.fitness, reverse=True)

        return participants[0:2]


    def output_results(self):
        print("in output_results()")

        x = np.linspace(1, self.curr_gen, num=self.curr_gen, dtype=int)
        #plt.plot(x, self.fitness_data, label='Average Fitness')
        plt.plot(x, self.flow_data, label='Average Flow')
        plt.plot(x, self.relevance_data, label='Average Relevance')
        plt.plot(x, self.variety_data, label='Average Variety')
        plt.plot(x, self.num_notes, label='Average number of notes')
        plt.xlabel('Generation')
        plt.legend()
        plt.show()

        output_filename = 'solution_song'
        save(self.best.parts, output_filename)

    def evolve(self):
        self.init_pop()
        #save(self.pop[0].parts)
        self.eval_fitness()
        self.check_condition()
        while not self.stop:
            self.next_gen()
            self.eval_fitness()
            self.check_condition()
        self.output_results()


def main():
    e = Evolver()
    e.evolve()

if __name__=='__main__':
    main()
