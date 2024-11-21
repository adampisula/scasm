UNIT_SIZE = 4
WORD_SIZE = 16

if WORD_SIZE % UNIT_SIZE != 0:
    raise ValueError(f"Word size {WORD_SIZE} must be a multiple of unit size {UNIT_SIZE}")