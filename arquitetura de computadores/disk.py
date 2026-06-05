import memory

def read(filename):
    """
    Abre o arquivo binário compilado pelo assembler (.bin)
    e injeta o seu conteúdo sequencialmente na memória RAM
    a partir do endereço 1 (conforme o padrão do computador avaliador).
    """
    try:
        with open(filename, 'rb') as f:
            binary_data = f.read()
        
        current_address = 1
        for byte in binary_data:
            memory.write_byte(current_address, byte)
            current_address += 1
            
    except FileNotFoundError:
        print(f"Erro no Disco: O arquivo binário '{filename}' não foi encontrado.")
        import sys
        sys.exit(1)