from computer import Computer
from unit import Word
from utils import binary_str_to_list, str_instruction_to_word

instruction_set = [
    "1120", # 0
    "1221",
    "6220",
    "3221",
    "A200",
    "2222",
    "C221",
    "A200",
    "5100",
    "A100",
    "D206",
    "2231",
    "0000",
]

def main():
    w1 = Word()
    w1.from_binary(binary_str_to_list("100"))

    w2 = Word()
    w2.from_binary(binary_str_to_list("100"))

    i_mem = {
        32: w1,
        33: w2,
    }
    c = Computer(init_memory=i_mem)

    count = 1
    jump_count = 0
    pc = 0
    while True:
        instruction = instruction_set[pc]

        i_w = str_instruction_to_word(instruction)

        opcode, n, f, o = c.decode(i_w)
        if opcode == 0:  # halt detected 
            print("Halt")
            break

        if opcode == 13:
            jump_count += 1

        pc = c.execute(function=f, operands=o, name=n, program_counter=pc)
        count += 1

        if count % 500 == 0:
            print("R1", c.get_register(1).to_hex())
            print("R2", c.get_register(2).to_hex())
            input()

    print("M22", c.get_memory(34).to_hex())
    print("M23", c.get_memory(35).to_hex())
    print()
    print("Total instructions run:", count)
    print("Total jumps:", jump_count)

if __name__ == "__main__":
    main()