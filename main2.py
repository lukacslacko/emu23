debug = False
ram = [0]*0x100000
rom = [0]*0x40000
def read(addr, isProg=False):
  return 0xff
def write(addr, data):
  raise Exception('')
def breakpoint():
  global debug
  debug=True
def hexpad(n,l):
  return hex(n)[2:].zfill(l)
def printdebug():
  print('CZI='+str(+flagC)+str(+flagZ)+str(+flagI)+' PC='+hexpad(PC,6)+' PCB='+hexpad(PCB,2)+' PCH='+hexpad(PCH,2)+' RA='+hexpad(RA,6)+' SP='+hexpad(SP,4)+' FP='+hexpad(FP,4)+' r1='+hexpad(r1,2)+' r2='+hexpad(r2,2)+' r3='+hexpad(r3,2)+' r4='+hexpad(r4,2)+' r5='+hexpad(r5,2)+' r6='+' r7='+hexpad(r7,2)+' A='+['zero/imm','r1','r2','r3','r4','r5','r6','r7'][rA]+' B='+['zero/imm','r1','r2','r3','r4','r5','r6','r7'][rB]+' C='+hexpad(rC,2)+' interrupt='+hexpad(intc,2)+' dev='+devnames[rD]+' halted='+str(halted), end='')
devnames=['`invalid device('+hexpad(dn,2)+')1' for dn in range(256)]
devnames[0]='`null device(00)`'
devnames[1]='`left fifo(01)`'
devnames[2]='`right fifo(02)`'
devnames[3]='`timer low(03)`'
devnames[4]='`timer high(04)`'

stack = [0]*0x4000
intstack = [0]*0x4000
flagC=False
flagZ=False
PC=0x000000
PCB=0
PCH=0
RA=0x000000
SP=0x0000
FP=0x0000
r0=0
r1=0
r2=0
r3=0
r4=0
r5=0
r6=0
r7=0
rA=0
rB=0
flagI=False
rC=0
intc=0
halted=False
rD=0
fifo0=[]
fifo1=[]
fifo_size=16
div1=0
div2=0
t1=0
t2=0
timer_expired=False

def canreaddev():
  if rD==0:
    return True
  if rD==1:
    return len(fifo1)>0
  if rD==2:
    return len(fifo0)>0
  if rD==3:
    return True
  if rD==4:
    return True
  return False
def canwritedev():
  if rD==0:
    return True
  if rD==1:
    return len(fifo0)<fifo_size
  if rD==2:
    return len(fifo1)<fifo_size
  if rD==3:
    return True
  if rD==4:
    return True
  return False
def writedev(data):
  global fifo0,fifo1,t1,t2
  if rD==0:
    return
  if rD==1:
    if canwritedev():
      fifo0.append(data)
    if len(fifo0)==fifo_size:
      interrupt(3)
    return
  if rD==2:
    if canwritedev():
      fifo1.append(data)
    if len(fifo1)==fifo_size:
      interrupt(4)
    return
  if rD==3:
    div1=data
    t1=0
    return
  if rD==4:
    div2=data
    t2=0
  interrupt(2,True)
def readdev():
  global fifo0,fifo1
  if rD==0:
    return 0
  if rD==1:
    if len(fifo1)==0:
      interrupt(5)
      return 0
    q=fifo1.pop(0)
    if len(fifo1)==0:
      interrupt(5)
    return q
  if rD==2:
    if len(fifo0)==0:
      interrupt(6)
      return 0
    q=fifo0.pop(0)
    if len(fifo1)==0:
      interrupt(6)
    return q
  if rD==3:
    return t1
  if rD==4:
    return t2
  interrupt(2,True)
def interrupt(c=0xff,haltininterrupt=False):
  global intc,flagI,PC,halted
  breakpoint()
  if flagI:
    if haltininterrupt:
      halted=True
      breakpoint()
    return
  intc=1
  flagI=True
  push(PC&0xff)
  push((PC>>8)&0xff)
  push(PC>>16)
  PC=0x80
  return
def reset():
  global PC,flagI
  PC=0
  flagI=True
def getAB():
  return ([r0,r1,r2,r3,r4,r5,r6,r7][rA],[r0,r1,r2,r3,r4,r5,r6,r7][rB])
