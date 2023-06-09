import re

# Define the instruction mnemonics and their corresponding opcodes
instructions = {
    'add': '00000',
    'sub': '00001',
    'mov_imm': '00010',
    'mov_reg': '00011',
    'ld': '00100',
    'st': '00101',
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '11100',
    'jgt': '11101',
    'je': '11111',
    'hlt': '11010'
}

# Define the register addresses
registers = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}

# Initialize variables to store labels and variables
labels = {}
variables = {}
variable_address = 0


def process_instruction(line):
    global variable_address
    line = line.strip()
    if line.startswith('var'):
        # Variable declaration
        var_name = line.split()[1]
        variables[var_name] = variable_address
        variable_address += 1
    elif line.endswith(':'):
        # Label definition
        label = line[:-1]
        labels[label] = variable_address
    else:
        # Instruction parsing
        parts = re.split(r'\s+', line)
        opcode = instructions.get(parts[0])
        if opcode:
            if opcode in ['00010', '01000', '01001']:
                # Instructions with immediate value
                register1 = registers.get(parts[1])
                immediate = format(int(parts[2]), '07b')
                instruction = opcode + '00' + register1 + immediate
            elif opcode in ['00011', '01101']:
                # Instructions with register
                register1 = registers.get(parts[1])
                register2 = registers.get(parts[2])
                instruction = opcode + '00000' + register1 + register2
            elif opcode in ['00100', '00101']:
                # Load and Store instructions
                register1 = registers.get(parts[1])
                mem_addr = format(variables.get(parts[2]), '07b')
                instruction = opcode + '0' + register1 + mem_addr
            elif opcode in ['01110', '01111', '11100', '11101']:
                # Jump and Compare instructions
                mem_addr = format(labels.get(parts[1]), '07b')
                instruction = opcode + '000' + mem_addr
            elif opcode == '11010':
                # Halt instruction
                instruction = opcode + '0000000000'
            else:
                # Instructions with 3 registers
                register1 = registers.get(parts[1])
                register2 = registers.get(parts[2])
                register3 = registers.get(parts[3])
                instruction = opcode + '000' + register1 + register2 + register3

            return instruction

    return None


def assemble(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    instructions_binary = []
    errors = []

    # Process each line of the input file
    for line_num, line in enumerate(lines):
        line = line.strip()
        if line == '':
            # Ignore empty lines
            continue
        elif line.startswith('var') or line.endswith(':'):
            # Variable declaration or label definition
            instruction = process_instruction(line)
            if instruction:
                instructions_binary.append(instruction)
            else:
                errors.append(f"Syntax error at line {line_num + 1}")
        else:
            # Instruction line
            instruction = process_instruction(line)
            if instruction:
                instructions_binary.append(instruction)
            else:
                errors.append(f"Syntax error at line {line_num + 1}")

    # Check for errors
    if errors:
        for error in errors:
            print(error)
        return

    # Check if 'hlt' instruction is present as the last instruction
    if instructions_binary[-1] != '1101000000000000':
        print("Error: 'hlt' instruction missing or not used as the last instruction")
        return

    # Write the binary instructions to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(instructions_binary))

    print("Assembly successful. Binary file generated.")

# Test the assembler
input_file = 'assembly_program.txt'
output_file = 'binary_code.txt'
assemble(input_file, output_file)



