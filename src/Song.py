from Part import Part
from Note import Note
import random as rand
import SongFitness as fit
from Chord import Chord

class Song:

    def __init__(self, tempo, time_sig, num_bars, parents=()):
        self.tempo = tempo
        self.fitness = None
        self.time_sig = time_sig # time_sig[0] is the numerator
        self.num_bars = num_bars
        self.note_types = ["whole", "half", "quarter", "eighth"] # "sixteenth", "thirty-second"]
        self.parts = [Part("piano"), Part("guitar")]
        self.chordID = 0 # the next chord to make when creating a song
        self.mutation_prob = 0.05
        self.num_mutations = 3
        self.chords = ["Cmaj", "Amin", "Gmaj"]
        self.times = ["half", "half", "whole"]
        self.chord2notes = self.get_chord2notes()
        self.note2freq = fit.get_freqs()

        if not parents:
            self.random_song()
        elif len(parents) == 2:
            self.crossover(*parents)
            self.mutate()
        else:
            print('error, ', len(parents), ' parents were passed to Song constructor.')
            exit(-1)
        self.calc_fitness()

    def get_chord2notes(self):
        chord2notes = dict()
        chord2notes["Cmaj"] = [48, 52, 55]
        chord2notes["Amin"] = [45, 48, 52]
        chord2notes["Gmaj"] = [43, 47, 50]
        return chord2notes

    def random_song(self):
        for i in range(self.num_bars):
            mbar = self.melody_bar(*self.parts[1].note_range)
            cbar = self.chord_bar(*self.parts[0].note_range)
            self.parts[1].bars.append(mbar)
            self.parts[0].bars.append(cbar)

    def melody_bar(self, low, high):
        total_beats = 0
        bar = []

        while total_beats < self.time_sig[0]:
            note = Note(
                1.0,
                rand.randint(low, high),
                rand.choice(self.note_types),
                self.time_sig)
            if self.can_add_note(note.num_beats, total_beats):
                bar.append(note)
                total_beats += note.num_beats

        return bar

    def can_add_note(self, num_beats, total_beats):
        return num_beats + total_beats <= self.time_sig[0]

    def chord_bar(self, low, high):
        total_beats = 0
        bar = []

        while total_beats < self.time_sig[0]:
            chord = Chord(
                1.0,
                self.chord2notes[self.chords[self.chordID]],
                self.times[self.chordID],
                self.time_sig)
            if self.can_add_note(chord.num_beats, total_beats):
                bar.append(chord)
                total_beats += chord.num_beats
                self.chordID = (self.chordID + 1) % len(self.chords)

        return bar


    def crossover(self, p1, p2):
        self.parts = p1.parts[:]
        crosspoint = rand.randint(0, len(p1.parts[0].bars)-1)
        self.parts[1].bars[crosspoint:] = p2.parts[1].bars[crosspoint:]

    def calc_fitness(self):
        self.fitness = 1

    def mutate(self):
        if rand.random() < self.mutation_prob:
            for _ in range(self.num_mutations):
                bar_index = rand.randint(0, len(self.parts[1].bars)-1)
                note_index = rand.randint(0, len(self.parts[1].bars[bar_index])-1)
                #note_type = self.parts[1].bars[bar_index][note_index].note_type
                note_num = rand.randint(*self.parts[1].note_range)
                #note = Note(1.0, note_num, note_type, self.time_sig)
                self.parts[1].bars[bar_index][note_index].note_num = note_num


    def play(self):
        None

    def save(self):
        None
