from effects.effect import Effect
import math

class AMEffect(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)
        self.theta = 0

    def apply(self, view, input_tuple):

        self.gain = view.am_feedback.get() / 100
        self.f0 = view.am_frequency.get()

        diff_block = [0] * self.block_len
        
        # Initialize phase
        self.om = 2 * math.pi * self.f0 / self.rate

        # self.theta = 0

        for n in range(0, self.block_len):

            x0 = input_tuple[n]

            # Amplitude modulation:
            self.theta = self.theta + self.om
            diff_block[n] = int( self.gain * (x0 * math.cos(self.theta) - x0) )

            
        # keep theta betwen -pi and pi
        while self.theta > math.pi:
            self.theta = self.theta - 2*math.pi

        return diff_block