from array import array

# Cria 1 MByte de memória física real mapeada por bytes (0 a 1048575)
memory = array("B", [0]) * (1024 * 1024)

def read_word(ender):
    # Garante o alinhamento: o índice lógico de Word (1, 2, 3...) é multiplicado por 4
    byte_addr = (ender << 2) & 0xFFFFF
    # Remonta o inteiro de 32 bits a partir de 4 bytes consecutivos
    b0 = memory[byte_addr]
    b1 = memory[byte_addr + 1]
    b2 = memory[byte_addr + 2]
    b3 = memory[byte_addr + 3]
    return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
    
def write_word(ender, val):
    byte_addr = (ender << 2) & 0xFFFFF
    val = val & 0xFFFFFFFF
    # Distribui o inteiro de 32 bits em 4 bytes consecutivos na memória
    memory[byte_addr]     = val & 0xFF
    memory[byte_addr + 1] = (val >> 8) & 0xFF
    memory[byte_addr + 2] = (val >> 16) & 0xFF
    memory[byte_addr + 3] = (val >> 24) & 0xFF
    
def read_byte(ender):
    return memory[ender & 0xFFFFF]
    
def write_byte(ender, val):
    memory[ender & 0xFFFFF] = val & 0xFF