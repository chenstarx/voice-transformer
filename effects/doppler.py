from effects.effect import Effect
import math

soundspeed = 343.0  #Speed of sound
frequency = 2000.0  #frequency in Hz

class DopplerEffect(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)
        self.theta = 0
    
    def apply(self, view, input_tuple):

        self.velr = view.velocity_receiver.get()
        self.vels = view.velocity_source.get()

        diff_block = [0] * self.block_len
        
        self.f0 = ( (soundspeed + self.velr) / (soundspeed + self.vels) ) * frequency

        # Initialize phase
        self.om = 2 * math.pi * self.f0 / self.rate

        for n in range(0, self.block_len):

            x0 = input_tuple[n]

            # Amplitude modulation:
            self.theta = self.theta + self.om
            diff_block[n] = int(x0 * math.cos(self.theta) - x0)

        # keep theta betwen -pi and pi
        while self.theta > math.pi:
            self.theta = self.theta - 2*math.pi

        return diff_block
