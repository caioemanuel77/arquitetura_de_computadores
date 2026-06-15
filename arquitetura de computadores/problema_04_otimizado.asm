saida         ww 0
entrada       ww 3648413612
word3         ww 0
b0            ww 0
b1            ww 0
b2            ww 0
b3            ww 0
temp          ww 0
res           ww 0
mask_ff       ww 255
one           ww 1
eight         ww 8

inicio        load x, entrada
              and x, mask_ff
              mov b0, x
              
              load x, entrada
              shr8
              mov temp, x
              and x, mask_ff
              mov b1, x
              
              load x, temp
              shr8
              mov temp, x
              and x, mask_ff
              mov b2, x
              
              load x, temp
              shr8
              and x, mask_ff
              mov b3, x

              load x, b3
              sub x, b2
              jn next1
              load x, b3
              mov temp, x
              load x, b2
              mov b3, x
              load x, temp
              mov b2, x

next1         load x, b1
              sub x, b0
              jn next2
              load x, b1
              mov temp, x
              load x, b0
              mov b1, x
              load x, temp
              mov b0, x

next2         load x, b3
              sub x, b1
              jn next3
              load x, b3
              mov temp, x
              load x, b1
              mov b3, x
              load x, temp
              mov b1, x

next3         load x, b2
              sub x, b0
              jn next4
              load x, b2
              mov temp, x
              load x, b0
              mov b2, x
              load x, temp
              mov b0, x

next4         load x, b2
              sub x, b1
              jn next5
              load x, b2
              mov temp, x
              load x, b1
              mov b2, x
              load x, temp
              mov b1, x

next5         load x, b3
              mov res, x
              
              load x, eight
              mov temp, x
shl1          load x, res
              add x, res
              mov res, x
              load x, temp
              sub x, one
              mov temp, x
              jz end_shl1
              goto shl1
              
end_shl1      load x, res
              add x, b2
              mov res, x
              
              load x, eight
              mov temp, x
shl2          load x, res
              add x, res
              mov res, x
              load x, temp
              sub x, one
              mov temp, x
              jz end_shl2
              goto shl2
              
end_shl2      load x, res
              add x, b1
              mov res, x
              
              load x, eight
              mov temp, x
shl3          load x, res
              add x, res
              mov res, x
              load x, temp
              sub x, one
              mov temp, x
              jz end_shl3
              goto shl3
              
end_shl3      load x, res
              add x, b0
              mov saida, x
              halt