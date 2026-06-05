import memory
from array import array

MPC = 0
MIR = 0

MAR = 0
MDR = 0
PC = 0
MBR = 0
X = 0
Y = 0
H = 0

N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

firmware = array('L',[0]) * 512

#==============================================================================
# MICROPROGRAMA (FIRMWARE) - ISA EXPANDIDA E OTIMIZADA
#==============================================================================

# 0: INIT (FETCH da instrução de máquina)
firmware[0] = 0b000000000_100_00110101_001000_001_001 
              # BUS_C = PC + 1; PC = BUS_C; MBR = memory.read_byte(PC); GOTO MBR.

# ADD (Opcode 2) -> X = X + mem[address]
firmware[2] = 0b00000001100000110101001000001001
firmware[3] = 0b00000010000000010100100000010010
firmware[4] = 0b00000010100000010100000001000000
firmware[5] = 0b00000000000000111100000100000011             

# STORE (Opcode 6) -> mem[address] = X
firmware[6] = 0b000000111_000_00110101_001000_001_001
firmware[7] = 0b000001000_000_00010100_100000_000_010
firmware[8] = 0b000000000_000_00010100_010000_100_011

# JMP (Opcode 9) -> GOTO address      
firmware[9]  = 0b000001010_000_00110101_001000_001_001
firmware[10] = 0b000000000_100_00010100_001000_001_010

# JZ (Opcode 11) -> IF X == 0 GOTO address
firmware[11] =  0b000001100_001_00010100_000000_000_011
firmware[12] =  0b000000000_000_00110101_001000_000_001
firmware[268] = 0b000001001_000_00000000_000000_000_000

# SUB (Opcode 13) -> X = X - mem[address]
firmware[13] = 0b00000111000000110101001000001001
firmware[14] = 0b00000111100000010100100000010010
firmware[15] = 0b00001000000000010100000001000000
firmware[16] = 0b00000000000000111111000100000011

# LOAD (Opcode 20) -> X = mem[address]
firmware[20] = 0b00001010100000110101001000001001 
firmware[21] = 0b00001011000000010100100000010010
firmware[22] = 0b00001011100000010100000001000000
firmware[23] = 0b00000000000000011000000100000000

# INC (Opcode 24) -> X = X + 1
firmware[24] = 0b000000000_000_00110101_000100_000_011

# DEC (Opcode 25) -> X = X - 1
firmware[25] = 0b000000000_000_00110110_000100_000_011

# CLEAR (Opcode 26) -> X = 0
firmware[26] = 0b000000000_000_00010000_000100_000_000

# JNZ (Opcode 27) -> IF X != 0 GOTO address
firmware[27] = 0b000011100_001_00010100_000000_000_011
firmware[28] = 0b000001001_000_00000000_000000_000_000
firmware[284] = 0b000000000_000_00110101_001000_000_001
firmware[286] = 0b000001001_000_00000000_000000_000_000

# MOVXY (Opcode 31) -> Y = X
firmware[31] = 0b000000000_000_00010100_000010_000_011

# MOVYX (Opcode 32) -> X = Y
firmware[32] = 0b000000000_000_00010100_000100_000_100

#==============================================================================
# MUL (Opcode 33) -> Multiplica X por Y através de somas sucessivas
#==============================================================================
# 33: Inicializa o acumulador H com 0 -> NEXT: 34, JAM: 000, ALU: 010000, REG_C: 000001 (H)
firmware[33] = int("00010001000001000000000100000000", 2)

# 34: Testar se Y já é zero antes de somar -> NEXT: 35, JAM: 001 (Z), ALU: 010100 (B), REG_B: 100 (Y)
firmware[34] = int("00010101100101010000000000000100", 2)

# 35: Decrementa Y (Y = Y - 1) -> NEXT: 19, JAM: 000, ALU: 110110 (B-1), REG_C: 000010 (Y), REG_B: 100 (Y)
firmware[35] = int("00001001100011011000001000000100", 2)

# 19: Acumula X em H (H = H + X) -> NEXT: 34, JAM: 000, ALU: 111100 (A+B), REG_C: 000001 (H), REG_B: 011 (X)
firmware[19] = int("00010001000011110000000100000011", 2)

# 291 (35 + 256): Fim do loop de multiplicação -> NEXT: 0, JAM: 000, ALU: 011000 (A), REG_C: 000100 (X)
firmware[291] = int("00000000000001100000010000000000", 2)

#==============================================================================
# MOD (Opcode 36) -> Calcula X % Y através de subtrações sucessivas protegidas
#==============================================================================
# 36: Carrega Y em H -> NEXT: 21, JAM: 000, ALU: 010100, REG_C: 000001 (H), REG_B: 100 (Y)
firmware[36] = int("00001010100001010000000100000100", 2)

# 21: Loop de subtração: Testa (X - H) -> NEXT: 22, JAM: 010 (N), ALU: 111111 (B-A), REG_B: 011 (X)
firmware[21] = int("00001011001011111100000000000011", 2)

