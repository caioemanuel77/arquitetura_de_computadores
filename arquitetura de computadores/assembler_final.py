import sys

# Constantes de Cabeçalho
HEADER_OFFSET = 4

# Dicionário principal de opcodes
OPCODES = {
    'load': 0x01, 'add': 0x02, 'sub': 0x0D, 'goto': 0x09,
    'mov':  0x06, 'jz':  0x0B, 'halt': 0xFF, 'jn':   0x11,
    'shr8': 0x23, 'and': 0x2D, 'shr1': 0x32
}

# Categorização para cálculo automático de memória
OP_1_BYTE = {'halt', 'shr8', 'shr1', 'wb'}
OP_2_BYTE = {'load', 'add', 'sub', 'mov', 'jz', 'goto', 'jn', 'and'}
OP_4_BYTE = {'ww'}

def build_symbol_table(source_code):
    """ Mapeia os labels para seus respectivos endereços na memória """
    sym_table = {}
    current_addr = HEADER_OFFSET

    for tokens in source_code:
        head = tokens[0]
        
        if head in OPCODES or head in ['wb', 'ww']:
            cmd = head
        else:
            sym_table[head] = current_addr
            if len(tokens) > 1:
                cmd = tokens[1]
            else:
                continue

        # Calcula o avanço do PC
        if cmd in OP_1_BYTE: current_addr += 1
        elif cmd in OP_2_BYTE: current_addr += 2
        elif cmd in OP_4_BYTE: current_addr += 4

    return sym_table

def resolve_memory_operand(args_list, symbols):
    """ Encontra o endereço da variável desconsiderando o registrador 'x' """
    if len(args_list) < 2: return None
    target_var = args_list[1] if args_list[0] == 'x' else args_list[0]
    
    if target_var in symbols:
        return symbols[target_var] // 4
    return None

def pack_word_32bit(value_str):
    """ Empacota um inteiro em 4 bytes (Little Endian) """
    try:
        v = int(value_str)
        return [v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF, (v >> 24) & 0xFF]
    except ValueError:
        return []

def generate_bytecode(source_code, sym_table):
    """ Monta o binário final """
    out_bin = bytearray()
    entry_point = None

    # Descobre a primeira instrução para o GOTO inicial
    for tokens in source_code:
        if tokens[0] not in OPCODES and tokens[0] not in ['wb', 'ww']:
            if len(tokens) > 1 and tokens[1] not in ['wb', 'ww']:
                entry_point = tokens[0]
                break

    if entry_point and entry_point in sym_table:
        out_bin.extend([OPCODES['goto'], sym_table[entry_point], 0x00, 0x00])
    else:
        for lbl in sym_table:
            sym_table[lbl] -= HEADER_OFFSET

    # Geração do código
    for tokens in source_code:
        if tokens[0] in OPCODES or tokens[0] in ['wb', 'ww']:
            cmd, args = tokens[0], tokens[1:]
        else:
            if len(tokens) > 1:
                cmd, args = tokens[1], tokens[2:]
            else:
                continue

        # 1-Byte Instructions
        if cmd in OP_1_BYTE and cmd != 'wb':
            out_bin.append(OPCODES[cmd])

        # Operações na ULA e Memória (2 Bytes)
        elif cmd in ['load', 'add', 'sub', 'mov', 'and']:
            addr = resolve_memory_operand(args, sym_table)
            if addr is not None:
                out_bin.extend([OPCODES[cmd], addr])
            else:
                print(f"[Assembly Error] Variavel nao encontrada: {cmd} {args}")
                return None

        # Saltos (2 Bytes)
        elif cmd in ['goto', 'jz', 'jn']:
            if args and args[0] in sym_table:
                out_bin.extend([OPCODES[cmd], sym_table[args[0]]])
            else:
                print(f"[Assembly Error] Label de pulo invalido: {cmd} {args}")
                return None

        # Definição de Variáveis de 32 bits
        elif cmd == 'ww':
            out_bin.extend(pack_word_32bit(args[0]))

    return out_bin

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python assembler.py <codigo.asm> <saida.bin>")
        sys.exit(1)

    # Limpeza e Padronização do arquivo
    with open(sys.argv[1], 'r') as src:
        raw_lines = src.read().splitlines()

    parsed_code = []
    for line in raw_lines:
        clean_str = line.replace(',', ' ').replace('\t', ' ').replace('\xa0', ' ')
        parts = clean_str.strip().lower().split()
        if parts:
            parsed_code.append(parts)

    # Fluxo principal do compilador
    symbols_map = build_symbol_table(parsed_code)
    final_binary = generate_bytecode(parsed_code, symbols_map)

    if final_binary:
        with open(sys.argv[2], 'wb') as dst:
            dst.write(final_binary)
        print(">> Compilacao concluida com sucesso!")