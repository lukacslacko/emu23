#include <stdlib.h>
#include <poll.h>
#include <stdio.h>
#include <termios.h>
#include <errno.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <ctime>

class CPU {
public:
  CPU(uint32_t hertz, bool d=false) {
    cycle=0;
    halted=false;
    dbg=d;
    clockrate=1000000000L/hertz;
    reset();
    ltime=0;
  }
  ~CPU() {
    ;
  }
  void run(uint32_t t) {
    if (dbg) return;
    ltime+=t;
    while (ltime>clockrate) {
      doInst();
      if (dbg) {
        break;
      }
    }
  }
  void addchar(char c) {
    Char=c;
  }
  bool interrupt(char i) {
    if (i<0) {
      return false;
    }
    if (!flagI) {
      fault(0x80+i,false,true);
    }
    return !flagI;
  }
  void reset() {
    flagI=true;
    PC=0;
    hadimm=false;
  }
  void doInst() {
    if (halted) {
      return;
    }
    r0=0;
    uint8_t inst = pread();
    PC++;
    PC&=0xffffff;
    getAB();
    cycle+=Inst(inst);
    PC&=0xffffff;
    if (hadimm) {
      cycle++;
    }
    hadimm=false;
    ltime-=cycle*clockrate;
    cycle=0;
    if (dbg) {
      debug();
    }
  }
  void debug() {
    printf("CZI=%d%d%d PC=%06x PCB=%02x PCH=%02x RA=%06x SB=%02x ISB=%02x SP=%04x FP=%04x r1=%02x r2=%02x r3=%02x r4=%02x r5=%02x r6=%02x r7=%02x A=r%d B=r%d C=%02x int=%02x halted=%d\r\n",flagC,flagZ,flagI,PC,PCB,PCH,RA,SB,ISB,SP,FP,r1,r2,r3,r4,r5,r6,r7,rA,rB,rC,intc,halted);
  }
  uint8_t rom[0x8000];
  bool dbg;
private:
  char Char;
  bool halted;
  uint32_t clockrate;
  uint8_t r0,r1,r2,r3,r4,r5,r6,r7,rC;
  uint8_t intc;
  bool flagC,flagZ,flagI;
  uint8_t PCB,PCH;
  uint16_t SP,FP;
  uint32_t PC,RA;
  uint8_t SB,ISB;
  char rA,rB;
  uint8_t A,B;
  uint8_t cycle;
  bool hadimm;
  uint32_t ltime;
  uint8_t ram0[0x4000];
  uint8_t atr[0x4000];
  uint8_t istack[0x10000];
  uint8_t ram1[0x10000];
  uint8_t ram2[0x40000];

