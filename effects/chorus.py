from effects.effect import Effect
import math

class ChorusEffect(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)

        self.W = 0.1
        self.BUFFER_LEN =  1024          # Set buffer length.
        self.buffer = self.BUFFER_LEN * [0]   # list of zeros
        
        self.kr = 0  # read index
        self.kw = int(0.5 * self.BUFFER_LEN)  # write index (initialize to middle of buffer)
        
        self.theta = 0
        
    def apply(self, view, input_tuple):

        self.f0 = view.chorus_frequency.get() / 100
        self.G = view.chorus_gain.get()

        diff_block = [0] * self.block_len

        for n in range(0, self.block_len):

            x0 = input_tuple[n]
            # Get previous and next buffer values (since kr is fractional)
            kr_prev = int(math.floor(self.kr))
            frac = self.kr - kr_prev  # 0 <= frac < 1
            kr_next = kr_prev + 1
            if kr_next == self.BUFFER_LEN:
                kr_next = 0
            
            # Chorus effect
            # diff_block[n] = x0 + int(self.G * ((1 - frac) * self.buffer[kr_prev] + frac * self.buffer[kr_next]))
            diff_block[n] = int(self.G * ((1 - frac) * self.buffer[kr_prev] + frac * self.buffer[kr_next]))
            
            # Update buffer
            self.buffer[self.kw] = x0

            self.kr = self.kr + 1 + self.W * math.sin(self.theta)

            while self.theta > math.pi:
                self.theta = self.theta - 2*math.pi

            # Ensure that 0 <= kr < BUFFER_LEN
            if self.kr >= self.BUFFER_LEN:
                # End of buffer. Circle back to front.
                self.kr = self.kr - self.BUFFER_LEN

            # Increment write index    
            self.kw = self.kw + 1
            if self.kw == self.BUFFER_LEN:
                # End of buffer. Circle back to front.
                self.kw = 0

        return diff_block