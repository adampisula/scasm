from typing import Callable, Dict, List, Tuple

from config import WORD_SIZE
from unit import Unit, Word
from utils import add_words, binary_and, binary_circular_shift, binary_not, binary_or, units_to_int


class Register:
    content: Word

    def __init__(self):
        self.content = Word()

    def set(self, value: Word):
        self.content = value

    def get(self) -> Word:
        return self.content


class Computer:
    registers: Dict[int, Register] = {
        0: Register(),
    }
    memory: Dict[int, Word]


    def __init__(self, init_memory: Dict[int, Word]={}):
        self.memory = init_memory

    def decode(self, instruction: Word) -> Tuple[int, str, Callable, List[Unit]]:
        opcode = instruction.units[0].value

        if opcode not in self.INSTRUCTIONS:
            raise NotImplementedError(f"{opcode} instruction not implemented")

        return opcode, *self.INSTRUCTIONS[opcode], instruction.units[1:]

    def execute(self, function: Callable, operands: List[Unit], program_counter: int, name: str) -> int:
        print(f"{hex(program_counter)[2:].upper()}: Executing {name} with operands {[o.to_hex() for o in operands]}")
        return function(self, operands, program_counter)

    def set_register(self, register_num: int, value: Word):
        if register_num not in self.registers:
            self.registers[register_num] = Register()
        self.registers[register_num].set(value)

    def get_register(self, register_num: int) -> Word:
        return self.registers.get(register_num, Register()).get()

    def get_memory(self, address: int) -> Word:
        return self.memory.get(address, Word())
    
    def set_memory(self, address: int, value: Word):
        self.memory[address] = value

    def __load(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_num = operands[0].value
        mem_address = units_to_int(operands[1:])

        self.set_register(register_num, self.get_memory(mem_address))
        return pc + 1

    def __store(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        mem_address = units_to_int(operands[0:2])
        register_num = operands[2].value

        self.set_memory(mem_address, self.get_register(register_num))
        return pc + 1

    def __addi(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src_a = operands[1].value
        register_src_b = operands[2].value

        sum_ab = add_words(self.get_register(register_src_a), self.get_register(register_src_b))

        self.set_register(register_dest, sum_ab)
        return pc + 1

    def __move(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src = operands[1].value

        self.set_register(register_dest, self.get_register(register_src))
        return pc + 1

    def __not(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src = operands[1].value

        inv = binary_not(self.get_register(register_src))
        self.set_register(register_dest, inv)
        return pc + 1

    def __and(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src_a = operands[1].value
        register_src_b = operands[2].value

        and_res = binary_and(self.get_register(register_src_a), self.get_register(register_src_b))
        self.set_register(register_dest, and_res)
        return pc + 1

    def __or(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src_a = operands[1].value
        register_src_b = operands[2].value

        or_res = binary_or(self.get_register(register_src_a), self.get_register(register_src_b))
        self.set_register(register_dest, or_res)
        return pc + 1

    def __xor(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register_dest = operands[0].value
        register_src_a = operands[1].value
        register_src_b = operands[2].value

        xor_res = binary_or(self.get_register(register_src_a), self.get_register(register_src_b))
        self.set_register(register_dest, xor_res)
        return pc + 1

    def __inc(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register = operands[0].value

        a = self.get_register(register)

        one = Word()
        one.from_binary([True])

        inc_res = add_words(a, one)
        self.set_register(register, inc_res)
        return pc + 1

    def __dec(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register = operands[0].value

        a = self.get_register(register)

        negative_one = Word()
        negative_one.from_binary([True for _ in range(WORD_SIZE)])  # 2's complement

        dec_res = add_words(a, negative_one)
        self.set_register(register, dec_res)
        return pc + 1

    def __rot(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register = operands[0].value
        n = operands[1].value
        d = operands[2].value

        if d != 0 and d != 1:
            raise ValueError(f"ROT only accepts 1 or 0 for direction")

        a = self.get_register(register)
        rot_res = binary_circular_shift(a, n, True if d == 1 else False)

        self.set_register(register, rot_res)
        return pc + 1

    def __jump(self, operands: List[Unit], pc: int):
        if len(operands) != 3:
            raise ValueError(f"Expected 3 operands, got {len(operands)}")

        register = operands[0].value
        n = units_to_int(operands[1:3])

        if self.get_register(register).to_binary() != self.get_register(0).to_binary():
            pc = n - 1

        return pc + 1
        

    INSTRUCTIONS: Dict[int, Tuple[str, Callable]] = {
        0: ("HALT", lambda: None),
        1: ("LOAD", __load),
        2: ("STORE", __store),
        3: ("ADDI", __addi),
        5: ("MOVE", __move),
        6: ("NOT", __not),
        7: ("AND", __and),
        8: ("OR", __or),
        9: ("XOR", __xor),
        10: ("INC", __inc),
        11: ("DEC", __dec),
        12: ("ROT", __rot),
        13: ("JUMP", __jump),
    }