start:
tac
tcd
tac 1
tcispb
hlt

syscall:
ra1
switch {
0: sys$yield
1: sys$exit
2: sys$fork
3: sys$getPid
}
rets

u24 kmalloc_eternal(u16 size) {

rets
}

u24 kmalloc(u16 size) {

}

u24 kmalloc16() {

rets
}

u24 kmalloc32() {

rets
}

kfree(u24 ptr, u8 size) {

rets
}

struct MemReg ALIGN(16) {
u24 next_reg;
u24 prev_reg;
u16 phys_start;
u16 start;
u16 end;
}

u8 File::write(u24 this, u24 ptr, u8 count);
u8 File::read(u24 this, u24 ptr, u8 count);
File::move(u24 this, u16 pos);
u24 File::dup(u24 this);
File::close(u24 this);

struct File {
u24 write;
u24 read;
u24 move;
u24 dup;
u24 close;
}

struct ProcS ALIGN(32) {
u120 fmemreg;
u40 fdvec;
u16 uid;
u8 prio;
}

struct Proc ALIGN(32) {
u24 SP;
u16 FP;
u16 ret;
u24 ra;
u8 r7;
u8 r6;
u8 r5;
u8 r4;
u8 r3;
u8 r2;
u8 r1;
u8 PCB;
u8 PCH;
u8 rC;
u8 S;
u24 PC;
u24 next_proc;
u16 pid;
u24 state;
}

sys$exit:
tbc
tcrab
tcral
tbc $80
tcrah
tbc 1
tcm 1
tcral
tma
tbc 2
tcral
ra6
tma
tbc 3
tmc
tcrab
tac
tcrah
ra7
add Proc::pid
tcral
tbm
add Proc::pid+1
tcral
tbm

sys$yield:
;;if (--g_rt) return;
tbc
tcrab
tcral
tbc $80
tcrah
tma
sub 1
tcm
seq
ret
;;Proc *p = g_proc;
tbc 1
tcral
tma
ra6
tbc 2
tcral
tma

tbc 3
tcral
tmc
;;Proc *n = p->next_proc;
tcrab
tac
tcrah
ra7
add Proc::next_proc+2
tcral
;r1-3=n
ra1
tma
ra7
add Proc::next_proc+1
ra2
tma
ra7
add Proc::next_proc
ra3
tma
;;ProcS *s = n->state;
;r4-6=s
add Proc::state
ra6
pha
;;while (!n->pid) {
;;s = n->state;
;;~sPtrVec(s+ProcS::fdvec);
;;// free memreg
;;n = n->next_proc;
;;p->next_proc = n;
;;}
;;phf();
phf
;;// push SP
tsplc
phc
tsphc
phc
tspbc
phc
;;// copy stack to p
;;g_proc = n;
;;g_rt = s->prio;
;;// read SP from n
;;// copy n to stack
;;plc();
plc
;;plc();
plc
;;plc();
plc
;;plf();
plf
;;return;
ret

sys$getPid:
tbc g_procB
tcrab
tbc g_procH
tcrah
tbc g_procL
tcral
tma
tbc g_procL+1
ra6
tma
tbc g_procL+2
tmc
tcrab
tac
tcrah
ra7
add Proc::pid
tcral
ra6
tma
taspb 10
ra7
add Proc::pid+1
tcral
tma
taspb 11
rets

.org $008000
globals:
g_rt:
u8;
g_proc:
u24;
g_npid:
u16;