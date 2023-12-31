; 000000
; reset


; 000080
; interrupt
phc
phs
tpchc
phc
ra1
pha
rb0
tic
tca
phb tdL
phb tdH

; 00 syscall
tbc syscallH
tcpch
tbc syscallL
tcpcl
cmp
sne
jmps

; ?? timer
tbc timerH
tcpch
tbc timerL
tcpcl
cmp ??
sne
jmps

; 01 illegal instruction
tbc illinstH
tcpch
tbc illinstL
tcpcl
cmp $01
sne
jmps

; 02 breakpoint
tbc brkH
tcpch
tbc brkL
tcpcl
cmp $02
sne
jmps

; 03 segfault x
tbc segfxH
tcpch
tbc segfxL
tcpcl
cmp $03
sne
jmps

; 04 segfault r
tbc segfrH
tcpch
tbc segfrL
tcpcl
cmp $04
sne
jmps

; 05 segfault w
tbc segfwH
tcpch
tbc segfwL
tcpcl
cmp $05
sne
jmps

hlt
td:
ra1
pla
plc
tcpch
pls
plc
rti
syscall:
; TODO
hlt

timer:
; TODO
hlt

illinst:
segfr:
segfw:
segfx:
; TODO
hlt

brk:
sys_brk:
; TODO
brk
rets