def getImm():
  global r0,PC
  r0=read(PC,False)
  PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
  return getAB()
def setA(val):
  global r1,r2,r3,r4,r5,r6,r7
  if rA==1:
    r1=val
  if rA==2:
    r2=val
  if rA==3:
    r3=val
  if rA==4:
    r4=val
  if rA==5:
    r5=val
  if rA==6:
    r6=val
  if rA==7:
    r7=val
def setB(val):
  global r1,r2,r3,r4,r5,r6,r7
  if rB==1:
    r1=val
  if rB==2:
    r2=val
  if rB==3:
    r3=val
  if rB==4:
    r4=val
  if rB==5:
    r5=val
  if rB==6:
    r6=val
  if rB==7:
    r7=val
def push(val):
  global stack,SP,intstack
  SP=(SP-1)&0x3fff
  if flagI:
    intstack[SP]=val
  else:
    stack[SP]=val
def pop():
  global SP,stack,intstack
  if flagI:
    val=intstack[SP]
  else:
    val=stack[SP]
  SP=(SP+1)&0x3fff
  return val
def doInst():
  global stack,intstack,flagC,flagZ,PC,PCB,PCH,RA,SP,FP,r0,r1,r2,r3,r4,r5,r6,r7,rA,rB,flagI,rC,intc,halted,rD
  if halted:
    return
  r0=0
  inst=read(PC,True)
  PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
  if inst==0:#rA0
    rA=0
    return
  if inst==1:#rA1
    rA=1
    return
  if inst==2:#rA2
    rA=2
    return
  if inst==3:#rA3
    rA=3
    return
  if inst==4:#rA4
    rA=4
    return
  if inst==5:#rA5
    rA=5
    return
  if inst==6:#rA6
    rA=6
    return
  if inst==7:#rA7
    rA=7
    return
  if inst==8:#rB0
    rB=0
    return
  if inst==9:#rB1
    rB=1
    return
  if inst==10:#rB2
    rB=2
    return
  if inst==11:#rB3
    rB=3
    return
  if inst==12:#rB4
    rB=4
    return
  if inst==13:#rB5
    rB=5
    return
  if inst==14:#rB6
    rB=6
    return
  if inst==15:#rB7
    rB=7
    return
  if inst==16:#ADD
    A,B=getAB()
    rC=A+B
    flagC=rC>255
    rC&=255
    flagZ=rC==0
    return
  if inst==17:#ADDi
    A,B=getImm()
    rC=A+B
    flagC=rC>255
    rC&=255
    flagZ=rC==0
    return
  if inst==18:#ADC
    A,B=getAB()
    rC=A+B+flagC
    flagC=rC>255
    rC&=255
    flagZ=rC==0
    return
  if inst==19:#ADCi
    A,B=getImm()
    rC=A+B+flagC
    flagC=rC>255
    rC&=255
    flagZ=rC==0
    return
  if inst==20:#SUB
    A,B=getAB()
    rC=A-B
    flagC=rC<0
    rC&=255
    flagZ=rC==0
    return
  if inst==21:#SUBi
    A,B=getImm()
    rC=A-B
    flagC=rC<0
    rC&=255
    flagZ=rC==0
    return
  if inst==22:#SBC
    A,B=getAB()
    rC=A-B-flagC
    flagC=rC<0
    rC&=255
    flagZ=rC==0
    return
  if inst==23:#SBCi
    A,B=getImm()
    rC=A-B-flagC
    flagC=rC<0
    rC&=255
    flagZ=rC==0
    return
  if inst==24:#OR
    A,B=getAB()
    rC=A|B
    flagZ=rC==0
    return
  if inst==25:#ORi
    A,B=getImm()
    rC=A|B
    flagZ=rC==0
    return
  if inst==26:#XOR
    A,B=getAB()
    rC=A^B
    flagZ=rC==0
    return
  if inst==27:#XORi
    A,B=getImm()
    rC=A^B
    flagZ=rC==0
    return
  if inst==28:#AND
    A,B=getAB()
    rC=A&B
    flagZ=rC==0
    return
  if inst==29:#ADNi
    A,B=getImm()
    rC=A&B
    flagZ=rC==0
    return
  if inst==30:#TCA
    setA(rC)
    return
  if inst==31:#TCB
    setB(rC)
    return
  if inst==32:#PHF
    push(FP&0xff)
    push(FP&0x3f00)
    FP=SP
    return
  if inst==33:#PLF
    SP=FP
    FP=(pop()&0x3f)<<8
    FP|=pop()
    return
  if inst==34:#TAB
    A,B=getAB()
    setB(A)
    return
  if inst==35:#TABi
    A,B=getImm()
    setB(A)
    return
  if inst==36:#TBA
    A,B=getAB()
    setA(B)
    return
  if inst==37:#TBAi
    A,B=getImm()
    setA(B)
    return
  if inst==38:#PHA
    A,B=getAB()
    push(A)
    return
  if inst==39:#PLA
    setA(pop())
    return
  if inst==40:#PHB
    A,B=getAB()
    push(B)
    return
  if inst==41:#PLB
    setB(pop())
    return
  if inst==42:#PHC
    push(rC)
    return
  if inst==43:#PLC
    rC=pop()
  if inst==44:#PHS
    push(rA<<5|rB<<2|flagC<<1|flagZ)
    flagC=False
    flagZ=False
    return
  if inst==45:#PLS
    S=pop()
    flagZ=(S&1)==1
    flagC=(S&2)==2
    rB=(S>>2)&7
    rA=S>>5
    return
  if inst==46:#SHR
    A,B=getAB()
    rC=A>>1
    flagC=(A&1)==1
    flagZ=rC==0
    return
  if inst==47:#ROR
    A,B=getAB()
    rC=A>>1|flagC<<7
    flagC=(A&1)==1
    flagZ=rC==0
    return
  if inst==48:#TCRAB
    RA=(RA&0xffff)|rC<<16
    return
  if inst==49:#TRABC
    rC=RA>>16
    return
  if inst==50:#TCRAH
    RA=(RA&0xff00ff)|rC<<8
    return
  if inst==51:#TRAHC
    rC=(RA>>8)&0xff
    return
  if inst==52:#TCRAL
    RA=(RA&0xffff00)|rC
    return
  if inst==53:#TRALC
    rC=RA&0xff
    return
  if inst==54:#TCPCB
    PCB=rC
    return
  if inst==55:#TCPCH
    PCH=rC
    return
  if inst==56:#JMPS
    PC=(PC&0xff0000)|PCH<<8|rC
  if inst==57:#JMPL
    PC=rC|PCH<<8|PCB<<16
    return
  if inst==58:#CALLS
    push(PC&0xff)
    push((PC>>8)&0xff)
    PC=(PC&0xff0000)|PCH<<8|rC
    return
  if inst==59:#CALLL
    push(PC&0xff)
    push((PC>>8)&0xff)
    push(PC>>16)
    PC=PCB<<16|PCH<<8|rC
    return
  if inst==60:#RETS
    q=pop()
    w=pop()
    PC=(PC&0xff0000)|q<<8|w
    return
  if inst==61:#RETL
    q=pop()
    w=pop()
    e=pop()
    PC=q<<16|w<<8|e
    return
  if inst==62:#RTI
    if not flagI:
      interrupt(1)
    q=pop()
    w=pop()
    e=pop()
    PC=q<<16|w<<8|e
    flagI=False
    return
  if inst==63:#BRK
    if flagI:
      breakpoint()
    else:
      interrupt(7)
    return
  if inst==64:#SYS
    if flagI:
      halted=True
      breakpoint()
      return
    intc=0
    flagI=True
    push(PC&0xff)
    push((PC>>8)&0xff)
    push(PC>>16)
    PC=0x80
    return
  if inst==65:#NOP
    return
  if inst==66:#SCC
    if not flagC:
      PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
    return
  if inst==67:#SCS
    if flagC:
      PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
    return
  if inst==68:#SEQ
    if flagZ:
      PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
    return
  if inst==69:#SNE
    if not flagZ:
      PC=(PC&0xff0000)|(((PC&0xffff)+1)&0xffff)
    return
  if inst==70:#SICC
    if not flagC:
      PC=(PC&0xff0000)|(((PC&0xffff)+2)&0xffff)
    return
  if inst==71:#SICS
    if flagC:
      PC=(PC&0xff0000)|(((PC&0xffff)+2)&0xffff)
    return
  if inst==72:#SIEQ
    if flagZ:
      PC=(PC&0xff0000)|(((PC&0xffff)+2)&0xffff)
    return
  if inst==73:#SINE
    if not flagZ:
      PC=(PC&0xff0000)|(((PC&0xffff)+2)&0xffff)
    return
  if inst==74:#TIC
    if not flagI:
      interrupt(1)
      return
    rC=intc
    return
  if inst==75:#TMA
    setA(read(RA,False))
    return
  if inst==76:#TMB
    setB(read(RA,False))
    return
  if inst==77:#TMC
    rC=read(RA,False)
    return
  if inst==78:#TAM
    A,B=getAB()
    write(RA,A)
    return
  if inst==79:#TBM
    A,B=getAB()
    write(RA,B)
    return
  if inst==80:#TCM
    write(RA,rC)
    return
  if inst==81:#TAC
    A,B=getAB()
    rC=A
    return
  if inst==82:#TACi
    A,B=getImm()
    rC=A
    return
  if inst==83:#TBC
    A,B=getAB()
    rC=B
    return
  if inst==84:#TBCi
    A,B=getImm()
    rC=B
    return
  if inst==85:#TSBA
    A,B=getAB()
    if flagI:
      setA(intstack[(SP+B)&0x3fff])
    else:
      setA(stack[(SP+B)&0x3fff])
    return
  if inst==86:#TSBAi
    A,B=getImm()
    if flagI:
      setA(intstack[(SP+B)&0x3fff])
    else:
      setA(stack[(SP+B)&0x3fff])
    return
  if inst==87:#TCSB
    A,B=getAB()
    if flagI:
      intstack[(SP+B)&0x3fff]=rC
    else:
      stack[(SP+B)&0x3fff]=rC
    return
  if inst==88:#TCSBi
    A,B=getImm()
    if flagI:
      intstack[(SP+B)&0x3fff]=rC
    else:
      stack[(SP+B)&0x3fff]=rC
    return
  if inst==89:#TASB
    A,B=getAB()
    if flagI:
      intstack[(SP+B)&0x3fff]=A
    else:
      stack[(SP+B)&0x3fff]=A
    return
  if inst==90:#TASBi
    A,B=getImm()
    if flagI:
      intstack[(SP+B)&0x3fff]=rC
    else:
      stack[(SP+B)&0x3fff]=rC
    return
  if inst==91:#HLT
    if not flagI:
      interrupt(1)
      return
    halted=True
  if inst==92:#CMP
    A,B=getAB()
    flagZ=A==B
    flagC=B>A
  if inst==93:#CMPi
    A,B=getImm()
    flagZ=A==B
    flagC=B>A
  if inst==94:#TCD
    if flagI:
      rD=rC
      return
    interrupt(1)
    return
  if inst==95:#TDC
    rC=rD
    return
  if inst==96:#WCD
    writedev(rC)
    return
  if inst==97:#RDC
    rC=readdev()
    return
  if inst==98:#SCW
    flagC=canwritedev()
    return
  if inst==99:#SCR
    flagC=canreaddev()
    return
  if inst==100:#PHAi
    A,B=getImm()
    push(A)
    return
  if inst==101:#PHBi
    A,B=getImm()
    push(B)
    return
  interrupt(1,True)
reset()

def advance_time():
  global t1,t2,timer_expired
  t1=t1+1
  if t1>=div1:
    t1=0
    t2=t2+1
    if t2>=div2:
      t2=0
      timer_expired=True

while True:
  doInst()
  if timer_expired and not flagI:
    timer_expired=False
    interrupt(254)
  if debug:
    printdebug()
    q=input()
    if q!='':
      if q=='q':
        if halted:
          exit()
        debug=False
      if q=='c':
        halted=False
      if q=='h':
        halted=True
      if q[0]=='s':
        if q!='s':
          for i in range(int(q[1:],16)):
            print(hexpad(stack[(SP+i)&0x3fff],2),end=' ')
        print()
      if q[0]=='i':
        if q!='i':
          for i in range(int(q[1:],16)):
            print(hexpad(intstack[(SP+i)&0x3fff],2),end=' ')
        print()
      if q[0]=='e':
        exit()
