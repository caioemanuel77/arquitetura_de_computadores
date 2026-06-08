# ==============================================================================
# PROB3 - PRODUTO ESCALAR (ALINHAMENTO CORRIGIDO)
# ==============================================================================
JMP INICIO

# Força o alinhamento correto das Words exigido pelo memory.py e computador.py
WW 0        # WORD 1 (Endereço lógico 1) -> Saída do Resultado
WW 0        # WORD 2 (Endereço lógico 2) -> Entrada A (Vetor A)
WW 0        # WORD 3 (Endereço lógico 3) -> Entrada B (Vetor B)

INICIO:
# 1. Inicialização de Constantes na Memória Alta (longe do cabeçalho)
CLEAR
STORE 108   # [108] = Constante 0
INC
STORE 105   # [105] = Constante 1

# 2. Inicialização do Acumulador do Produto Escalar
CLEAR
STORE 100   # [100] = SOMA ACUMULADA TOTAL = 0

# 3. Faz cópia de segurança das entradas para as variáveis locais
LOAD 2
STORE 110   # [110] = VETOR A VIVO

LOAD 3
STORE 120   # [120] = VETOR B VIVO

# ==============================================================================
# ELEMENTO 0 (Byte menos significativo)
# ==============================================================================
LOAD 110
GET_BYTE    # Captura apenas os 8 bits inferiores de A
STORE 111   # Guarda temporariamente

LOAD 120
GET_BYTE    # Captura apenas os 8 bits inferiores de B
MOVXY       # Move o fator B para o registrador Y

LOAD 111    # Recupera o fator A no Acumulador
MUL         # Acumulador = A[0] * B[0]
ADD 100     # Soma com o total acumulado
STORE 100

# ==============================================================================
# ELEMENTO 1 (Byte 1)
# ==============================================================================
LOAD 110
SHR_BYTE    # Desloca 8 bits para a direita (descarta o Byte 0 de A)
STORE 110

LOAD 120
SHR_BYTE    # Desloca 8 bits para a direita (descarta o Byte 0 de B)
STORE 120

LOAD 110
GET_BYTE
STORE 111

LOAD 120
GET_BYTE
MOVXY

LOAD 111
MUL         # Acumulador = A[1] * B[1]
ADD 100
STORE 100

# ==============================================================================
# ELEMENTO 2 (Byte 2)
# ==============================================================================
LOAD 110
SHR_BYTE    # Desloca mais 8 bits para a direita
STORE 110

LOAD 120
SHR_BYTE    # Desloca mais 8 bits para a direita
STORE 120

LOAD 110
GET_BYTE
STORE 111

LOAD 120
GET_BYTE
MOVXY

LOAD 111
MUL         # Acumulador = A[2] * B[2]
ADD 100
STORE 100

# ==============================================================================
# ELEMENTO 3 (Byte mais significativo)
# ==============================================================================
LOAD 110
SHR_BYTE    # Desloca os últimos 8 bits
STORE 110

LOAD 120
SHR_BYTE
STORE 120

LOAD 110
GET_BYTE
STORE 111

LOAD 120
GET_BYTE
MOVXY

LOAD 111
MUL         # Acumulador = A[3] * B[3]
ADD 100
STORE 100

# ==============================================================================
# ESCRITA DO RESULTADO FINAL NA WORD 1 E DESLIGAMENTO
# ==============================================================================
LOAD 100    # Recupera o total acumulado do produto escalar
STORE 1     # Grava na WORD 1 (onde o computador.py espera ler a saída)
HALT        # Para a CPU de forma correta e segura