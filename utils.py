from typing import List

from config import UNIT_SIZE, WORD_SIZE
from unit import Unit, Word


def units_to_int(units: List[Unit]) -> int:
    return sum(unit.value << i * UNIT_SIZE for i, unit in enumerate(reversed(units)))

def binary_to_int(binary: List[bool]) -> int:
    return sum(bit << i for i, bit in enumerate(reversed(binary)))

def str_instruction_to_word(instruction: str) -> Word:
    if len(instruction) != 4:
        raise ValueError("Instruction has to be 4 characters long")

    units: List[Unit] = []
    for c in instruction:
        u = Unit()
        u.from_hex(c)
        units += [u]

    return Word(units)
    
def binary_str_to_list(s: str) -> List[bool]:
    ret: List[bool] = []

    for c in s:
        if c != "1" and c != "0":
            raise ValueError("Binary string can only contain 1s and 0s.")

        ret += [True if c == "1" else False]

    return ret


def add_words(a: Word, b: Word) -> Word:
    a_bits: List[bool] = a.to_binary()
    b_bits: List[bool] = b.to_binary()

    a_rev = list(reversed(a_bits))
    b_rev = list(reversed(b_bits))

    res: List[bool] = [False for _ in range(WORD_SIZE)]
    carry = False

    for i in range(len(a_rev)):
        digit_a = 1 if a_rev[i] else 0
        digit_b = 1 if b_rev[i] else 0
        digit_carry = 1 if carry else 0

        local_sum = digit_a + digit_b + digit_carry
        
        res[i] = True if local_sum % 2 == 1 else False

        if local_sum > 1:
            carry = True
        else:
            carry = False

    res_ordered = list(reversed(res))

    w = Word()
    w.from_binary(res_ordered)

    return w
        
def binary_not(w: Word) -> Word:
    bits = w.to_binary()
    inv_bits = [not b for b in bits]

    w = Word()
    w.from_binary(inv_bits)

    return w

def binary_and(a: Word, b: Word) -> Word:
    a_bits = a.to_binary()
    b_bits = b.to_binary()

    res_bits = [a_bits[i] and b_bits[i] for i in range(len(a_bits))]

    w = Word()
    w.from_binary(res_bits)

    return w
    
def binary_or(a: Word, b: Word) -> Word:
    a_bits = a.to_binary()
    b_bits = b.to_binary()

    res_bits = [a_bits[i] or b_bits[i] for i in range(len(a_bits))]

    w = Word()
    w.from_binary(res_bits)

    return w
    
def binary_xor(a: Word, b: Word) -> Word:
    a_bits = a.to_binary()
    b_bits = b.to_binary()

    res_bits = [a_bits[i] ^ b_bits[i] for i in range(len(a_bits))]

    w = Word()
    w.from_binary(res_bits)

    return w

def binary_circular_shift(w: Word, n: int, direction_left=True) -> Word:
    bits = w.to_binary()

    if not direction_left:
        bits = bits[::-1]

    res_bits = bits[n:] + bits[0:n]

    if not direction_left:
        res_bits = res_bits[::-1]

    w = Word()
    w.from_binary(res_bits)

    return w