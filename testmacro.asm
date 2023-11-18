include test.macros
$nejmpl=lda%1 tas tsc pop netcpcl

$setmemaddr 128 0
$ldb 1
LDA 0
TAS
loop:
TSA
ADD
TCS
TCM
PSH
$nejmpl loopL
BRK
