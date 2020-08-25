from Part import Part
from Note import Note

class Song:

    def __init__(self, tempo, time_sig, num_bars, parents=()):
        self.tempo = tempo
        self.time_sig = time_sig
        self.num_bars = num_bars
        self.parts = []

        if not parents:
            self.randomSong()
        elif len(parents) == 2:
            self.crossover(*parents)
        else:
            print('error, ', len(parents), ' parents were passed to Song constructor.')
            exit(-1)

    def randomSong(self):
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
