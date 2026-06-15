res        ww 0
op1        ww 3648413612
op2        ww 1017835715
mask       ww 255
curr1      ww 0
curr2      ww 0
one        ww 1
four       ww 4
count      ww 0
temp       ww 0

inicio     load x, four
           mov count, x

vec_loop   load x, op1
           and x, mask
           mov curr1, x

           load x, op2
           and x, mask
           mov curr2, x

           load x, curr1
           sub x, curr2
           jn do_swap
           goto mult_init
           
do_swap    load x, curr1
           mov temp, x
           load x, curr2
           mov curr1, x
           load x, temp
           mov curr2, x

mult_init  load x, curr2
           jz mult_done
           
mult_loop  load x, res
           add x, curr1
           mov res, x
           
           load x, curr2
           sub x, one
           mov curr2, x
           jz mult_done
           goto mult_loop

mult_done  load x, op1
           shr8
           mov op1, x
           
           load x, op2
           shr8
           mov op2, x

           load x, count
           sub x, one
           mov count, x
           jz fim
           goto vec_loop

fim        halt