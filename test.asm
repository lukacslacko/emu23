include stdlib.asm
LDA ret1L
TAS
PSH
LDA ret1H
TAS
PSH
LDA 1
TAS
PSH
TAS
PSH
LDA str1L
TAS
PSH
LDA str1H
TAS
PSH
$jump strcpyH strcpyL
ret1:
LDA ret2L
TAS
PSH
LDA ret2H
TAS
PSH
LDA 1
TAS
PSH
TAS
PSH
LDA str2L
TAS
PSH
LDA str2H
TAS
PSH
$jump strcatH strcatL
ret2:
LDA ret3L
TAS
PSH
LDA ret3H
TAS
PSH
LDA 1
TAS
PSH
TAS
PSH
$jump printH printL
ret3:
LDA ret4L
TAS
PSH
LDA ret4H
TAS
PSH
$jump rand8H rand8L
ret4:
LDA 128
TAS
TSC
TCRAH
LDA 0
TAS
TSC
TCRAL
TBS
TSC
TCM
$jump ret3H ret3L
str1:
.b 'H'
.b 'e'
.b 'l'
.b 'l'
.b 'o'
.b 0
str2:
.b ' '
.b 'W'
.b 'o'
.b 'r'
.b 'l'
.b 'd'
.b 10
.b 0