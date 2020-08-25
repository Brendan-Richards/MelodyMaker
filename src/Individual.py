import numpy as np
import random as rand
import math

class Individual:
    def __init__(self, parents, piano_roll_length):
        self.piano_roll_length = piano_roll_length
        self.lowest_note = 0
        self.highest_note = 127
        self.mutate_prob = .1
        self.num_replacements = math.ceil(self.piano_roll_length*0.05)
        self.piano_roll = np.zeros((self.piano_roll_length, self.highest_note - self.lowest_note + 1))
        self.fitness = 0

        if len(parents) == 0: # no parents, so make a random song
            for i in range(len(self.piano_roll)):
                num_notes = 1
                notes = rand.choices(np.linspace(self.lowest_note,
                                                 self.highest_note,
                                                 num=self.highest_note-self.lowest_note+1,
                                                 dtype=int),
                                     k=num_notes)
                #print(notes)
                for note in notes:
                    self.piano_roll[i, note] = 1
            #print(self.piano_roll)
            #print()
            self.mutate()
            #print(self.piano_roll)

        elif len(parents) == 2:
            self.crossover(parents)
            self.mutate()
        else:
            print("error trying to make individual from number of parents not equal to 2")
            exit(-1)


    def crossover(self, parents):
        p1 = parents[0]
        p2 = parents[1]
        cross_point = rand.randint(0, len(p1.piano_roll[0])-1)
        self.piano_roll[:, :cross_point] = p1.piano_roll[:, :cross_point]
        self.piano_roll[:, cross_point:] = p2.piano_roll[:, cross_point:]


    def mutate(self):
        num = rand.random()

        if num < self.mutate_prob:
            replacements = np.zeros((self.num_replacements, self.highest_note - self.lowest_note + 1))
            for i in range(self.num_replacements):
                num_notes = 1
                notes = rand.choices(np.linspace(self.lowest_note,
                                                 self.highest_note,
                                                 num=self.highest_note - self.lowest_note + 1,
                                                 dtype=int),
                                     k=num_notes)

                for note in notes:
                    replacements[i, note] = 1

            replace_location = rand.randint(0, self.piano_roll_length-self.num_replacements)
            #print('replacements:', replacements)
            #print('replace_location:', replace_location)
            self.piano_roll[replace_location : replace_location+self.num_replacements] = replacements
