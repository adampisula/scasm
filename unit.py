from typing import List

from config import UNIT_SIZE, WORD_SIZE


class Unit:
    value: int

    def __init__(self, value=0):
        if value < 0 or value >= 2 ** UNIT_SIZE - 1:
            raise ValueError(f"Value {value} is out of range for unit size {UNIT_SIZE}")
        
        self.value = value

    def to_binary(self) -> List[bool]:
        r = [(self.value >> i) & 1 == 1 for i in range(UNIT_SIZE)]
        return list(reversed(r))

    def from_binary(self, bits: List[bool]):
        if len(bits) != UNIT_SIZE:
            raise ValueError(f"Unit from_binary value has to be {UNIT_SIZE} bits long, got {len(bits)} bits")

        powers = [2**i for i, b in enumerate(reversed(bits)) if b]
        self.value = sum(powers)

    def to_hex(self) -> str:
        return hex(self.value)[2:].upper()

    def from_hex(self, d: str):
        if len(d) != 1:
            raise ValueError(f"from_hex expects 1 digit, got {len(d)}")
        
        v = int(f"0x{d}", 16)
        self.value = v
    

class Word:
    units: List[Unit] = []

    def __init__(self, units: List[Unit]=[]):
        self.units = units

        if len(units) == 0:
            self.units = [Unit() for _ in range(WORD_SIZE // UNIT_SIZE)]

    def to_hex(self) -> str:
        r = ""
        for u in self.units:
            r += u.to_hex()

        return r

    def to_binary(self) -> List[bool]:
        return [bit for unit in self.units for bit in unit.to_binary()]

    def from_binary(self, bits: List[bool]):
        if len(bits) > WORD_SIZE:
            raise ValueError("There cannot be more than 32 bits in Word's from_binary")

        if len(bits) < WORD_SIZE:
            bits = [False for _ in range(WORD_SIZE - len(bits))] + bits

        units: List[Unit] = []
        temp_w = Word()

        for i in range(0, len(bits) // UNIT_SIZE):
            u = Unit()
            u.from_binary(bits[i*UNIT_SIZE:(i+1)*UNIT_SIZE])

            units += [u]
            temp_w.units = units

        self.units = units