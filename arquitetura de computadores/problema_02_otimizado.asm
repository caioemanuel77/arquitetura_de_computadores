resp       ww 0
input      ww 17
word3      ww 0

numpossivel ww 0
D          ww 0
temp       ww 0
soma_acc   ww 0
zero       ww 0
um         ww 1

inicio     load x, input
           jz caso_nao_eh_primo
           sub x, um
           jz caso_nao_eh_primo

           load x, um
           add x, um
           mov D, x

verifica_primalidade load x, input
           sub x, D
           jz num_eh_primo

           load x, input
           mov temp, x

mod_loop_1 load x, temp
           sub x, D
           jz caso_nao_eh_primo
           jn prox_d_1
           mov temp, x
           goto mod_loop_1

prox_d_1   load x, D
           add x, um
           mov D, x
           goto verifica_primalidade

num_eh_primo load x, input
           add x, um
           mov numpossivel, x
           
           load x, zero
           mov soma_acc, x
           
           load x, um
           mov D, x

soma_acc_divs_loop load x, numpossivel
           sub x, D
           jz fim_prog

           load x, numpossivel
           mov temp, x

mod_loop_2 load x, temp
           sub x, D
           jz checa_divisor
           jn caso_nao_div
           mov temp, x
           goto mod_loop_2

checa_divisor load x, soma_acc
           add x, D
           mov soma_acc, x

caso_nao_div load x, D
           add x, um
           mov D, x
           goto soma_acc_divs_loop

caso_nao_eh_primo load x, input
           add x, um
           mov numpossivel, x

verifica_numpossivel load x, um
           add x, um
           mov D, x

testa_primalidade_numpossivel load x, numpossivel
           sub x, D
           jz acha_prox_primo

           load x, numpossivel
           mov temp, x

mod_loop_3 load x, temp
           sub x, D
           jz numpossivel_falha
           jn numpossivel_prox_d
           mov temp, x
           goto mod_loop_3

numpossivel_prox_d load x, D
           add x, um
           mov D, x
           goto testa_primalidade_numpossivel

numpossivel_falha load x, numpossivel
           add x, um
           mov numpossivel, x
           goto verifica_numpossivel

acha_prox_primo load x, numpossivel
           mov soma_acc, x

fim_prog   load x, soma_acc
           mov resp, x
           halt