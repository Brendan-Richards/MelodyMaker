class Part:
    def __init__(self, instrument):
        self.instrument = instrument
        self.note_range = self.get_range()
        self.bars = []

    # get the midi note range for the instrument
    def get_range(self):
        if self.instrument == "guitar":
            return (40, 76)
        elif self.instrument == "piano":
            return (9, 96)
        else:
            print("instrument not recognized")
            exit(-1)
