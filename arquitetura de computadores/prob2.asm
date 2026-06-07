# ==============================================================================
# HEADER - RESERVA OBRIGATÓRIA DAS WORDS 1, 2 E 3
# ==============================================================================
JMP INICIO

WW 0        # WORD 1 -> Resposta Final (Saída)
WW 0        # WORD 2 -> Entrada (Valor X)
WW 0        # WORD 3 -> RESERVADA / INTOCADA

INICIO:
# Inicialização ultra-rápida de constantes na memória alta
CLEAR
STORE 108   # [108] = Constante 0
INC
STORE 105   # [105] = Constante 1
INC
STORE 106   # [106] = Constante 2

CLEAR
STORE 100   # [100] = ACUMULADOR DE RESPOSTA = 0

LOAD 2      
STORE 110   # [110] = VALOR DE ENTRADA (X)

# ==============================================================================
# TESTE DE PRIMALIDADE PARA O X ORIGINAL
# ==============================================================================
# Se X <= 1, não é primo.
LOAD 110
SUB 105     # X - 1
JN ADVERSO  # Se X < 1 (0), não é primo -> vai para o "caso contrário"
JZ ADVERSO  # Se X == 1, não é primo -> vai para o "caso contrário"

# Se X == 2, é primo direto!
LOAD 110
SUB 106     # X - 2
JZ CASO_PRIMO

# Se X > 2 e for par, não é primo!
LOAD 106
MOVXY
LOAD 110
MOD
JZ ADVERSO

# Teste de divisores ímpares de 3 até raiz(X)
LOAD 105
ADD 106
STORE 101   # Y = 3 (Divisor candidato)

LOOP_TESTE_PRIMO:
LOAD 101
MOVXY
LOAD 110
DIV         # X / Y
SUB 101     # (X / Y) - Y
JN CASO_PRIMO # Se Y > X/Y, testou até a raiz e não achou divisor. É PRIMO!

LOAD 101
MOVXY
LOAD 110
MOD
JZ ADVERSO  # Se o resto for 0, achou um divisor. NÃO É PRIMO!

LOAD 101
ADD 106
STORE 101   # Y = Y + 2
JMP LOOP_TESTE_PRIMO

# ==============================================================================
# [SITUAÇÃO A]: X É PRIMO -> CALCULAR SOMA DOS DIVISORES DE (X + 1)
# ==============================================================================
CASO_PRIMO:
LOAD 110
ADD 105
STORE 120   # [120] = NÚMERO SEGUINTE (N = X + 1)

# O número 1 sempre é divisor de qualquer N > 1
LOAD 105
STORE 100   # Inicializa SOMA com 1

# Otimização por pares complementares (busca até a raiz de N)
LOAD 106
STORE 101   # Y = 2 (Primeiro divisor candidato para o número seguinte)

LOOP_DIVISORES_SEGUINTE:
LOAD 101
MOVXY
LOAD 120    # N
DIV         # N / Y
STORE 111   # [111] = Quociente complementar (Z)
SUB 101     # (N / Y) - Y
JN FIM_SUCESSO # Se Y > N/Y, passamos da raiz. Fim do cálculo!

# Testa se Y divide N
LOAD 101
MOVXY
LOAD 120
MOD
JNZ AVANCA_DIV_SEGUINTE

# Achou divisor exato! Verifica se os fatores Y e Z são iguais (raiz perfeita)
LOAD 111    # Z
SUB 101     # Z - Y
JZ ACUMULA_SINGLE_SEGUINTE

# Se forem diferentes, acumula ambos os divisores complementares
LOAD 100
ADD 101     # Adiciona Y
ADD 111     # Adiciona Z
STORE 100
JMP AVANCA_DIV_SEGUINTE

ACUMULA_SINGLE_SEGUINTE:
LOAD 100
ADD 101     # Soma apenas uma vez (Y)
STORE 100

AVANCA_DIV_SEGUINTE:
LOAD 101
INC
STORE 101   # Y = Y + 1
JMP LOOP_DIVISORES_SEGUINTE

# ==============================================================================
# [SITUAÇÃO B]: X NÃO É PRIMO -> BUSCAR O PRÓXIMO PRIMO STRICTO
# ==============================================================================
ADVERSO:
LOAD 110
INC
STORE 130   # [130] = Candidato a Próximo Primo (P = X + 1)

LOOP_BUSCA_PROXIMO:
# Se P <= 2, tratamos direto
LOAD 130
SUB 106     # P - 2
JN FORCA_DOIS  # Se P < 2, o próximo primo com certeza é 2
JZ FIM_BUSCA   # Se P == 2, achamos o primo!

# Se P > 2 e for par, pula para o próximo ímpar
LOAD 106
MOVXY
LOAD 130
MOD
JZ PROXIMO_CANDIDATO

# Teste de robustez de P (divisores ímpares de 3 até raiz(P))
LOAD 105
ADD 106
STORE 101   # Y = 3

LOOP_VALIDA_P:
LOAD 101
MOVXY
LOAD 130
DIV
SUB 101     # (P / Y) - Y
JN FIM_BUSCA # Se Y > P/Y, P é primo! Encontramos.

LOAD 101
MOVXY
LOAD 130
MOD
JZ PROXIMO_CANDIDATO # Se achou divisor, não é primo.

LOAD 101
ADD 106
STORE 101   # Y = Y + 2
JMP LOOP_VALIDA_P

PROXIMO_CANDIDATO:
LOAD 130
INC
STORE 130   # P = P + 1
JMP LOOP_BUSCA_PROXIMO

FORCA_DOIS:
LOAD 106
STORE 130
# cai no FIM_BUSCA

FIM_BUSCA:
LOAD 130
STORE 100   # A resposta passa a ser o número primo encontrado
JMP FIM_SUCESSO

# ==============================================================================
# FINALIZAÇÃO SEGURA
# ==============================================================================
FIM_SUCESSO:
LOAD 100    
STORE 1     # Descarrega o resultado final sem erros na WORD 1

FIM:
HALT
JMP FIM     # Escudo protetor contra clocks fantasmas no servidor