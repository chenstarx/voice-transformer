from effects.effect import Effect

class PitchShift(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)
        self.theta = 0
    
    def apply(self, view, input_tuple):

        diff_block = [0] * self.block_len

        return diff_block
