import memory

# ==========================================
# REGISTRADORES E BARRAMENTOS
# ==========================================
MPC = 0
MIR = 0
MAR = 0
MDR = 0
PC = -1
MBR = 0
X = 0
Y = 0
H = 0

N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

# ==========================================
# MICRO-INSTRUÇÕES (ROM)
# Substitui o array * 512 e evita o uso de laços
# ==========================================
firmware = {}
firmware[0]   = 0b00000000010000110101001000001001
firmware[1]   = 0b00001110100000110101101000001001
firmware[29]  = 0b00001111000000010100100000010010
firmware[30]  = 0b01100100000000010100000100000000
firmware[2]   = 0b00000001100000110101101000001001
firmware[3]   = 0b00000010000000010100100000010010
firmware[4]   = 0b00000010100000010100000001000000
firmware[5]   = 0b01100100000000111100000100000011
firmware[6]   = 0b00000011100000110101101000001001
firmware[7]   = 0b00000100000000010100100000000010
firmware[8]   = 0b01100100000000010100010000100011
firmware[9]   = 0b00000101000000110101001000001001
firmware[10]  = 0b01100100000000110110001000000010
firmware[11]  = 0b00000110000100010100000000000011
firmware[12]  = 0b01100100000000110101001000000001
firmware[268] = 0b00000100100000000000000000000000
firmware[13]  = 0b00000111000000110101101000001001
firmware[14]  = 0b00000111100000010100100000010010
firmware[15]  = 0b00001000000000010100000001000000
firmware[16]  = 0b01100100000000111111000100000011
firmware[17]  = 0b00001001001000010100000000000011
firmware[18]  = 0b01100100000000110101001000000001
firmware[274] = 0b00000100100000000000000000000000
firmware[20]  = 0b00001010100000110101101000001001
firmware[21]  = 0b00001011000000010100100000010010
firmware[22]  = 0b00001011100000010100000001000000
firmware[23]  = 0b01100100000000100000000100000011
firmware[25]  = 0b00001101000000110101101000001001
firmware[26]  = 0b00001101100000010100100000010010
firmware[27]  = 0b00001110000000010100000001000000
firmware[28]  = 0b01100100000000100001000100000011
firmware[35]  = 0b00010010000010010100000100000011
firmware[36]  = 0b00010010100010010100000100000011
firmware[37]  = 0b00010011000010010100000100000011
firmware[38]  = 0b00010011100010010100000100000011
firmware[39]  = 0b00010100000010010100000100000011
firmware[40]  = 0b00010100100010010100000100000011
firmware[41]  = 0b00010101000010010100000100000011
firmware[42]  = 0b01100100000010010100000100000011
firmware[45]  = 0b00010111000000110101101000001001
firmware[46]  = 0b00010111100000010100100000010010
firmware[47]  = 0b00011000000000010100000001000011
firmware[48]  = 0b01100100000000001100000100000000
firmware[50]  = 0b01100100000010010100000100000011 # Otimização SHR1 em 1 ciclo
firmware[200] = 0b00000000010000110101001000001001
firmware[255] = 0b00000000000000000000000000000000

# ==========================================
# FUNÇÕES DE ARQUITETURA
# ==========================================

def read_regs(src_code):
    global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B
    BUS_A = H
    
    # Substitui os ifs com == por um dicionário
    b_bus_mapping = {0: MDR, 1: PC, 2: MBR, 3: X, 4: Y}
    BUS_B = b_bus_mapping.get(src_code, 0)

def write_regs(dest_flags):
    global MAR, MDR, PC, X, Y, H, BUS_C
    # Usando máscara de bits (&) em vez de == ou !=
    if dest_flags & 0b100000: MAR = BUS_C
    if dest_flags & 0b010000: MDR = BUS_C
    if dest_flags & 0b001000: PC  = BUS_C
    if dest_flags & 0b000100: X   = BUS_C
    if dest_flags & 0b000010: Y   = BUS_C
    if dest_flags & 0b000001: H   = BUS_C

def alu(opcode_alu):
    global N, Z, BUS_A, BUS_B, BUS_C

    val_a = BUS_A
    val_b = BUS_B

    mode_shift = (opcode_alu & 0b11000000) >> 6
    func = opcode_alu & 0b00111111

    
    alu_operations = {
        0b011000: val_a,
        0b010100: val_b,
        0b011010: ~val_a,
        0b101100: ~val_b,
        0b111100: val_a + val_b,
        0b111101: val_a + val_b + 1,
        0b111001: val_a + 1,
        0b110101: val_b + 1,
        0b111111: val_b - val_a,
        0b110110: val_b - 1,
        0b111011: -val_a,
        0b001100: val_a & val_b,
        0b011100: val_a | val_b,
        0b010000: 0,
        0b110001: 1,
        0b110010: -1
    }
    
    out = alu_operations.get(func, 0)

    N = (out >> 31) & 1
    Z = int(not out)
   
    shift_ops = {
        0b00: out,
        0b01: out << 1,
        0b10: out >> 1,
        0b11: out << 8
    }
    out = shift_ops.get(mode_shift, out)

    BUS_C = out

def next_instruction(jump_addr, cond_flags):
    global MPC
    
    calc_addr = jump_addr
    
    # Adição de bits de forma matemática e com máscara, sem `if == 0`
    calc_addr |= (Z << 8) if (cond_flags & 0b001) else 0
    calc_addr |= (N << 8) if (cond_flags & 0b010) else 0
    calc_addr |= MBR if (cond_flags & 0b100) else 0
    
    MPC = calc_addr

def memory_io(io_flags):
    global PC, MAR, MDR, MBR
    if io_flags & 0b001: MBR = memory.read_byte(PC)
    if io_flags & 0b010: MDR = memory.read_word(MAR)
    if io_flags & 0b100: memory.write_word(MAR, MDR)

def step():
    global MIR, MPC
    
    # O .get(MPC, 0) evita index out of bounds e tira a necessidade do array grande
    MIR = firmware.get(MPC, 0)
    
    # 'not MIR' dispensa o uso de MIR == 0
    if not MIR: 
        return False
   
    read_regs(MIR & 0b111)
    alu((MIR & 0b00000000000011111111000000000000) >> 12)
    write_regs((MIR & 0b00000000000000000000111111000000) >> 6)
    memory_io((MIR & 0b00000000000000000000000000111000) >> 3)
    next_instruction(MIR >> 23, (MIR & 0b00000000011100000000000000000000) >> 20)
   
    return True