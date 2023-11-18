exit()
from comp import build
from preproc import preproc

ram = [0]*0x8000
rom = [0]*0x4000
#TODO: load rom
regA=0
regB=0
regC=0
PC=0xC000
PCH=0xC0
RA=0
stack = [0]*0x4000
SP=0
C=False
Z=False
runClock = True
debug = False
def read(addr):
  if addr>=0x0000 and addr<=0x7FFF:
    return ram[addr]
  if addr>=0xC000 and addr<=0xFFFF:
    return rom[addr-0xC000]
  raise Exception('invalid read addr: '+hex(addr))
def write(addr, data):
  global ram
  if addr==0x8000:
    print(data)
    print(chr(data),end='')
    return
  if addr>=0x0000 and addr<=0x7FFF:
    ram[addr]=data
    return
  raise Exception('invalid write addr: '+hex(addr))
def doInst():
  global regA,regB,regC,PC,PCH,RA,stack,SP,C,Z,runClock,debug
  I = read(PC)
  if debug:
    input("I="+str(I>>3)+", PC="+hex(PC)+", regA="+hex(regA)+", regB="+hex(regB)+", regC="+hex(regC)+", RA="+hex(RA)+", PCH="+hex(PCH)+", S="+hex(stack[SP])+", CZ="+str(+C)+str(+Z))
  inst = I
  PC+=1
  PC&=0xFFFF
  if I&4:
    if I&2:
      if I&1:
        if not C:#111 CC
          return
      else:
        if C:#110 CS
          return
    else:
      if I&1:
        if not Z:#101 EQ
          return
      else:
        if Z:#100 NE
          return
  if I&128 and I&64:
    if I&16:
      if I&8:
        C=True
      else:
        C=False
    else:
      if I&8:
        Z=True
      else:
        Z=False
    return
  I>>=3
  if I==0:#NOP
    return
  if I==1:#BRK
    runClock = False
    return
  if I==2:#PSH
    SP+=1
    SP&=0x3FFF
    return
  if I==3:#POP
    SP-=1
    SP&=0x3FFF
    return
  if I==4:#LDA
    regA=read(PC)
    PC+=1
    PC&=0xFFFF
    return
  if I==5:#ROR
    regC=C<<7|regA>>1
    C=regA&1==1
    Z=regC==0
    return
  if I==6:#TAS
    stack[SP]=regA
    return
  if I==7:#TBS
    stack[SP]=regB
    return
  if I==8:#TCS
    stack[SP]=regC
    return
  if I==9:#TSA
    regA=stack[SP]
    return
  if I==10:#TSB
    regB=stack[SP]
    return
  if I==11:#TSC
    regC=stack[SP]
    return
  if I==12:#TCRAH
    RA&=0xFF
    RA|=regC<<8
    return
  if I==13:#TCRAL
    RA&=0xFF00
    RA|=regC
    return
  if I==14:#TCPCH
    PCH=regC
    return
  if I==15:#TCPCL
    PC=PCH<<8|regC
    return
  if I==16:#ADD
    regC=regA+regB+C
    C=regC>>8==1
    regC&=0xFF
    Z=regC==0
    return
  if I==17:#SUB
    regC=regA-regB-C
    C=regC<0
    regC&=0xFF
    Z=regC==0
    return
  if I==18:#OR
    regC=regA|regB
    Z=regC==0
    return
  if I==19:#AND
    regC=regA&regB
    Z=regC==0
    return
  if I==20:#XOR
    regC=regA^regB
    Z=regC==0
    return
  if I==21:#TMA
    regA=read(RA)
    return
  if I==22:#TCM
    write(RA,regC)
    return
  if I==23:#DEBUG
    debug=True
    return
  raise Exception('invalid instruction: '+hex(inst))
def run():
  while runClock:
    doInst()

f = open('test.asm','r')
lines = f.read().split('\n')
f.close()

build(preproc(lines), rom)

run()
# for i in range(SP):
#   print(hex(stack[i])[2:], end=' ')
# print()
# debug = True
# while True:
#   runClock = True
#   run()