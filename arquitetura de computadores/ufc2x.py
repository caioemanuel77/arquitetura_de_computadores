import memory
from array import array

def bitwise_divmod(n, d, bit=31, q=0, r=0):
    # Condição de parada usando bitwise em vez de relacional (interrompe quando bit vai abaixo de 0)
    if bit & 0x80000000: 
        return q, r
    
    r = (r << 1) | ((n >> bit) & 1)
    diff = r - d
    
    # Substitui 'if not (diff >> 64):' por verificação do bit de sinal em 32/64 bits
    if not (diff & 0x8000000000000000):
        r = diff
        q = q | (1 << bit)
        
    # Decremento sem operador relacional
    return bitwise_divmod(n, d, (bit - 1) & 0xFFFFFFFF, q, r)

def bitwise_mul(a, b, bit=0, res=0):
    # Condição de parada: quando passa de 31 bits, encerra (testa se o bit 5 está ativo, ou seja, bit de controle 32)
    if bit & 32: 
        return res
        
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

# ADD (Opcode 2)
firmware[2] = 0b00000001100000110101001000001001
firmware[3] = 0b00000010000000010100100000010010
firmware[4] = 0b00000010100000010100000001000000
firmware[5] = 0b00000000000000111100000100000011             

# STORE (Opcode 6)
firmware[6] = 0b000000111_000_00110101_001000_001_001
firmware[7] = 0b000001000_000_00010100_100000_000_010
firmware[8] = 0b000000000_000_00010100_010000_100_011

# JMP (Opcode 9)
firmware[9]  = 0b000001010_000_00110101_001000_001_001
firmware[10] = 0b000000000_100_00010100_001000_001_010

# JZ (Opcode 11)
firmware[11] =  0b000001100_001_00010100_000000_000_011
firmware[12] =  0b000000000_000_00110101_001000_000_001
firmware[268] = 0b000001001_000_00000000_000000_000_000

# SUB (Opcode 13)
firmware[13] = 0b00000111000000110101001000001001
firmware[14] = 0b00000111100000010100100000010010
firmware[15] = 0b00001000000000010100000001000000
firmware[16] = 0b00000000000000111111000100000011

# LOAD (Opcode 20)
firmware[20] = 0b00001010100000110101001000001001 
firmware[21] = 0b00001011000000010100100000010010
firmware[22] = 0b00001011100000010100000001000000
firmware[23] = 0b00000000000000011000000100000000

# INC (Opcode 24)
firmware[24] = 0b000000000_000_00110101_000100_000_011

# DEC (Opcode 25)
firmware[25] = 0b000000000_000_00110110_000100_000_011

# CLEAR (Opcode 26)
firmware[26] = 0b000000000_000_00010000_000100_000_000

# JNZ (Opcode 27)
firmware[27] = 0b000011100_001_00010100_000000_000_011
firmware[28] = 0b000001001_000_00000000_000000_000_000
firmware[284] = 0b000000000_000_00110101_001000_000_001
firmware[286] = 0b000001001_000_00000000_000000_000_000

# MOVXY (Opcode 31)
firmware[31] = 0b000000000_000_00010100_000010_000_011

# MOVYX (Opcode 32)
firmware[32] = 0b000000000_000_00010100_000100_000_100

# MUL (Opcode 33)
firmware[33] = int("00010001000000010100000001000100", 2)
firmware[34] = int("00000000000000100000000100000011", 2)

# MOD (Opcode 36)
firmware[36] = int("00010110000000010100000001000100", 2)
firmware[44] = int("00000000000000100001000100000011", 2)

# DIV (Opcode 39)
firmware[39] = int("00010100000000010100000001000100", 2)
firmware[40] = int("00000000000000100010000100000011", 2)

# AND (Opcode 47)
firmware[47] = int("00011000000000010100000001000100", 2)
firmware[48] = int("00000000000000001100000100000011", 2)

# JN (Opcode 49)
firmware[49] = int("00000110001000010100000000000011", 2)
firmware[305] = int("00000100100000000000000000000000", 2)

# GET_BYTE (Opcode 37) e SHR_BYTE (Opcode 38)
firmware[37] = 0b000000000_000_000111_000100_000_100
firmware[38] = 0b000000000_000_11010100_000010_000_100

# HALT (Opcode 255)
firmware[255] = 0b00000000000000000000000000000000


#==============================================================================
# COMPONENTES DE HARDWARE DA CPU
#==============================================================================

def read_regs(reg_num):
    global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B
    
    BUS_A = H
    
    # Substituído '==' por teste XOR bitwise ('not (a ^ b)')
    if not reg_num:
       BUS_B = MDR
    elif not (reg_num ^ 1):
       BUS_B = PC
    elif not (reg_num ^ 2):
       BUS_B = MBR
    elif not (reg_num ^ 3):
       BUS_B = X
    elif not (reg_num ^ 4):
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
    
    # Substituído '==' por teste XOR bitwise ('not (control_bits ^ VAL)')
    if not (control_bits ^ 0b011000):
       o = a
    elif not (control_bits ^ 0b010100):
       o = b
    elif not (control_bits ^ 0b011010):
       o = ~a
    elif not (control_bits ^ 0b101100):
       o = ~b
    elif not (control_bits ^ 0b111100):
       o = a + b
    elif not (control_bits ^ 0b111101):
       o = a + b + 1
    elif not (control_bits ^ 0b111001):
       o = a + 1
    elif not (control_bits ^ 0b110101):
       o = b + 1
    elif not (control_bits ^ 0b111111):
       o = b - a
    elif not (control_bits ^ 0b110110):
       o = b - 1
    elif not (control_bits ^ 0b111011):
       o = -a
    elif not (control_bits ^ 0b001100):
       o = a & b
    elif not (control_bits ^ 0b011100):
       o = a | b
    elif not (control_bits ^ 0b010000):
       o = 0
    elif not (control_bits ^ 0b110001):
       o = 1
    elif not (control_bits ^ 0b110010):
       o = -1
    elif not (control_bits ^ 0b000111): 
       o = b & 0xFF
    elif not (control_bits ^ 0b100000): 
       o = bitwise_mul(a, b)
    elif not (control_bits ^ 0b100001):
       o = bitwise_divmod(b, a)[1] if a else 0
    elif not (control_bits ^ 0b100010): 
       o = bitwise_divmod(b, a)[0] if a else 0

    o = o & 0xFFFFFFFF

    Z = 0
    N = 0

    # Removido '== 0'
    if not o:
       Z = 1

    if o & 0x80000000:
       N = 1    
    
    if not (shift_bits ^ 0b01):
       o = (o << 1) & 0xFFFFFFFF
    elif not (shift_bits ^ 0b10):
       o = o >> 1
    elif not (shift_bits ^ 0b11):
       o = o >> 8 

    BUS_C = o
    
def next_instruction(nextadd, jam):
    global MPC
    
    # Removido '== 0b000'
    if not jam:
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
   
   # Removido '== 0'
   if not MIR:
      return False
   
   read_regs( MIR & 0b00000000000000000000000000000111 )
   alu((MIR & 0b00000000000011111111000000000000) >> 12)
   write_regs( (MIR & 0b00000000000000000000111111000000) >> 6)
   memory_io( (MIR & 0b00000000000000000000000000111000) >> 3 )
   next_instruction(MIR >> 23, (MIR & 0b00000000011100000000000000000000) >> 20)
   
   return True