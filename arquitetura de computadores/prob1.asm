# ==============================================================================
# HEADER E CONSTANTES
# ==============================================================================
JMP INICIO
CLEAR
WW 0        # Word 1 - Resposta
WW 0        # Word 2 - Entrada
WW 0        # Word 3 - Reservado

INICIO:
CLEAR
STORE 108   # 0
INC
STORE 105   # 1
INC
STORE 106   # 2

LOAD 2
STORE 110   # X = Entrada
CLEAR
STORE 100   # SOMA = 0

# Trata X <= 1
LOAD 110
SUB 105
JN FIM      # Se X < 1 (ou seja, 0), FIM
JZ FIM      # Se X == 1, FIM

# ==============================================================================
# FATORAÇÃO POR 2
# ==============================================================================
LOOP_DOIS:
LOAD 106
MOVXY
LOAD 110
MOD
JNZ SET_Y_TRES

LOAD 100
ADD 106
STORE 100

LOAD 106
MOVXY
LOAD 110
DIV
STORE 110
JMP LOOP_DOIS

# ==============================================================================
# FATORAÇÃO ÍMPARES
# ==============================================================================
SET_Y_TRES:
LOAD 105
ADD 106
STORE 101   # Y = 3

LOOP_FATORES:
# Condição de Parada Segura (Sem Overflow): Y > X / Y ---> (X / Y) - Y < 0
LOAD 101
MOVXY
LOAD 110
DIV
SUB 101
JN RESTO_FATOR

DIVIDE_Y:
LOAD 101
MOVXY
LOAD 110
MOD
JNZ PROX_FATOR

# É fator! SOMA += Y
LOAD 100
ADD 101
STORE 100

LOAD 101
MOVXY
LOAD 110
DIV
STORE 110
JMP DIVIDE_Y

PROX_FATOR:
LOAD 101
ADD 106     # Y += 2
STORE 101
JMP LOOP_FATORES

# ==============================================================================
# SOMA O RESTO (SE X > 1) E FINALIZA
# ==============================================================================
RESTO_FATOR:
LOAD 110
SUB 105
JZ FIM
LOAD 100
ADD 110
STORE 100

FIM:
LOAD 100
STORE 1
HALT