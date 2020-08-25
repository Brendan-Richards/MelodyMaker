class Note:
    def __init__(self, velocity, note_num, note_type, time_sig):
        self.velocity = velocity
        self.note_num = note_num
        self.note_type = note_type
        self.num_beats = self.get_num_beats(time_sig[1])

    def get_num_beats(self, bottom):
        if self.note_type == "whole":
            return bottom
        elif self.note_type == "half":
            return bottom/2.0
        elif self.note_type == "quarter":
            return bottom/4.0
        elif self.note_type == "eighth":
            return bottom/8.0
        elif self.note_type == "sixteenth":
            return bottom/16.0
        elif self.note_type == "thirty-second":
            return bottom/32.0
        else:
            print("unknown note type: ", self.note_type)
            exit(-1)