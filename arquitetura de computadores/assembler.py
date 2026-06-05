import sys

# Mapeamento oficial da ISA para Opcodes
ISA = {
    'ADD': 2, 'STORE': 6, 'JMP': 9, 'JZ': 11, 'SUB': 13, 'LOAD': 20,
    'INC': 24, 'DEC': 25, 'CLEAR': 26, 'JNZ': 27, 'MOVXY': 31,
    'MOVYX': 32, 'MUL': 33, 'MOD': 36, 'GET_BYTE': 37, 'SHR_BYTE': 38, 'HALT': 255
}

INSTRUCOES_COM_ARG = {'ADD', 'STORE', 'JMP', 'JZ', 'SUB', 'LOAD', 'JNZ'}

def assemble_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo {input_filename} não encontrado.")
        sys.exit(1)

    binary = []
    lines = source_code.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.split('#')[0].strip() # Remove comentários
        if not line:
            continue
            
        parts = line.split()
        mnemonic = parts[0].upper()
        
        if mnemonic not in ISA:
            print(f"Erro Sintático: Mnemônico '{mnemonic}' inválido na linha {line_num}")
            sys.exit(1)
            
        binary.append(ISA[mnemonic])
        
        if mnemonic in INSTRUCOES_COM_ARG:
            if len(parts) < 2:
                print(f"Erro: Instrução '{mnemonic}' exige endereço na linha {line_num}")
                sys.exit(1)
            try:
                # Trata rótulos simples ou números diretos
                address = int(parts[1])
                binary.append(address)
            except ValueError:
                print(f"Erro: Endereço '{parts[1]}' inválido na linha {line_num}")
                sys.exit(1)

    # Grava os bytes diretamente no arquivo binário de saída
    with open(output_filename, 'wb') as f:
        f.write(bytes(binary))
    print(f"Sucesso: '{input_filename}' montado com sucesso em '{output_filename}' ({len(binary)} bytes).")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python assembler.py <arquivo.asm> <arquivo.bin>")
    else:
        assemble_file(sys.argv[1], sys.argv[2])