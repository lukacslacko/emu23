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
    clockrate=1/(double)hertz;
    reset();
    ltime=0;
  }
  ~CPU() {
    ;
  }
  void run(double t) {
    ltime+=t;
    std::string s;
    while (ltime>clockrate) {
      doInst();
      if (dbg) {
        debug();
        std::cout << std::flush;
        std::cin >> s;
      }
      ltime-=cycle*clockrate;
      cycle=0;
    }
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
  }
  void debug() {
    printf("CZI=%d%d%d PC=%06x PCB=%02x PCH=%02x RA=%06x SB=%02x ISB=%02x SP=%04x FP=%04x r1=%02x r2=%02x r3=%02x r4=%02x r5=%02x r6=%02x r7=%02x A=r%d B=r%d C=%02x int=%02x halted=%d",flagC,flagZ,flagI,PC,PCB,PCH,RA,SB,ISB,SP,FP,r1,r2,r3,r4,r5,r6,r7,rA,rB,rC,intc,halted);
  }
  uint8_t rom[0x8000];
// private:
  bool halted,dbg;
  double clockrate;
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
  double ltime;
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
      case 0x34://shr
        rC=A>>1;
        flagC=A&1;
        flagZ=!rC;
        return 2;
      case 0x36://rori
        getImm();
      case 0x35://ror
        rC=A>>1|flagC<<7;
        flagC=A&1;
        flagZ=!rC;
        return 2;
      case 0x36://tcrab
        RA=RA&0xffff|(uint32_t)rC<<16;
        return 2;
      case 0x37://trabc
        rC=RA>>16;
        return 2;
      case 0x38://tcrah
        RA=RA&0xff00ff|(uint32_t)rC<<8;
        return 2;
      case 0x39://trahc
        rC=RA>>8&0xff;
        return 2;
      case 0x3a://tcral
        RA=RA&0xffff00|(uint32_t)rC;
        return 2;
      case 0x3b://tralc
        rC=RA&0xff;
        return 2;
      case 0x3c://jmps
        PC=PC&0xff0000|(uint32_t)PCH<<8|(uint32_t)rC;
        return 2;
      case 0x3d://jmpl
        PC=(uint32_t)PCB<<16|(uint32_t)PCH<<8|(uint32_t)rC;
        return 2;
      case 0x3e://calls
        push(PC&0xff);
        push(PC>>8&0xff);
        PC=PC&0xff0000|(uint32_t)PCH<<8|(uint32_t)rC;
        return 4;
      case 0x3f://calll
        push(PC&0xff);
        push(PC>>8&0xff);
        push(PC>>16);
        PC=(uint32_t)PCB<<16|(uint32_t)PCH<<8|(uint32_t)rC;
        return 5;
      case 0x40://rets
        PC=PC&0xff0000|(uint32_t)pop()<<8;
        PC|=(uint32_t)pop();
        return 3;
      case 0x41://retl
        PC=(uint32_t)pop()<<16;
        PC|=(uint32_t)pop()<<8;
        PC|=(uint32_t)pop();
        return 4;
      case 0x42://rti
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
      case 0x43://brk
        if (!flagI) {
          fault(2,true);
          return 1;
        }
        dbg=true;
        return 2;
      case 0x44://sys
        fault(0,true);
        return 1;
      case 0x45://sicc
        if (!flagC) {
          PC+=2;
          return 3;
        }
        return 2;
      case 0x46://scc
        if (!flagC) {
          PC++;
        }
        return 2;
      case 0x47://scs
        if (flagC) {
          PC++;
        }
        return 2;
      case 0x48://sics
        if (flagC) {
          PC+=2;
          return 3;
        }
        return 2;
      case 0x49://sieq
        if (flagZ) {
          PC+=2;
          return 3;
        }
        return 2;
      case 0x4a://seq
        if (flagZ) {
          PC++;
        }
        return 2;
      case 0x4b://sine
        if (!flagZ) {
          PC+=2;
          return 3;
        }
        return 2;
      case 0x4c://sne
        if (!flagZ) {
          PC++;
        }
        return 2;
      case 0x4d://tic
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        rC=intc;
        return 2;
      case 0x4e://tami
        getImm();
      case 0x4f://tam
        write(RA,A);
        return 2;
      case 0x50://tbmi
        getImm();
      case 0x51://tbm
        write(RA,B);
        return 2;
      case 0x52://tcm
        write(RA,rC);
        return 2;
      case 0x53://tma
        setA(read(RA));
        return 2;
      case 0x54://tmb
        setB(read(RA));
        return 2;
      case 0x55://tmc
        rC=read(RA);
        return 2;
      case 0x56://hlt
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        halted=true;
        dbg=true;
        return 2;
      case 0x57://reset
        if (!flagI) {
          fault(1,true);
          return 1;
        }
        reset();
        return 2;
      case 0x58://cmpi
        getImm();
      case 0x59://cmp
        flagZ=A==B;
        flagC=B>A;
        return 2;
      case 0x5a://tsbai
        getImm();
      case 0x5b://tsba
        setA(read(indstack(B)));
        return 2;
      case 0x5c://tcsbi
        getImm();
      case 0x5d://tcsb
        write(indstack(B),rC);
        return 2;
      case 0x5e://tasbi
        getImm();
      case 0x5f://tasb
        write(indstack(B),A);
        return 2;
      case 0x60://tsbci
        getImm();
      case 0x61://tsbc
        rC=read(indstack(B));
        return 2;
      case 0x62://nop
        return 2;
      case 0x63://tcsph
        SP=SP&0xff|(uint16_t)rC<<8;
        return 2;
      case 0x64://tcspl
        SP=SP&0xff00|(uint16_t)rC;
        return 2;
      case 0x65://tsphc
        rC=SP>>8;
        return 2;
      case 0x66://tsplc
        rC=SP&0xff;
        return 2;
      case 0x67://tcspb
        SB=rC;
        return 2;
      case 0x68://tspbc
        rC=SB;
        return 2;
      case 0x69://tcispb
        ISB=rC;
        return 2;
      case 0x6a://tispbc
        rC=ISB;
        return 2;
      case 0x6b://tcpch
        PCH=rC;
        return 2;
      case 0x6c://tcpcb
        PCB=rC;
        return 2;
      case 0x6d://tpchc
        rC=PCH;
        return 2;
      case 0x6e://tpcbc
        rC=PCB;
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
    if (PC<0x800000) {
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
    if (PC<0x800000) {
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

int main(int argc, char** argv) {
  CPU cpu = CPU(100,true);
  time_t lt = time(nullptr);
  time_t nt;
  if (argc < 2) return 1;
  std::ifstream infile(argv[1], std::ios::binary);
  char buf[0x100];
  infile.read(buf,14);
  if (!infile) return 1;
  if (buf[0]!=0xfe||buf[1]!=0xed) {
    std::cout << "wrong magic" << std::endl;
    return 1;
  }
  uint32_t code_size=(uint32_t)buf[2]<<16|(uint32_t)buf[3]<<8|(uint32_t)buf[4];
  uint32_t rodata_size=(uint32_t)buf[5]<<16|(uint32_t)buf[6]<<8|(uint32_t)buf[7];
  uint32_t data_size=(uint32_t)buf[8]<<16|(uint32_t)buf[9]<<8|(uint32_t)buf[10];
  uint32_t entry=(uint32_t)buf[11]<<16|(uint32_t)buf[12]<<8|(uint32_t)buf[13];
  // identity map atr
  for (uint16_t i=0;i<0x2000;i++) {
    cpu.atr[i<<1]=i&0xff;
    cpu.atr[(i<<1)+1]=i>>8;
  }
  cpu.SP=0xffff;
  cpu.SB=0x80;
  for (uint16_t i=1;i<64;i++) {
    cpu.atr[(i<<1)+1]|=0xc0; // set stack to RW
  }
  for (uint16_t i=65;i<66+(code_size>>10);i++) {
    cpu.atr[(i<<1)+1]|=0x20; // set code to X
  }
  for (uint16_t i=66+(code_size>>10);i<67+(rodata_size>>10)+(code_size>>10);i++) {
    cpu.atr[(i<<1)+1]|=0x80; // set rodata to R
  }
  for (uint16_t i=67+(rodata_size>>10)+(code_size>>10);i<68+(data_size>>10)+(rodata_size>>10)+(code_size>>10);i++) {
    cpu.atr[(i<<1)+1]|=0xc0; // set data to RW
  }
  cpu.rom[0x80]=0x43;
  cpu.rom[0x81]=0x42;
  cpu.rom[0]=0;
  cpu.rom[1]=0x2a;
  cpu.rom[2]=entry&0xff;
  cpu.rom[3]=0x2a;
  cpu.rom[4]=(entry&0xff00)>>8;
  cpu.rom[5]=0x2a;
  cpu.rom[6]=entry>>16;
  cpu.rom[7]=0x42;
  for(;;) {
    nt=time(nullptr);
    cpu.run(difftime(nt,lt));
    lt=nt;
  }
  return 0;
}
// g++ -Wall -Wfatal-errors -std=c++17 -O2 -o main main.cpp