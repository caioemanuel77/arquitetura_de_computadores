# ==============================================================================
# PROB1 - SOMA DOS FATORES PRIMOS DISTINTOS (RESILIENTE A ENTRADAS EXTREMAS)
# SE PAR: APENAS BASES DOS FATORES PRIMOS
# SE ÍMPAR: BASES DOS FATORES PRIMOS + NÚMERO 1
# ==============================================================================
JMP INICIO

WW 0        # WORD 1 (Bytes 4-7)   -> Resposta enviada ao avaliador
WW 0        # WORD 2 (Bytes 8-11)  -> Entrada (X) injetada pelo servidor

INICIO:
# 1. Inicialização de Constantes na Memória
CLEAR
STORE 108   # [108] = 0
INC
STORE 105   # [105] = 1
INC
STORE 106   # [106] = 2

# 2. Inicialização de Variáveis de Trabalho
CLEAR
STORE 100   # [100] = SOMA ACUMULADA TOTAL = 0

LOAD 2      # Carrega o valor X da Word 2
STORE 110   # [110] = DIVIDENDO VIVO (X)

# Caso Fronteira: Se X <= 1, não possui fatores válidos. Fim direto.
SUB 105     # X - 1
JN FIM_PROGRAMA
JZ FIM_PROGRAMA

# ==============================================================================
# ANÁLISE DE PARIDADE DO NÚMERO ORIGINAL
# ==============================================================================
LOAD 106
MOVXY       # Y = 2
LOAD 110    # X original
MOD         # X % 2
JNZ FLUXO_IMPAR # Se resto for 1, pula para a lógica de números ímpares

# ==============================================================================
# [FLUXO PAR] -> Fatoração Clássica do Número 2
# ==============================================================================
LOAD 100
ADD 106     # Adiciona o fator primo 2 uma única vez
STORE 100

REDUZ_DOIS:
LOAD 106
MOVXY       # Y = 2
LOAD 110    # X
DIV         # X / 2
STORE 110   # X = X / 2

# Verifica se o novo X ainda é divisível por 2
LOAD 106
MOVXY
LOAD 110
MOD
JZ REDUZ_DOIS # Enquanto for par, continua dividindo por 2 para reduzir X

JMP PREPARA_DIVISORES_IMPARES

# ==============================================================================
# [FLUXO ÍMPAR] -> Adiciona o 1 Conforme Especificação
# ==============================================================================
FLUXO_IMPAR:
LOAD 100
ADD 105     # Soma obrigatoriamente o número 1
STORE 100

# ==============================================================================
# FATORAÇÃO SEQUENCIAL DOS CANDIDATOS ÍMPARES (3, 5, 7, 9, 11...)
# ==============================================================================
PREPARA_DIVISORES_IMPARES:
LOAD 105
ADD 106
STORE 101   # [101] = DIVISOR VIVO (Y = 3)

LOOP_FATORACAO:
# Condição de Saída Matemática Segura: se (X / Y) < Y, significa que Y * Y > X.
# Se passamos da raiz quadrada de X e o número não foi dividido, o que restou é primo!
LOAD 101
MOVXY       # Y
LOAD 110    # X
DIV         # X / Y
SUB 101     # (X / Y) - Y
JN ANALISA_RESIDUO # Se deu negativo, Y ultrapassou a raiz de X. Loop encerrado!

# Teste de divisibilidade: X % Y
LOAD 101
MOVXY       # Y
LOAD 110    # X
MOD         # X % Y
JNZ PROXIMO_DIVISOR # Se o resto não for 0, pula para o próximo número da lista

# Sucesso! Encontramos um fator primo distinto. Acumula ele uma única vez.
LOAD 100
ADD 101
STORE 100

REDUZ_X_PELO_FATOR:
LOAD 101
MOVXY       # Y
LOAD 110    # X
DIV         # X / Y
STORE 110   # X = X / Y

# Checa se o X que sobrou ainda consegue ser dividido pelo mesmo Y
LOAD 101
MOVXY
LOAD 110
MOD
JZ REDUZ_X_PELO_FATOR # Drena totalmente as repetições desse fator primo

PROXIMO_DIVISOR:
LOAD 101
ADD 106
STORE 101   # Y = Y + 2 (Avança para o próximo ímpar: 3 -> 5 -> 7...)
JMP LOOP_FATORACAO

# ==============================================================================
# ANÁLISE DO RESÍDUO FINAL DE X
# ==============================================================================
ANALISA_RESIDUO:
# Se após reduzir o número por todos os divisores o X atual for maior que 1,
# significa que o valor restante é, por si só, um fator primo (o maior deles).
LOAD 110
SUB 105     # X - 1
JN FIM_PROGRAMA
JZ FIM_PROGRAMA

# Adiciona esse fator primo restante na soma final
LOAD 100
ADD 110
STORE 100

# ==============================================================================
# GRAVAÇÃO DO RESULTADO E DESLIGAMENTO
# ==============================================================================
FIM_PROGRAMA:
LOAD 100    # Pega o total acumulado da soma
STORE 1     # Escreve na Word 1 (Onde o corretor vai ler)
HALT