# 22: Efetiva a subtração em X -> NEXT: 21, JAM: 000, ALU: 111111 (B-A), REG_C: 000100 (X), REG_B: 011 (X)
firmware[22] = int("00001010100011111100010000000011", 2)

# 278 (22 + 256): Restaura o último valor positivo -> NEXT: 0, JAM: 000, ALU: 111100 (A+B), REG_C: 000100 (X)
firmware[278] = int("00000000000011110000010000000000", 2)

# GET_BYTE (Opcode 37) e SHR_BYTE (Opcode 38)

# GET_BYTE (Opcode 37) -> Isola o byte menos significativo de Y e coloca em X (X = Y & 0xFF)
firmware[37] = 0b000000000_000_000111_000100_000_100

# SHR_BYTE (Opcode 38) -> Desloca Y em 8 bits para a direita (Y = Y >> 8) para andar no vetor
firmware[38] = 0b000000000_000_11010100_000010_000_100

# HALT (Opcode 255) -> Interrompe a execução
firmware[255] = 0b00000000000000000000000000000000


#==============================================================================
# COMPONENTES DE HARDWARE DA CPU
#==============================================================================

def read_regs(reg_num):
    global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B
    
    BUS_A = H
    
    if reg_num == 0:
       BUS_B = MDR
    elif reg_num == 1:
       BUS_B = PC
    elif reg_num == 2:
       BUS_B = MBR
    elif reg_num == 3:
       BUS_B = X
    elif reg_num == 4:
       BUS_B = Y
    else:
       BUS_B = 0

def write_regs(reg_bits):
    global MAR, MDR, PC, X, Y, H, BUS_C
    
    if reg_bits & 0b100000:
       MAR = BUS_C
    if reg_bits & 0b010000:
       MDR = BUS_C
    if reg_bits & 0b001000:
       PC = BUS_C
    if reg_bits & 0b000100:
       X = BUS_C
    if reg_bits & 0b000010:
       Y = BUS_C
    if reg_bits & 0b000001:
       H = BUS_C

def alu(control_bits):
    global N, Z, BUS_A, BUS_B, BUS_C
    
    a = BUS_A
    b = BUS_B
    o = 0
    
    shift_bits = control_bits & 0b11000000
    shift_bits = shift_bits >> 6

    control_bits = control_bits & 0b00111111
    
    if control_bits == 0b011000:
       o = a
    elif control_bits == 0b010100:
       o = b
    elif control_bits == 0b011010:
       o = ~a
    elif control_bits == 0b101100:
       o = ~b
    elif control_bits == 0b111100:
       o = a + b
    elif control_bits == 0b111101:
       o = a + b + 1
    elif control_bits == 0b111001:
       o = a + 1
    elif control_bits == 0b110101:
       o = b + 1
    elif control_bits == 0b111111:
       o = b - a
    elif control_bits == 0b110110:
       o = b - 1
    elif control_bits == 0b111011:
       o = -a
    elif control_bits == 0b001100:
       o = a & b
    elif control_bits == 0b011100:
       o = a | b
    elif control_bits == 0b010000:
       o = 0
    elif control_bits == 0b110001:
       o = 1
    elif control_bits == 0b110010:
       o = -1
    elif control_bits == 0b000111:  # Isolador do Byte 0 de BUS_B para GET_BYTE
       o = b & 0xFF
   
    # Mascara o resultado para simular barramento de 32 bits real
    o = o & 0xFFFFFFFF

    Z = 0
    N = 0

    if o == 0:
       Z = 1

    # Checa o bit mais significativo (Bit 31) para determinar sinal negativo em 32 bits
    if o & 0x80000000:
       N = 1    
    
    if shift_bits == 0b01:
       o = (o << 1) & 0xFFFFFFFF
    elif shift_bits == 0b10:
       o = o >> 1
    elif shift_bits == 0b11:
       o = o >> 8  # Deslocamento modificado para a direita para suportar vetores

    BUS_C = o
    
def next_instruction(nextadd, jam):
    global MPC
    
    if jam == 0b000:
        MPC = nextadd
        return
        
    if jam & 0b001:
        nextadd = nextadd | (Z << 8)
        
    if jam & 0b010:
        nextadd = nextadd | (N << 8)
        
    if jam & 0b100:
        nextadd = nextadd | MBR
        
    MPC = nextadd

def memory_io(mem_bits):
    global PC, MAR, MDR, MBR
    
    if mem_bits & 0b001:
       MBR = memory.read_byte(PC)
    if mem_bits & 0b010:
       MDR = memory.read_word(MAR)
    if mem_bits & 0b100:
       memory.write_word(MAR, MDR)

def step():
   global MIR, MPC
   
   MIR = firmware[MPC]
   
   if MIR == 0:
      return False
   
   read_regs( MIR & 0b00000000000000000000000000000111 )
   alu((MIR & 0b00000000000011111111000000000000) >> 12)
   write_regs( (MIR & 0b00000000000000000000111111000000) >> 6)
   memory_io( (MIR & 0b00000000000000000000000000111000) >> 3 )
   next_instruction(MIR >> 23, (MIR & 0b00000000011100000000000000000000) >> 20)
   
   return True