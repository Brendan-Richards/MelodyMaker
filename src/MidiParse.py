from mido import Message, MidiFile, MidiTrack, MetaMessage

def save(parts, output_filename):

    mid = MidiFile(type=1)

    melody_velocity = 64
    chord_velocity = 64
    melody_channel = 0
    chord_channel = 1

    # melody track
    track1 = MidiTrack()
    track1.append(Message('program_change', channel=melody_channel, program=25, time=0))
    for bar in parts[1].bars:
        for note in bar:
            track1.append(Message('note_on', channel=melody_channel, note=note.note_num, velocity=melody_velocity, time=0))
            duration_ticks = int(note.num_beats*mid.ticks_per_beat)
            track1.append(Message('note_off', channel=melody_channel, note=note.note_num, velocity=melody_velocity, time=duration_ticks))

    # chord track
    track2 = MidiTrack()
    track2.append(Message('program_change', channel=chord_channel, program=1, time=0))

    for bar in parts[0].bars:
        for chord in bar:
            for note in chord.notes:
                track2.append(Message('note_on', channel=chord_channel, note=note, velocity=chord_velocity, time=0))
            duration_ticks = int(chord.num_beats*mid.ticks_per_beat)
            # track2.append(Message('note_off', note=chord.notes[0], velocity=chord_velocity, time=duration_ticks))
            # for i in range(1, len(chord.notes)):
            #     track2.append(Message('note_off', note=chord.notes[i], velocity=chord_velocity, time=0))
            track2.append(Message('note_off', channel=chord_channel, note=chord.notes[0], velocity=0, time=duration_ticks))
            for i in range(1, len(chord.notes)):
                track2.append(Message('note_off', channel=chord_channel, note=chord.notes[i], velocity=0, time=0))

    mid.tracks.append(track1)
    mid.tracks.append(track2)

    mid.save(output_filename + '.mid')

