import time

class LinearFeedbackShiftRegister:
    def __init__(self, seed, tap_positions):
        self.current_state = seed #Semilla inicial
        self.tap_positions = tap_positions  #posiciones

    def generate_next_state(self):
        feedback = 0
        for pos in self.tap_positions:
            feedback ^= (self.current_state >> pos) & 1  # XOR entre los bits indicados por los pasos
        
        # Desplazamos el estado y añadimos el nuevo bit de retroalimentación
        self.current_state = (self.current_state >> 1) | (feedback << (self.current_state.bit_length() - 1))
        
        return self.current_state

    def generate_random_bits(self, length):
        output_bits = []
        for _ in range(length):
            output_bits.append(self.generate_next_state() & 1)  # Guardar el bit menos significativo
        return int(''.join(map(str,output_bits)),2)

initial_seed = int(time.time_ns())
lfsr = LinearFeedbackShiftRegister(seed=initial_seed, tap_positions=[3, 2])
print(lfsr.generate_random_bits(20))
