.org 0
reset:
rb0
tbc
tcpcb
tbc startH
tcpch
tbc startL
jmps
hlt

.org $80
int:
phs
phc
tpchc
phc
tpcbc
phc
ra1
pha
ra2
pha
ra3
pha
ra4
pha
ra5
pha
ra6
pha
ra7
pha
tralc
phc
trahc
phc
trabc
phc
rb0
tbc
tcpcb
tcpch
tbc l1L
calls
;stack : PCl PCh PCb S C PCH PCB r1 r2 r3 r4 r5 r6 r7 RAl RAh RAb RETl RETh
plc
tcrab
plc
tcrah
plc
tcral
ra7
pla
ra6
pla
ra5
pla
ra4
pla
ra3
pla
ra2
pla
ra1
pla
plc
tcpcb
plc
tcpch
plc
pls
rti
l1:
tic
tca

;syscall
cmp 0
tbc syscallH
tcpch
tbc syscallL
sne
jmps

;illegal instruction
cmp 1
tbc sys$exitH
tcpch
tbc sys$exitL
tcpcl
sne
jmps

;breakpoint
cmp 2

;segmentation fault x
cmp 3

;segmentation fault r
cmp 4

;segmentation fault w
cmp 5

;timer interrupt
cmp $80
tbc sys$yieldH
tcpch
tbc sys$yieldL
sne
jmps

rets