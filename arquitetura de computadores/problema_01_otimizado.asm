saida         ww 0
entrada_unica ww 55
word3         ww 0
soma          ww 0
D             ww 0
numprovis     ww 0
temp          ww 0
quociente     ww 0
zero          ww 0
one           ww 1
two           ww 2
mask_1        ww 1

inicio       load x, entrada_unica
             jz fim_prog  
             jn fim_prog    

             and x, mask_1
             jz eh_par
             goto eh_impar

eh_impar     load x, zero
             mov soma, x
             load x, one
             mov D, x       

loop_odd     load x, entrada_unica
             sub x, D
             jz fim_prog
             jn fim_prog    

             load x, entrada_unica
             mov temp, x     

mod_im_loop  load x, temp
             sub x, D
             jz eh_div_impar 
             jn nao_div_impar
             mov temp, x
             goto mod_im_loop

eh_div_impar load x, soma
             add x, D
             mov soma, x

nao_div_impar load x, D
             add x, two
             mov D, x       
             goto loop_odd

eh_par       load x, zero
             mov soma, x
             load x, entrada_unica
             mov numprovis, x  

tira_dois    load x, numprovis
             and x, mask_1
             jz divide_por_dois
             goto setup_impares

divide_por_dois load x, numprovis
             shr1
             mov numprovis, x
             load x, soma
             add x, two
             mov soma, x
             
             load x, numprovis
             sub x, one
             jz fim_prog
             goto tira_dois

setup_impares load x, one
             add x, two
             mov D, x

tenta_div    load x, numprovis
             sub x, one
             jz fim_prog

             load x, numprovis
             mov temp, x
             load x, zero
             mov quociente, x

div_loop     load x, temp
             sub x, D
             jz exata   
             jn falhou 
             mov temp, x
             load x, quociente
             add x, one
             mov quociente, x 
             goto div_loop

exata        load x, quociente
             add x, one
             mov numprovis, x 
             load x, soma
             add x, D
             mov soma, x
             goto tenta_div

falhou       load x, D
             add x, two
             mov D, x     
             goto tenta_div

fim_prog     load x, soma
             mov saida, x
             halt