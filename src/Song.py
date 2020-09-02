from Part import Part
from Note import Note
import random as rand
#import SongFitness as fit
from Chord import Chord
import copy

class Song:

    def __init__(self, tempo, time_sig, num_bars, parents=()):
        self.tempo = tempo
        self.fitness = None
        self.time_sig = time_sig # time_sig[0] is the numerator
        self.num_bars = num_bars
        #self.note_types = ["whole", "half", "quarter", "eighth", "sixteenth"]#, "thirty-second"]
        self.note_types = ['quarter', 'eighth', 'half']
        self.parts = [Part("piano"), Part("guitar")]
        self.chordID = 0 # the next chord to make when creating a song
        self.mutation_prob = 0.05
        self.num_mutations = 1
        self.chords = ["Dmaj", "Amaj", "Bmin", "Gmaj"]
        self.chord2notes = self.get_chord2notes()
        self.all_chord_notes = self.get_chord_notes()
        self.times = ["half", "half", "half", "half"]
        self.flow = None
        self.variety = None
        self.relevance = None
        self.num_notes = None
        #self.note2freq = fit.get_freqs()

        if not parents:
            self.random_song()
        elif len(parents) == 2:
            self.crossover(*parents)
            self.mutate()
        else:
            print('error, ', len(parents), ' parents were passed to Song constructor.')
            exit(-1)
        self.calc_fitness()

    def get_chord_notes(self):
        # base notes are all the notes that make up the chord progression
        base_notes = set([note for sublist in self.chord2notes.values() for note in sublist])

        all_notes = set()
        for note in base_notes:
            all_notes.add(note+12)
            # ctr = note - 12
            # while ctr > 0:
            #     all_notes.add(ctr)
            #     ctr -= 12
            # ctr = note + 12
            # while ctr < 127:
            #     all_notes.add(ctr)
            #     ctr += 12

        return all_notes

    def get_chord2notes(self):
        chord2notes = dict()

        # major chords
        chord2notes["Amaj"] = self.maj_chord(57)
        chord2notes["A#maj"] = self.maj_chord(58)
        chord2notes["Bbmaj"] = self.maj_chord(58)
        chord2notes["Bmaj"] = self.maj_chord(59)
        chord2notes["Cmaj"] = self.maj_chord(60)
        chord2notes["C#maj"] = self.maj_chord(61)
        chord2notes["Dbmaj"] = self.maj_chord(61)
        chord2notes["Dmaj"] = self.maj_chord(62)
        chord2notes["D#maj"] = self.maj_chord(63)
        chord2notes["Ebmaj"] = self.maj_chord(63)
        chord2notes["Emaj"] = self.maj_chord(64)
        chord2notes["Fmaj"] = self.maj_chord(65)
        chord2notes["F#maj"] = self.maj_chord(66)
        chord2notes["Gbmaj"] = self.maj_chord(66)
        chord2notes["Gmaj"] = self.maj_chord(67)
        chord2notes["G#maj"] = self.maj_chord(68)
        chord2notes["Abmaj"] = self.maj_chord(68)

        chord2notes["Amin"] = self.min_chord(57)
        chord2notes["A#min"] = self.min_chord(58)
        chord2notes["Bbmin"] = self.min_chord(58)
        chord2notes["Bmin"] = self.min_chord(59)
        chord2notes["Cmin"] = self.min_chord(60)
        chord2notes["C#min"] = self.min_chord(61)
        chord2notes["Dbmin"] = self.min_chord(61)
        chord2notes["Dmin"] = self.min_chord(62)
        chord2notes["D#min"] = self.min_chord(63)
        chord2notes["Ebmin"] = self.min_chord(63)
        chord2notes["Emin"] = self.min_chord(64)
        chord2notes["Fmin"] = self.min_chord(65)
        chord2notes["F#min"] = self.min_chord(66)
        chord2notes["Gbmin"] = self.min_chord(66)
        chord2notes["Gmin"] = self.min_chord(67)
        chord2notes["G#min"] = self.min_chord(68)
        chord2notes["Abmin"] = self.min_chord(68)

        return chord2notes

    def maj_chord(self, root):
        return [root, root+4, root+7]

    def min_chord(self, root):
        return [root, root+3, root+7]

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
        self.parts = copy.deepcopy(p1.parts)
        crosspoint = rand.randint(0, len(p1.parts[0].bars) - 1)
        self.parts[1].bars[crosspoint:] = copy.deepcopy(p2.parts[1].bars[crosspoint:])

    def mutate(self):
        if rand.random() < self.mutation_prob:
            for _ in range(self.num_mutations):
                bar_index = rand.randint(0, len(self.parts[1].bars)-1)
                note_index = rand.randint(0, len(self.parts[1].bars[bar_index])-1)
                note_num = rand.randint(*self.parts[1].note_range)
                self.parts[1].bars[bar_index][note_index].note_num = note_num

    def calc_fitness(self):

        num_notes_weight = 30
        flow_weight = 1
        rel_weight = 200
        var_weight = 50

        self.flow = self.get_flow() * flow_weight
        self.relevance = self.get_relevance() * rel_weight
        self.variety = self.get_variety() * var_weight
        self.num_notes = self.get_num_notes() * num_notes_weight

        #print("\nflow: ", flow, "\nrelevance: ", relevance, "\nvariety: ", variety)

        self.fitness = self.flow + self.relevance + self.variety + self.num_notes
        #self.fitness = rel_weight*relevance + flow_weight*flow
        #print("fitness: ", self.fitness)
        #self.fitness = self.count_60s()

    def get_num_notes(self):
        count = 0
        for bar in self.parts[1].bars:
            for note in bar:
                count += 1
        return (1/count)*100

    def count_60s(self):
        count = 0
        for bar in self.parts[1].bars:
            for note in bar:
                if note.note_num == 60:
                    count += 1
        return (count*100)

    def get_flow(self):
        total = 0

        prev = None
        for bar in self.parts[1].bars:
            for note in bar:
                if prev:
                    total += abs(note.note_num - prev.note_num)
                else:
                    prev = note

        return total

    def get_relevance(self):
        num_bad_notes = 0

        for bar in self.parts[1].bars:
            for note in bar:
                if not note.note_num in self.all_chord_notes:
                    num_bad_notes += 1

        return num_bad_notes

    def get_variety(self):
        notes = set()

        for bar in self.parts[1].bars:
            for note in bar:
                notes.add(note.note_num)

        return (1.0/len(notes))*100




