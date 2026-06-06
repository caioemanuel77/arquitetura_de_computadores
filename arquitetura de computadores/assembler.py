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
    if ':' in line:
        colon_idx = line.index(':')
        label_candidate = line[:colon_idx].strip()
        if label_candidate.isidentifier() and label_candidate.upper() not in ISA and label_candidate.upper() != 'WW':
            rest = line[colon_idx + 1:].strip()
            return label_candidate, rest
    return None, line

def find_names(lines):
    labels = {}
    byte_pos = 1  

    for line_num, raw_line in enumerate(lines, 1):
        line = strip_line(raw_line)
        if not line:
            continue

        label, line = parse_label(line)

        if label is not None:
            if label in labels:
                print(f"Erro: Rótulo '{label}' definido mais de uma vez (linha {line_num})")
                sys.exit(1)
            labels[label] = byte_pos

        if not line:
            continue

        parts = line.split()
        mnemonic = parts[0].upper()

        if mnemonic == 'WW':
            byte_pos += 4
        elif mnemonic in ISA:
            byte_pos += 2 if mnemonic in INSTRUCOES_COM_ARG else 1
        else:
            print(f"Erro Sintático: Mnemônico '{mnemonic}' inválido na linha {line_num}")
            sys.exit(1)

    return labels

def resolve_names(arg, labels, line_num):
    try:
        return int(arg)
    except ValueError:
        if arg in labels:
            return labels[arg]
        print(f"Erro: Rótulo '{arg}' não definido (linha {line_num})")
        sys.exit(1)

def assemble_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_filename}' não encontrado.")
        sys.exit(1)

    lines = source_code.split('\n')
    labels = find_names(lines)

    if labels:
        print("Rótulos encontrados:")
        for name, addr in sorted(labels.items(), key=lambda x: x[1]):
            print(f"  {name:<20} -> byte {addr}")

    binary = []

    for line_num, raw_line in enumerate(lines, 1):
        line = strip_line(raw_line)
        if not line:
            continue

        _, line = parse_label(line)
        if not line:
            continue

        parts = line.split()
        mnemonic = parts[0].upper()

        if mnemonic == 'WW':
            if len(parts) < 2:
                print(f"Erro: 'WW' exige um valor numérico na linha {line_num}")
                sys.exit(1)
            try:
                val = int(parts[1]) & 0xFFFFFFFF
                binary.append(val & 0xFF)
                binary.append((val >> 8) & 0xFF)
                binary.append((val >> 16) & 0xFF)
                binary.append((val >> 24) & 0xFF)
            except ValueError:
                print(f"Erro: Valor '{parts[1]}' inválido para WW na linha {line_num}")
                sys.exit(1)
            continue

        binary.append(ISA[mnemonic])

        if mnemonic in INSTRUCOES_COM_ARG:
            if len(parts) < 2:
                print(f"Erro: Instrução '{mnemonic}' exige argumento na linha {line_num}")
                sys.exit(1)
            address = resolve_names(parts[1], labels, line_num)
            binary.append(address)

    with open(output_filename, 'wb') as f:
        f.write(bytes(binary))

    print(f"Sucesso: '{input_filename}' montado em '{output_filename}' ({len(binary)} bytes).")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python assembler.py <arquivo.asm> <arquivo.bin>")
    else:
        assemble_file(sys.argv[1], sys.argv[2])