import sys
import os
import numpy as np
from pypianoroll import Multitrack, Track
import pypianoroll

class MidiParser:

    def parse_files(self, directory, track_type):
        data_x = []
        data_y = []
        total = 0
        bytes = 0
        for file in os.listdir(directory):

            print(directory + '/' + file)
            try:
                piano_roll = self.parse_file(directory + '/' + file, track_type)
            except:
                print('couldn\'t parse file for some reason. skipping')
                continue
            if piano_roll is None:
                continue
            temp_x, temp_y = self.get_training_data_multi(piano_roll)
            total += len(temp_x)
            bytes += temp_x.nbytes
            # print('temp_x shape:', temp_x.shape)
            # print('temp_y shape:', temp_y.shape)
            if len(data_x) == 0 and len(data_y) == 0:
                data_x.append(temp_x)
                data_y.append(temp_y)
            else:
                data_x.append(temp_x)
                data_y.append(temp_y)
                # data_x = np.concatenate([data_x, temp_x], axis=0)
                # data_y = np.concatenate([data_y, temp_y], axis=0)
            print('num examples:', total)
            print('size:', (bytes/1073741824), 'Gigabytes')
            #print('data shape:', data_x.shape)
        print('concatenating: ')
        return np.concatenate(data_x, axis=0), np.concatenate(data_y, axis=0)

    def parse_file(self, filename, track_type):
        return self.midi2piano_roll(filename, track_type)

    def midi2piano_roll(self, filename, track_type):

        program_range = None
        if track_type=='piano':
            program_range = (0, 8)
        elif track_type=='guitar':
            program_range = (25, 32)
        elif track_type=='bass':
            program_range = (33, 40)

        midi = Multitrack(filename)

        for track in midi.tracks:
            if program_range[0] <= track.program <= program_range[1]:
                return track.pianoroll

        print('couldn\'t find {} track in midi file {}'.format(track_type, filename))
        return None


def save_piano_roll(piano_roll, filename):
    track = Track(pianoroll=piano_roll)
    multi = Multitrack(tracks=[track])
    multi.binarize(0.1)
    pypianoroll.write(multi, '../generated_songs/' + filename)

    #fig, ax = track.plot()
    #plt.show()

def main():
    filename = 'C:\Users\Brendan\Dropbox\python 2020\MelodyMaker\simple_midi_songs\DOS.mid'
    midi = Multitrack(filename)

