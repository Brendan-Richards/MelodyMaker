

def get_fitness(parts):
    return 1

# def get_num_notes(self):
#     count = 0
#     for bar in self.parts[1].bars:
#         for note in bar:
#             count += 1
#     return (1/count)*100
#
# def count_60s(self):
#     count = 0
#     for bar in self.parts[1].bars:
#         for note in bar:
#             if note.note_num == 60:
#                 count += 1
#     return (count*100)
#
# def get_flow(self):
#     total = 0
#
#     prev = None
#     for bar in self.parts[1].bars:
#         for note in bar:
#             if prev:
#                 total += abs(note.note_num - prev.note_num)
#             else:
#                 prev = note
#
#     return total
#
# def get_relevance(self):
#     num_bad_notes = 0
#
#     for bar in self.parts[1].bars:
#         for note in bar:
#             if not note.note_num in self.all_chord_notes:
#                 num_bad_notes += 1
#
#     return num_bad_notes
#
# def get_variety(self):
#     notes = set()
#
#     for bar in self.parts[1].bars:
#         for note in bar:
#             notes.add(note.note_num)
#
#     return (1.0/len(notes))*100