# ==============================================================================
# HEADER - RESERVA OBRIGATÓRIA DAS WORDS 1, 2 E 3
# ==============================================================================
JMP INICIO

WW 0        # WORD 1 -> Resposta Final
WW 0        # WORD 2 -> Entrada (Valor)


INICIO:
# Inicialização ultra-rápida de constantes na memória alta
CLEAR
STORE 108   # [108] = Constante 0
INC
STORE 105   # [105] = Constante 1
INC
STORE 106   # [106] = Constante 2

CLEAR
STORE 100   # [100] = SOMA ACUMULADA = 0

LOAD 2      
STORE 110   # [110] = DIVIDENDO VIVO (X)

# Validação inicial: X <= 1 -> Encerra imediatamente com 0
SUB 105     # X - 1
JN FIM_SUCESSO
JZ FIM_SUCESSO

# ==============================================================================
# TESTE DE PARIDADE RÁPIDO
# ==============================================================================
LOAD 106
MOVXY       # Y = 2
LOAD 110
MOD         # X % 2
JNZ FLUXO_IMPAR  # Se o resto for 1, pula direto para o fluxo ímpar

# ==============================================================================
# [FLUXO PAR] -> FATORAÇÃO PRIMA (OTIMIZADA)
# ==============================================================================
LOOP_DOIS:
# Em vez de fazer MOD e depois DIV, nós dividimos direto! 
# Se o resto (guardado no registrador pela ULA) for zero, aproveitamos o quociente.
LOAD 106
MOVXY       # Y = 2
LOAD 110
DIV         # X / 2 -> Quociente vai para o acumulador, Resto fica interno
# Salvamos o quociente temporariamente
STORE 111   

LOAD 106
MOVXY
LOAD 110
MOD         # Testa se a divisão foi exata
JNZ PREPARA_IMPARES_PRIMOS # Se deu resto, o fator 2 acabou!

# Foi exata! Acumula o 2 e atualiza X com o quociente que já calculamos
LOAD 100
ADD 106
STORE 100

LOAD 111
STORE 110   # X = X / 2 (recuperado sem refazer a divisão)
JMP LOOP_DOIS

PREPARA_IMPARES_PRIMOS:
LOAD 105
ADD 106
STORE 101   # Y = 3

LOOP_FATORES_PRIMOS:
# Condição de parada: se Y > X / Y, o X restante é primo
LOAD 101
MOVXY
LOAD 110
DIV         
SUB 101     # (X / Y) - Y
JN ADICIONA_ULTIMO_PRIMO

# Otimização de Divisão Única
LOAD 101
MOVXY
LOAD 110
DIV
STORE 111   # Armazena quociente (X / Y)

LOAD 101
MOVXY
LOAD 110
MOD         # Testa o resto
JNZ PROXIMO_PRIMO_Y

# É fator primo! Acumula Y e atualiza X com o quociente pronto
LOAD 100
ADD 101
STORE 100

LOAD 111
STORE 110
JMP LOOP_FATORES_PRIMOS

PROXIMO_PRIMO_Y:
LOAD 101
ADD 106
STORE 101   # Y = Y + 2
JMP LOOP_FATORES_PRIMOS

ADICIONA_ULTIMO_PRIMO:
# Se o que sobrou em X for > 1, ele é o último primo
LOAD 110
SUB 105     # X - 1
JZ FIM_SUCESSO
LOAD 100
ADD 110
STORE 100
JMP FIM_SUCESSO

# ==============================================================================
# [FLUXO ÍMPAR] -> SOMA DOS DIVISORES UPGRADE
# ==============================================================================
FLUXO_IMPAR:
LOAD 105
STORE 100   # O número 1 sempre é divisor. Começamos a SOMA com 1.

# Otimização matemática crucial: O maior divisor possível de um ímpar é X / 3.
# Se testarmos um candidato Y e ele for divisor, nós descobrimos DOIS divisores de uma vez:
# O próprio Y e o seu quociente complementar (X / Y)!
# Isso nos permite cortar a condição de parada na raiz quadrada (Y * Y >= X).
LOOP_DIVISORES_IMPAR:
LOAD 105
ADD 106
STORE 101   # Inicializa o divisor vivo Y = 3

LOOP_RAIZ_IMPAR:
LOAD 101
MOVXY
LOAD 110
DIV         # Calcula (X / Y)
STORE 111   # [111] = Quociente complementar (Z)
SUB 101     # (X / Y) - Y
JN FIM_SUCESSO # Se Y > X / Y, passamos da raiz quadrada. Fim imediato!

# Verifica se Y é um divisor exato
LOAD 101
MOVXY
LOAD 110
MOD
JNZ AVANCA_CANDIDATO

# É DIVISOR EXATO! 
# Vamos checar se os dois fatores achados (o divisor Y e o quociente Z) são iguais
LOAD 111     # Carrega o quociente Z
SUB 101     # Z - Y
JZ ACUMULA_SINGLE # Se forem iguais (raiz perfeita), soma apenas uma vez

# Se forem diferentes, somamos AMBOS os divisores de uma só vez!
LOAD 100
ADD 101     # Adiciona o divisor Y
ADD 111     # Adiciona o quociente complementar Z (Parceiro de divisão)
STORE 100
JMP AVANCA_CANDIDATO

ACUMULA_SINGLE:
LOAD 100
ADD 101     # Soma apenas o Y (pois Z == Y)
STORE 100

AVANCA_CANDIDATO:
LOAD 101
ADD 106
STORE 101   # Y = Y + 2
JMP LOOP_RAIZ_IMPAR

# ==============================================================================
# SALVAMENTO DO RESULTADO
# ==============================================================================
FIM_SUCESSO:
LOAD 100    
STORE 1     # Descarrega o resultado direto na WORD 1

FIM:
HALT
JMP FIM     # Escudo anti-timeout