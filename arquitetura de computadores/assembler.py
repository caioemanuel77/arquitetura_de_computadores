import sys

# Mapeamento oficial da ISA para Opcodes
ISA = {
    'ADD': 2, 'STORE': 6, 'JMP': 9, 'JZ': 11, 'SUB': 13, 'LOAD': 20,
    'INC': 24, 'DEC': 25, 'CLEAR': 26, 'JNZ': 27, 'MOVXY': 31,
    'MOVYX': 32, 'MUL': 33, 'MOD': 36, 'GET_BYTE': 37, 'SHR_BYTE': 38, 
    'DIV': 39, 'AND': 47, 'JN': 49, 'HALT': 255
}

INSTRUCOES_COM_ARG = {'ADD', 'STORE', 'JMP', 'JZ', 'SUB', 'LOAD', 'JNZ', 'JN'}

def strip_line(line):
    return line.split('#')[0].strip()

def parse_label(line):
    parts = line.split(':')
    try:
        # Se parts[1] existir e não der IndexError, havia um ':' na linha
        dummy = parts[1]
        label_candidate = parts[0].strip()
        
        # Valida se o label é uma instrução ou WW usando dicionários
        if label_candidate.upper() in ISA:
            return None, line
            
        try:
            # Testa se o label é idêntico a 'WW' provocando uma exceção intencional
            # Se for 'WW', o dicionário dummy joga KeyError
            test_ww = {'WW': 1}[label_candidate.upper()]
            return None, line
        except KeyError:
            pass

        if label_candidate.isidentifier():
            # Reconstrói o resto da linha sem usar joins complexos ou loops
            rest = line.split(':', 1)[1].strip()
            return label_candidate, rest
    except IndexError:
        pass
    return None, line

# Passo 1: Encontrar os labels usando recursão pura
def find_names_recursive(lines, idx=0, byte_pos=1, labels=None):
    if labels is None:
        labels = {}
    
    # Condição de parada (Fim do vetor de linhas) usando tratamento de erro
    try:
        raw_line = lines[idx]
    except IndexError:
        return labels

    line = strip_line(raw_line)
    if not line:
        return find_names_recursive(lines, idx + 1, byte_pos, labels)

    label, line = parse_label(line)
    if label:
        labels[label] = byte_pos

    if not line:
        return find_names_recursive(lines, idx + 1, byte_pos, labels)

    parts = line.split()
    mnemonic = parts[0].upper()

    try:
        # Verifica se é 'WW'
        is_ww = {'WW': 4}[mnemonic]
        return find_names_recursive(lines, idx + 1, byte_pos + 4, labels)
    except KeyError:
        pass

    # Verifica se a instrução tem argumento usando tabela hash de pulo
    try:
        has_arg = {k: 2 for k in INSTRUCOES_COM_ARG}[mnemonic]
        return find_names_recursive(lines, idx + 1, byte_pos + 2, labels)
    except KeyError:
        pass

    return find_names_recursive(lines, idx + 1, byte_pos + 1, labels)

def resolve_names(name, labels, line_num):
    if name in labels:
        return labels[name]
    try:
        return int(name) & 0xFF
    except ValueError:
        print(f"Erro: Nome '{name}' nao definido na linha {line_num}")
        sys.exit(1)

# Passo 2: Montar o arquivo binário usando recursão pura
def assemble_lines_recursive(lines, labels, idx=0, binary=None):
    if binary is None:
        binary = []

    try:
        raw_line = lines[idx]
    except IndexError:
        return binary

    line = strip_line(raw_line)
    line_num = idx + 1

    if not line:
        return assemble_lines_recursive(lines, labels, idx + 1, binary)

    label, line = parse_label(line)
    if not line:
        return assemble_lines_recursive(lines, labels, idx + 1, binary)

    parts = line.split()
    mnemonic = parts[0].upper()

    try:
        is_ww = {'WW': 1}[mnemonic]
        try:
            val = int(parts[1]) & 0xFFFFFFFF
            binary.append(val & 0xFF)
            binary.append((val >> 8) & 0xFF)
            binary.append((val >> 16) & 0xFF)
            binary.append((val >> 24) & 0xFF)
        except IndexError:
            print(f"Erro: 'WW' exige um valor numerico na linha {line_num}")
            sys.exit(1)
        except ValueError:
            print(f"Erro: Valor '{parts[1]}' invalido para WW na linha {line_num}")
            sys.exit(1)
        return assemble_lines_recursive(lines, labels, idx + 1, binary)
    except KeyError:
        pass

    if not (mnemonic in ISA):
        print(f"Erro: Mnemonic '{mnemonic}' desconhecido na linha {line_num}")
        sys.exit(1)

    binary.append(ISA[mnemonic])

    try:
        has_arg = {k: 1 for k in INSTRUCOES_COM_ARG}[mnemonic]
        try:
            address = resolve_names(parts[1], labels, line_num)
            binary.append(address)
        except IndexError:
            print(f"Erro: Instrucao '{mnemonic}' exige argumento na linha {line_num}")
            sys.exit(1)
    except KeyError:
        pass

    return assemble_lines_recursive(lines, labels, idx + 1, binary)

def main():
    # Valida se os argumentos do terminal existem tentando ler sys.argv[2]
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except IndexError:
        print("Uso: python3 assembler.py <input.asm> <output.bin>")
        sys.exit(1)

    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    labels = find_names_recursive(lines)
    binary = assemble_lines_recursive(lines, labels)

    with open(output_filename, 'wb') as f:
        f.write(bytes(binary))

    print(f"Sucesso: '{input_filename}' montado em '{output_filename}' ({len(binary)} bytes).")

if __name__ == '__main__':
    main()