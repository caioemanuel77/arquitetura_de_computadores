import memory
from array import array

def bitwise_divmod(n, d, bit=31, q=0, r=0):
    if bit >> 64: return q, r
    r = (r << 1) | ((n >> bit) & 1)
    diff = r - d
    if not (diff >> 64):
        r = diff
        q = q | (1 << bit)
    return bitwise_divmod(n, d, bit - 1, q, r)

def bitwise_mul(a, b, bit=0, res=0):
    if not ((bit - 32) >> 64): return res
    if (b >> bit) & 1:
        res = res + (a << bit)
    return bitwise_mul(a, b, bit + 1, res)

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
# MUL (Opcode 33) -> Calcula X * Y em apenas 2 ciclos
#==============================================================================
# 33: H = Y -> NEXT: 34
firmware[33] = int("00010001000000010100000001000100", 2)

# 34: X = H * X -> NEXT: 0, ALU: MUL (100000)
firmware[34] = int("00000000000000100000000100000011", 2)

#==============================================================================
# MOD (Opcode 36) -> Calcula X % Y em apenas 2 ciclos
#==============================================================================
# 36: H = Y -> NEXT: 44
firmware[36] = int("00010110000000010100000001000100", 2)

# 44: X = X % H -> NEXT: 0, ALU: MOD (100001)
firmware[44] = int("00000000000000100001000100000011", 2)

#==============================================================================
# DIV (Opcode 39) -> Calcula X / Y em apenas 2 ciclos
#==============================================================================
# 39: H = Y -> NEXT: 40
firmware[39] = int("00010100000000010100000001000100", 2)

# 40: X = X / H -> NEXT: 0, ALU: DIV (100010)
firmware[40] = int("00000000000000100010000100000011", 2)

#==============================================================================
# AND (Opcode 47) -> Calcula X = X & Y 
#==============================================================================
# 47: Salva Y no acumulador H -> NEXT: 48
firmware[47] = int("00011000000000010100000001000100", 2)

# 48: Executa X = H & X na ULA -> NEXT: 0
firmware[48] = int("00000000000000001100000100000011", 2)

#==============================================================================
# JN (Opcode 49) -> IF X < 0 GOTO address
#==============================================================================
# 49: Testa a flag N (Negativo) -> NEXT: 12, JAM: 010 (N), ALU: B, REG_B: X
firmware[49] = int("00000110001000010100000000000011", 2)

# 305 (49 + 256): Executa o salto -> NEXT: 9
firmware[305] = int("00000100100000000000000000000000", 2)

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
    elif control_bits == 0b000111: 
       o = b & 0xFF
    elif control_bits == 0b100000: 
       o = bitwise_mul(a, b)
    elif control_bits == 0b100001:
       o = bitwise_divmod(b, a)[1] if a else 0
    elif control_bits == 0b100010: 
       o = bitwise_divmod(b, a)[0] if a else 0

    o = o & 0xFFFFFFFF

    Z = 0
    N = 0

    if o == 0:
       Z = 1

    if o & 0x80000000:
       N = 1    
    
    if shift_bits == 0b01:
       o = (o << 1) & 0xFFFFFFFF
    elif shift_bits == 0b10:
       o = o >> 1
    elif shift_bits == 0b11:
       o = o >> 8 

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