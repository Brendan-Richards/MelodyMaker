#from Individual import Individual
import SongFitness as fit
#import MidiParse
from Song import Song
import random as rand

class Evolver:
    def __init__(self):

        # genetic algorithm parameters
        self.pop_size = 10
        self.curr_gen = 1
        self.max_gens = 200
        self.stop = False
        self.tourney_size = 5
        self.avg_fitness = 100000
        self.target_fitness = .01
        #self.chords = chords
        self.best = []
        self.pop = []
        self.new_pop = []

        # song parameters
        self.num_bars = 5
        self.tempo = 120
        self.time_sig = (4, 4)

    def eval_fitness(self):
        self.avg_fitness = sum(song.fitness for song in self.pop) / self.pop_size
        print('average population fitness:', self.avg_fitness)

    def init_pop(self):
        for i in range(self.pop_size):
            self.pop.append(Song(self.tempo, self.time_sig, self.num_bars))

    def check_condition(self):
        print("in check_condition()")
        print("current generation is: " + str(self.curr_gen))
        if self.curr_gen >= self.max_gens:
            self.stop = True
            print('stopping because max generations has been reached')
        else:
            for song in self.pop:
                if song.fitness <= self.target_fitness:
                    print('stopping because fit enough individual was found')
                    self.stop = True
                    self.best = song
                    break

    def next_gen(self):
        print("in next_gen()")
        self.new_pop = []
        for _ in self.pop:
            parents = self.select_parents()
            self.new_pop.append(Song(self.tempo, self.time_sig, self.num_bars, parents))
        self.pop = self.new_pop
        self.curr_gen += 1

    def select_parents(self):
        participants = []
        for i in range(self.tourney_size):
            participants.append(self.pop[rand.randint(0, len(self.pop)-1)])
        participants.sort(key=lambda x: x.fitness, reverse=False)

        return participants[0:2]


    def output_results(self):
        print("in output_results()")
        output_filename = 'solution_song.mid'
        MidiParse.save_piano_roll(self.best.piano_roll, output_filename)

    def evolve(self):
        self.init_pop()
        self.eval_fitness()
        self.check_condition()
        while not self.stop:
            self.next_gen()
            self.eval_fitness()
            self.check_condition()
        # self.output_results()


def main():
    e = Evolver()
    e.evolve()
    #a = Individual([], 10)

if __name__=='__main__':
    main()