  uint8_t Inst(uint8_t inst) {
    switch(inst){
      case 0x00://ra0
        rA=0;
        return 2;
      case 0x01://ra1
        rA=1;
        return 2;
      case 0x02://ra2
        rA=2;
        return 2;
      case 0x03://ra3
        rA=3;
        return 2;
      case 0x04://ra4
        rA=4;
        return 2;
      case 0x05://ra5
        rA=5;
        return 2;
      case 0x06://ra6
        rA=6;
        return 2;
      case 0x07://ra7
        rA=7;
        return 2;
      case 0x08://rb0
        rB=0;
        return 2;
      case 0x09://rb1
        rB=1;
        return 2;
      case 0xa://rb2
        rB=2;
        return 2;
      case 0x0b://rb3
        rB=3;
        return 2;
      case 0x0c://rb4
        rB=4;
        return 2;
      case 0x0d://rb5
        rB=5;
        return 2;
      case 0x0e://rb6
        rB=6;
        return 2;
      case 0x0f://rb7
        rB=7;
        return 2;
      case 0x10://addi
        getImm();
      case 0x11://add
        rC=A+B;
        flagZ=!rC;
        flagC=A<rC;
        return 3;
      case 0x12://adci
        getImm();
      case 0x13://adc
        {int t=(int)A+(int)B+(int)flagC;
        rC=t&0xff;
        flagZ=!rC;
        flagC=t>0xff;
        return 3;}
      case 0x14://subi
        getImm();
      case 0x15://sub
        rC=A-B;
        flagZ=!rC;
        flagC=B>A;
        return 3;
      case 0x16://sbci
        getImm();
      case 0x17://sbc
        {int t=(int)A-(int)B-(int)flagC;
        rC=t&0xff;
        flagZ=!rC;
        flagC=t<0;
        return 3;}
      case 0x18://ori
        getImm();
      case 0x19://or
        rC=A|B;
        flagZ=!rC;
        return 3;
      case 0x1a://xori
        getImm();
      case 0x1b://xor
        rC=A^B;
        return 3;
      case 0x1c://andi
        getImm();
      case 0x1d://and
        rC=A&B;
        return 3;
      case 0x1e://phf
        push(FP&0xff);
        push(FP>>8);
        FP=SP;
        return 4;
      case 0x1f://plf
        SP=FP;
        FP=(uint16_t)pop()<<8;
        FP|=pop();
        return 4;
      case 0x20://tabi
        getImm();
      case 0x21://tab
        setB(A);
        return 2;
      case 0x22://tbai
        getImm();
      case 0x23://tba
        setA(B);
        return 2;
      case 0x24://tca
        setA(rC);
        return 2;
      case 0x25://tcb
        setB(rC);
        return 2;
      case 0x26://taci
        getImm();
      case 0x27://tac
        rC=A;
        return 2;
      case 0x28://tbci
        getImm();
      case 0x29://tbc
        rC=B;
        return 2;
      case 0x2a://phai
        getImm();
      case 0x2b://pha
        push(A);
        return 2;
      case 0x2c://phbi
        getImm();
      case 0x2d://phb
        push(B);
        return 2;
      case 0x2e://phc
        push(rC);
        return 2;
      case 0x2f://pla
        setA(pop());
        return 2;
      case 0x30://plb
        setB(pop());
        return 2;
      case 0x31://plc
        rC=pop();
        return 2;
      case 0x32://phs
        push(rA<<5|rB<<2|flagC<<1|flagZ);
        return 2;
      case 0x33://pls
        {uint8_t t=pop();
        flagZ=t&1;
        flagC=t>>1&1;
        rB=t>>2&7;
        rA=t>>5;
        return 2;}
      case 0x34://shri
        getImm();
      case 0x35://shr
        rC=A>>1;
        flagC=A&1;
        flagZ=!rC;
        return 2;
      case 0x36://rori
        getImm();
      case 0x37://ror
        rC=A>>1|flagC<<7;
        flagC=A&1;
        flagZ=!rC;
        return 2;
      case 0x38://tcrab
        RA=RA&0xffff|(uint32_t)rC<<16;
        return 2;
      case 0x39://trabc
        rC=RA>>16;
        return 2;
      case 0x3a://tcrah
        RA=RA&0xff00ff|(uint32_t)rC<<8;
        return 2;
      case 0x3b://trahc
        rC=RA>>8&0xff;
        return 2;
      case 0x3c://tcral
        RA=RA&0xffff00|(uint32_t)rC;
        return 2;
      case 0x3d://tralc
        rC=RA&0xff;
        return 2;
      case 0x3e://jmps
        PC=PC&0xff0000|(uint32_t)PCH<<8|(uint32_t)rC;
        return 2;
      case 0x3f://jmpl
        PC=(uint32_t)PCB<<16|(uint32_t)PCH<<8|(uint32_t)rC;
        return 2;
      case 0x40://calls
        push(PC&0xff);
        push(PC>>8&0xff);
        PC=PC&0xff0000|(uint32_t)PCH<<8|(uint32_t)rC;
        return 4;
      case 0x41://calll
        push(PC&0xff);
        push(PC>>8&0xff);
        push(PC>>16);
        PC=(uint32_t)PCB<<16|(uint32_t)PCH<<8|(uint32_t)rC;
        return 5;
      case 0x42://rets
        PC=PC&0xff0000|(uint32_t)pop()<<8;
        PC|=(uint32_t)pop();
        return 3;
      case 0x43://retl
        PC=(uint32_t)pop()<<16;
        PC|=(uint32_t)pop()<<8;
        PC|=(uint32_t)pop();
        return 4;
      case 0x44://rti
        if (flagI) {
          PC=(uint32_t)pop()<<16;
          PC|=(uint32_t)pop()<<8;
          PC|=(uint32_t)pop();
          flagI=false;
          return 4;
        } else {
          fault(1,true);
          return 1;
        }
      case 0x45://brk
        if (!flagI) {
          fault(2,true);
          return 1;
        }
        dbg=true;
        return 2;
      case 0x46://sys
        fault(0,true);
        return 1;
      case 0x47://sicc
        if (!flagC) {
          PC+=2;
          PC&=0xffffff;
          return 3;
        }
        return 2;
      case 0x48://scc
        if (!flagC) {
          PC++;
          PC&=0xffffff;
        }
        return 2;
      case 0x49://scs
        if (flagC) {
          PC++;
          PC&=0xffffff;
        }
        return 2;
      case 0x4a://sics
        if (flagC) {
          PC+=2;
          PC&=0xffffff;
          return 3;
        }
        return 2;
      case 0x4b://sieq
        if (flagZ) {
          PC+=2;
          PC&=0xffffff;
          return 3;
        }
        return 2;
      case 0x4c://seq
        if (flagZ) {
          PC++;
          PC&=0xffffff;
        }
        return 2;
      case 0x4d://sine
        if (!flagZ) {
          PC+=2;
          PC&=0xffffff;
          return 3;
        }
        return 2;
      case 0x4e://sne
        if (!flagZ) {
          PC++;
          PC&=0xffffff;
        }
        return 2;
      case 0x4f://tic
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        rC=intc;
        return 2;
      case 0x50://tami
        getImm();
      case 0x51://tam
        write(RA,A);
        return 2;
      case 0x52://tbmi
        getImm();
      case 0x53://tbm
        write(RA,B);
        return 2;
      case 0x54://tcm
        write(RA,rC);
        return 2;
      case 0x55://tma
        setA(read(RA));
        return 2;
      case 0x56://tmb
        setB(read(RA));
        return 2;
      case 0x57://tmc
        rC=read(RA);
        return 2;
      case 0x58://hlt
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        halted=true;
        dbg=true;
        return 2;
      case 0x59://reset
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        reset();
        return 2;
      case 0x5a://cmpi
        getImm();
      case 0x5b://cmp
        flagZ=A==B;
        flagC=B>A;
        return 2;
      case 0x5c://tsbai
        getImm();
      case 0x5d://tsba
        setA(read(indstack(B)));
        return 2;
      case 0x5e://tcsbi
        getImm();
      case 0x5f://tcsb
        write(indstack(B),rC);
        return 2;
      case 0x60://tasbi
        getImm();
      case 0x61://tasb
        write(indstack(B),A);
        return 2;
      case 0x62://tsbci
        getImm();
      case 0x63://tsbc
        rC=read(indstack(B));
        return 2;
      case 0x64://nop
        return 2;
      case 0x65://tcsph
        SP=SP&0xff|(uint16_t)rC<<8;
        return 2;
      case 0x66://tcspl
        SP=SP&0xff00|(uint16_t)rC;
        return 2;
      case 0x67://tsphc
        rC=SP>>8;
        return 2;
      case 0x68://tsplc
        rC=SP&0xff;
        return 2;
      case 0x69://tcspb
        SB=rC;
        return 2;
      case 0x6a://tspbc
        rC=SB;
        return 2;
      case 0x6b://tcispb
        if (!flagI) {
          fault(1);
          return 2;
        }
        ISB=rC;
        return 2;
      case 0x6c://tispbc
        rC=ISB;
        return 2;
      case 0x6d://tcpch
        PCH=rC;
        return 2;
      case 0x6e://tcpcb
        PCB=rC;
        return 2;
      case 0x6f://tpchc
        rC=PCH;
        return 2;
      case 0x70://tpcbc
        rC=PCB;
        return 2;
      case 0x71://testi
        getImm();
      case 0x72://test
        flagZ=(A&B)==0;
	return 2;
    }
    fault(1,true);
    return 1;
  }
  uint8_t physread(uint32_t addr, bool islow=false) {
    if (islow) {
      if ((addr&0xff0000)==0) {
        if (addr<0x8000) {
          return rom[addr];
        }
        if (addr<0xc000) {
          return ram0[addr-0x8000];
        }
        return atr[addr-0xc000];
      }
    }
    if (addr>=0x000000&&addr<=0x00ffff) {
      return ram1[addr];
    }
    if (addr>=0x010000&&addr<=0x01ffff) {
      return istack[addr-0x010000];
    }
    if (addr>=0x020000&&addr<=0x05ffff) {
      return ram2[addr-0x020000];
    }
    if (addr==0x7fffff) {
      char c=Char;
      Char=0;
      return c;
    }
    fault(4,true);
    return 0;
  }
  void physwrite(uint32_t addr, uint8_t data, bool islow=false) {
    if (islow) {
      if ((addr&0xff0000)==0) {
        if (addr<0x8000) {
          fault(4,true);
          return;
        }
        if (addr<0xc000) {
          ram0[addr-0x8000]=data;
          return;
        }
        atr[addr-0xc000]=data;
        return;
      }
    }
    if (addr>=0x000000&&addr<=0x00ffff) {
      ram1[addr]=data;
      return;
    }
    if (addr>=0x010000&&addr<=0x01ffff) {
      istack[addr-0x010000]=data;
      return;
    }
    if (addr>=0x020000&&addr<=0x05ffff) {
      ram2[addr-0x020000]=data;
      return;
    }
    if (addr==0x7fffff) {
      if (data) ::write(STDOUT_FILENO, (void*)&data, 1);
      return;
    }
    fault(4,true);
  }
  uint8_t pread() {
    if (PC<0x800000) {
      if (flagI) {
        return physread(PC,true);
      } else {
        fault(3,true);
        return 0;
      }
    } else {
      uint32_t a = atr[PC>>9&0x3ffe];
      a|=(uint32_t)atr[(PC>>9&0x3ffe)+1]<<8;
      if (~a&0x2000) {
        if (!flagI) {
          fault(3,true);
          return 0;
        }
      }
      return physread(a<<10&0x7ffc00|PC&0x3ff);
    }
  }
  uint8_t read(uint32_t addr) {
    if (addr<0x800000) {
      if (flagI) {
        return physread(addr,true);
      } else {
        fault(4,true);
        return 0;
      }
    } else {
      uint32_t a = atr[addr>>9&0x3ffe];
      a|=(uint32_t)atr[(addr>>9&0x3ffe)+1]<<8;
      if (~a&0x8000) {
        if (!flagI) {
          fault(4,true);
          return 0;
        }
      }
      return physread(a<<10&0x7ffc00|addr&0x3ff);
    }
  }
  void write(uint32_t addr, uint8_t data) {
    if (addr<0x800000) {
      if (flagI) {
        physwrite(addr,data,true);
      } else {
        fault(5,true);
      }
    } else {
      uint32_t a = atr[addr>>9&0x3ffe];
      a|=(uint32_t)atr[(addr>>9&0x3ffe)+1]<<8;
      if (~a&0x4000) {
        if (!flagI) {
          fault(5,true);
        }
      }
      physwrite(a<<10&0x7ffc00|addr&0x3ff,data);
    }
  }
  void push(uint8_t data) {
    SP--;
    if (flagI) {
      write((uint32_t)ISB<<16|SP,data);
    } else {
      write((uint32_t)SB<<16|SP,data);
    }
  }
  uint8_t pop() {
    uint8_t val;
    if (flagI) {
      val=read((uint32_t)ISB<<16|(uint32_t)SP);
    } else {
      val=read((uint32_t)SB<<16|(uint32_t)SP);
    }
    SP++;
    return val;
  }
  uint32_t indstack(uint8_t ind) {
    if (flagI) {
      return (uint32_t)ISB<<16|(uint32_t)SP+(uint32_t)ind&0xffff;
    } else {
      return (uint32_t)SB<<16|(uint32_t)SP+(uint32_t)ind&0xffff;
    }
  }
  void setA(uint8_t val) {
    switch(rA){
      case 0:
        break;
      case 1:
        r1=val;
        break;
      case 2:
        r2=val;
        break;
      case 3:
        r3=val;
        break;
      case 4:
        r4=val;
        break;
      case 5:
        r5=val;
        break;
      case 6:
        r6=val;
        break;
      case 7:
        r7=val;
        break;
    }
  }
  void setB(uint8_t val) {
    switch(rB){
     case 0:
       break;
     case 1:
       r1=val;
       break;
     case 2:
       r2=val;
       break;
     case 3:
       r3=val;
       break;
     case 4:
       r4=val;
       break;
     case 5:
       r5=val;
       break;
     case 6:
       r6=val;
       break;
     case 7:
       r7=val;
       break;
    }
  }
  void getAB() {
    switch(rA){
      case 0:
        A=r0;
        break;
      case 1:
        A=r1;
        break;
      case 2:
        A=r2;
        break;
      case 3:
        A=r3;
        break;
      case 4:
        A=r4;
        break;
      case 5:
        A=r5;
        break;
      case 6:
        A=r6;
        break;
      case 7:
        A=r7;
        break;
    }
    switch(rB){
      case 0:
        B=r0;
        break;
      case 1:
        B=r1;
        break;
      case 2:
        B=r2;
        break;
      case 3:
        B=r3;
        break;
      case 4:
        B=r4;
        break;
      case 5:
        B=r5;
        break;
      case 6:
        B=r6;
        break;
      case 7:
        B=r7;
        break;
    }
  }
  void getImm() {
    hadimm=true;
    r0=pread();
    PC++;
    PC&=0xffffff;
    getAB();
  }
  void fault(uint8_t f, bool halt=false, bool iint=false) {
    if (flagI&halt) {
      dbg=true;
      halted=true;
      return;
    }
    if (flagI) {
      return;
    }
    if (!iint) {
      PC--;
      if (hadimm) {
        PC--;
      }
      PC&=0xffffff;
    }
    intc=f;
    flagI=true;
    push(PC&0xff);
    push(PC>>8&0xff);
    push(PC>>16);
    PC=0x80;
    cycle+=4;
  }
};

