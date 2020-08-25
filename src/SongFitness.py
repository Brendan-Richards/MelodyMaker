from MidiParse import MidiParser
from Dissonance import *
import numpy as np
import os
import matplotlib.pyplot as plt

# gets the average and standard deviation of the dissonance for the specified midi file
def get_song_stats_from_file(filename, track_type, note2freq, n=50):

    print('parsing file:', filename)
    parser = MidiParser()
    piano_roll = parser.parse_file(filename, track_type)

    mean, stdev = get_piano_roll_stats(piano_roll, note2freq, n)

    return mean, stdev


def get_piano_roll_stats(piano_roll, note2freq, n=50):
    dscores = []

    for slice in piano_roll:
        # calculate dissonance for this slice
        notes = np.nonzero(slice)[0]
        note_pairs = []
        for note in notes:
            note_pairs.append((note2freq[note], 'piano'))
        dscores.append(dtotal(note_pairs))

    # calculate the moving average series
    cumsum, moving_aves = [0], []

    for i, x in enumerate(dscores, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= n:
            moving_ave = (cumsum[i] - cumsum[i - n]) / n
            # can do stuff with moving_ave here
            moving_aves.append(moving_ave)

    # normalize the moving average array
    moving_aves = (np.array(moving_aves)/max(moving_aves)).tolist()
    #dscores = (np.array(dscores) / max(dscores)).tolist()

    # plot the averages
    # x_vals = np.linspace(1, len(dscores)+1, num=len(dscores))*.0228794642
    # #plt.plot(x_vals, dscores)
    # plt.plot(x_vals, [0]*(N-1) + moving_aves)
    # plt.show()

    stdev = np.std(moving_aves)
    mean = np.mean(moving_aves)

    #print('     stdev', stdev)
    #print('     mean', mean)

    return mean, stdev



# collect the note to frequency list from a file
def get_freqs():
    freqs = []
    with open('../frequencies.txt') as file:
        lines = file.readlines()
        for line in lines:
            freqs.append(float(line))
    return freqs


# used once to parse the html containing the note frequencies
def get_note_freqs():
    freqs = [0]*128
    with open('note_html.txt') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip()=='<tr>':
                note = int(lines[i+1].replace('<td>', '').replace('</td>', '').strip())
                freq = float(lines[i+6].replace('<td>', '').replace('</td>', '').strip())
                freqs[note] = freq
                i += 8
    with open('frequencies.txt', 'w') as file:
        for freq in freqs:
            file.write(str(freq) + '\n')


# calculate the dissonance of all the simple midid songs to get the average mean and the average standard deviation
def parse_files(midi_directory):
    note2freq = get_freqs()
    track_type = 'piano'
    means = []
    stdevs = []

    #midi_directory = os.path.dirname(__file__) + '/simple_midi_songs'
    for fname in os.listdir(midi_directory):
        filename = 'simple_midi_songs/' + fname
        mean, stdev = get_song_stats_from_file(filename, track_type, note2freq)
        means.append(mean)
        stdevs.append(stdev)

    print(means)
    print(stdevs)
    print('average dissonance mean:', np.mean(means))
    print('average standard deviation:', np.mean(stdevs))


def get_fitness(piano_roll, note2freq):
    optimal_mean = 0.242593176329089
    optimal_stdev = 0.21551727704606313
    mean, stdev = get_piano_roll_stats(piano_roll, note2freq)

    return (mean-optimal_mean + stdev-optimal_stdev)*100
