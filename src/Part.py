class Part:
    def __init__(self, instrument):
        self.instrument = instrument
        self.range = self.get_range()

    def get_range(self):
        None