struct termios orig_termios;
void die(const char *s) {
  perror(s);
  exit(1);
}
void disableRawMode() {
  if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios)==-1) die("tcsetattr");
}
void enableRawMode() {
  if (tcgetattr(STDIN_FILENO, &orig_termios)==-1) die("tcgetattr");
  atexit(disableRawMode);
  struct termios raw = orig_termios;
  raw.c_iflag &= ~(IXON|ICRNL|BRKINT|ISTRIP);
  raw.c_oflag &= ~(OPOST);
  raw.c_cflag |= (CS8);
  raw.c_lflag &= ~(ECHO|ICANON|ISIG|IEXTEN);
  //raw.c_cc[VMIN] = 0;
  //raw.c_cc[VTIME] = 1;
  if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw)==-1) die("tcsetattr");
}
uint32_t d(struct timespec *nt, struct timespec *lt) {
  double secdiff = difftime(nt->tv_sec,lt->tv_sec);
  uint32_t nanodiff = nt->tv_nsec-lt->tv_nsec;
  nanodiff+=1000000000L*(uint32_t)secdiff;
  return nanodiff;
}
int main(int argc, char** argv) {
  enableRawMode();
  CPU cpu = CPU(1000000L);
  cpu.rom[0]=0x01;
  cpu.rom[1]=0x08;
  cpu.rom[2]=0x23;
  cpu.rom[3]=0x28;
  cpu.rom[4]=0x7f;
  cpu.rom[5]=0x38;
  cpu.rom[6]=0x28;
  cpu.rom[7]=0xff;
  cpu.rom[8]=0x3a;
  cpu.rom[9]=0x3c;
  cpu.rom[10]=0x27;
  cpu.rom[11]=0x6d;
  cpu.rom[12]=0x55;
  cpu.rom[13]=0x51;
  cpu.rom[14]=0x28;
  cpu.rom[15]=0x0c;
  cpu.rom[16]=0x3e;
  struct timespec lt;
  struct timespec nt, request = {0,104166L};
  char c;
  struct pollfd pfd;
  bool isdebug=false;
  pfd.fd=STDIN_FILENO;
  pfd.events=POLLIN;
  clock_gettime(CLOCK_MONOTONIC,&lt);
  for(;;) {
    if (poll(&pfd,1,10)==-1) die("poll");
    if(pfd.revents&POLLIN) {
      if(read(STDIN_FILENO, &c, 1)==-1) die("read");
      if (c==4) isdebug=true; else
      if (isdebug) {
        if (c=='q') break;
        if (c=='s') cpu.doInst();
	if (c==4) {
	  cpu.addchar(c);
          nanosleep(&request,&nt);
	}
	if (c=='x') isdebug=false;
	if (c=='b') cpu.dbg=true;
	if (c=='c') cpu.dbg=false;
      } else {
        cpu.addchar(c);
        nanosleep(&request,&nt);
      }
    }
    clock_gettime(CLOCK_MONOTONIC,&nt);
    cpu.run(d(&nt,&lt));
    lt=nt;
  }
  return 0;
}
// g++ -Wall -Wfatal-errors -O2 -o main main.cpp
