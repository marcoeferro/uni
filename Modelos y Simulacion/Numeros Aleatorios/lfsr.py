import time

class PseudoRandomNumberGenerator:
    def __init__(self, initial_value, feedback_positions):
        self.current_value = initial_value
        self.feedback_positions = feedback_positions

    def generate_next_value(self):
        feedback = 0
        for pos in self.feedback_positions:
            feedback ^= (self.current_value >> pos) & 1
        self.current_value = (self.current_value >> 1) | (feedback << (self.current_value.bit_length() - 1))
        return self.current_value

    def generate_random_bits(self, num_bits):
        bits = []
        for _ in range(num_bits):
            bits.append(self.generate_next_value() & 1)
        return int(''.join(map(str, bits)), 2)
"""
This script implements a Linear Feedback Shift Register (LFSR) to generate pseudo-random numbers. 
An LFSR is a digital circuit that generates a sequence of bits based on a feedback function. 
In this case, the feedback function is determined by the `feedback_positions` parameter.

The `PseudoRandomNumberGenerator` class encapsulates the LFSR logic:
1. **Initialization:**
   - `initial_value`: The starting state of the LFSR.
   - `feedback_positions`: The positions of the bits used to calculate the feedback.
2. **`generate_next_value()`:**
   - Calculates the feedback bit based on the specified positions.
   - Shifts the current value and appends the feedback bit.
   - Returns the least significant bit of the new value.
3. **`generate_random_bits()`:**
   - Generates a specified number of random bits by repeatedly calling `generate_next_value()`.
   - Concatenates the bits into an integer.

The script initializes the PRNG with a seed based on the current time and generates 20 random bits.
"""

seed_value = int(time.time_ns())
prng = PseudoRandomNumberGenerator(seed_value, [3, 2])
print(prng.generate_random_bits(20))