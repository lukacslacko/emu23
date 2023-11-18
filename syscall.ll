#pragma once
#ifdef Emu23
const yield := fun() {
  asm("
ra1
tba
sys
ret");
}
const exit := fun() {
  asm("
ra1
tba 1
sys");
}
const getPid := fun(() = u16) {
  asm("
ra1
tba 3
sys
tasb 4
ra2
tasb 3
ret");
}
const fork := fun(() = u16) {
  asm("
ra1
tba 2
sys
tasb 4
ra2
tasb 3
ret");
}
#endif
#ifdef X86
const exit := fun() {
  asm("
mov AX, 1
int 0x80");
}
#endif
