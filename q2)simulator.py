class Memory:
    def __init__(self):
        self.memory = [0] * 256

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value

    def dump(self):
        for data in self.memory:
            print(f"{data:016b}")


class ProgramCounter:
    def __init__(self):
        self.pc = 0

    def get(self):
        return self.pc

    def update(self, new_pc):
        self.pc = new_pc

    def dump(self):
        print(f"{self.pc:07b}", end=" ")


class RegisterFile:
    def __init__(self):
        self.registers = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0,
            "R4": 0,
            "R5": 0,
            "R6": 0,
            "FLAGS": 0,
        }

    def read(self, register):
        return self.registers[register]

    def write(self, register, value):
        self.registers[register] = value

    def dump(self):
        for register in self.registers.values():
            print(f"{register:016b}", end=" ")


class ExecutionEngine:
    def __init__(self, memory, register_file):
        self.memory = memory
        self.register_file = register_file

    def execute(self, instruction):
        opcode = instruction[:3]

        if opcode == "000":  # mov
            register1 = instruction[3:6]
            operand2 = instruction[6:16]

            if operand2[0] == "0":
                value = int(operand2, 2)
            else:
                value = int(operand2, 2) - 2 ** 10

            self.register_file.write(register1, value)

        # Add the code for other instructions here

        elif opcode == "111":  # hlt
            return True, self.register_file.read("PC")

        return False, self.register_file.read("PC") + 1


def simulate():
    memory = Memory()
    register_file = RegisterFile()
    execution_engine = ExecutionEngine(memory, register_file)

    # Load memory from stdin
    for address, line in enumerate(sys.stdin):
        data = line.strip()
        memory.write(address, int(data, 2))

    program_counter = ProgramCounter()
    halted = False

    while not halted:
        instruction = memory.read(program_counter.get())
        halted, new_pc = execution_engine.execute(f"{instruction:016b}")

        # Print PC
        program_counter.dump()

        # Print RF state
        register_file.dump()

        # Update PC
        program_counter.update(new_pc)

        print()  # Newline after each instruction

    # Print the complete memory
    memory.dump()


if __name__ == "__main__":
    simulate()
