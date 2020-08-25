from Part import Part
from Note import Note
import random as rand

class Song:

    def __init__(self, tempo, time_sig, num_bars, parents=()):
        self.tempo = tempo
        self.time_sig = time_sig # time_sig[0] is the numerator
        self.num_bars = num_bars
        self.note_types = ["whole", "half", "quarter", "eighth"] # "sixteenth", "thirty-second"]
        self.parts = [Part("piano"), Part("guitar")]
        self.chordID = 0 # the next chord to make when creating a song

        if not parents:
            self.random_song()
        elif len(parents) == 2:
            self.crossover(*parents)
        else:
            print('error, ', len(parents), ' parents were passed to Song constructor.')
            exit(-1)

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
            if self.can_add_note(note, total_beats):
                bar.append(note)
                total_beats += note.num_beats

        return bar

    def can_add_note(self, note, total_beats):
        return note.num_beats + total_beats <= self.time_sig[0]


    def chord_bar(self, low, high):
        None


    def crossover(self, p1, p2):
        None

    def calc_fitness(self):
        None

    def mutate(self):
        None

    def play(self):
        None

    def save(self):
        None
