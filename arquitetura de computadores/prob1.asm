# ==============================================================================
# HEADER - PROTEÇÃO DE MEMÓRIA
# ==============================================================================
JMP INICIO
CLEAR
WW 0        # Word 1 - Resposta
WW 0        # Word 2 - Entrada
WW 0        # Word 3 - Reservado

# ==============================================================================
# INÍCIO DO CÓDIGO
# ==============================================================================
INICIO:
# Constantes no final da RAM
CLEAR
STORE 108   # 0
INC
STORE 105   # 1
INC
STORE 106   # 2
INC
STORE 107   # 3

# Exceção (Entrada == 0)
LOAD 2
JZ FIM_ZERO

# Exceção (Entrada == 1)
LOAD 2
SUB 105
JZ FIM_ZERO

# Verifica Paridade (Entrada & 1 == 0)
LOAD 105
MOVXY
LOAD 2
AND
JZ CASO_PAR

# ==============================================================================
# LÓGICA ÍMPAR (Soma dos Divisores aos Pares)
# ==============================================================================
CASO_IMPAR:
LOAD 105
STORE 100     # SOMA = 1
LOAD 107
STORE 101     # Y = 3

LOOP_IMPAR:
# Condição de Parada Rápida: Y * Y > Entrada
LOAD 101
MOVXY
LOAD 101
MUL
STORE 102     # Temp = Y*Y

LOAD 2        # Entrada
SUB 102       # Entrada - Y*Y
JN FIM        # Se deu negativo (Entrada < Y*Y), Acabou!

# Verifica se Y divide a Entrada
LOAD 101
MOVXY
LOAD 2
MOD
JNZ PROX_IMPAR

# Soma Y
LOAD 100
ADD 101
STORE 100

# Previne soma duplicada se Y * Y == Entrada
LOAD 2
SUB 102       
JZ PROX_IMPAR

# Adiciona o Par (Entrada / Y)
LOAD 101
MOVXY
LOAD 2
DIV
STORE 103
LOAD 100
ADD 103
STORE 100

PROX_IMPAR:
LOAD 101
ADD 106      
STORE 101
JMP LOOP_IMPAR

# ==============================================================================
# LÓGICA PAR (Fatoração Direta Perfeita)
# ==============================================================================
CASO_PAR:
LOAD 2
STORE 110     # X = Entrada
CLEAR
STORE 100     # SOMA = 0

LOOP_DOIS:
LOAD 106
MOVXY
LOAD 110
MOD
JNZ FIM_DOIS

# SOMA += 2
LOAD 100
ADD 106
STORE 100

# X = X / 2
LOAD 106
MOVXY
LOAD 110
DIV
STORE 110
JMP LOOP_DOIS

FIM_DOIS:
LOAD 107
STORE 101     # Y = 3

LOOP_FATORES:
# Condição de Parada Rápida: Y * Y > X
LOAD 101
MOVXY
LOAD 101
MUL
STORE 102     # Y*Y

LOAD 110      # X
SUB 102       # X - Y*Y
JN RESTO_FATOR

DIVIDE_Y:
LOAD 101
MOVXY
LOAD 110
MOD
JNZ PROX_FATOR

# É fator primo! SOMA += Y
LOAD 100
ADD 101
STORE 100

LOAD 101
MOVXY
LOAD 110
DIV
STORE 110
JMP DIVIDE_Y  # Repete o teste para o MESMO fator primo!

PROX_FATOR:
LOAD 101
ADD 106       # Y += 2
STORE 101
JMP LOOP_FATORES

RESTO_FATOR:
# Soma a sobra se X > 1
LOAD 110
SUB 105
JZ FIM
LOAD 100
ADD 110
STORE 100
JMP FIM

# ==============================================================================
# FINALIZAÇÃO
# ==============================================================================
FIM_ZERO:
LOAD 108
STORE 100

FIM:
LOAD 100
STORE 1
HALT