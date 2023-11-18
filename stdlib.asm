$return=POP TSC TCPCH POP TSC TCPCL
$jump=LDA%1 TAS TSC TCPCH LDA%2 TAS TSC TCPCL
.org 0
ntok:
.b 0
.b 0
randseed:
.b 0
.b 0
.org 49152
$jump endstdlibH endstdlibL
;u8 *memchr(u8 *str, u8 c, u16 n)
memchr:
LDA 0
POP
TSB
ADD
POP
TSB
EQADD
PSH
PSH
LDA l6H
TAS
TSC
TCPCH
LDA l6L
TAS
TSC
EQTCPCL
POP
POP
LDA 255
TSB
ADD
TCS
PSH
TSB
ADD
TCS
POP
POP
TSB
POP
TSC
TCRAH
POP
TSC
TCRAL
TMA
XOR
TSB
PSH
TSA
POP
POP
TSC
TCPCH
POP
TSC
EQTCPCL
PSH
PSH
LDA 0
ADD
TCS
PSH
TSB
ADD
TCS
PSH
PSH
PSH
PSH
$jump memchrH memchrL
l6:
LDA 0
POP
POP
POP
POP
POP
$return
;memcmp
;void memcpy(u8 *dest, u8 *src, u16 n)
memcpy:
LDA 0
POP
TSB
ADD
POP
TSB
EQADD
PSH
PSH
LDA l1H
TAS
TSC
TCPCH
LDA l1L
TAS
TSC
EQTCPCL
POP
POP
TSB
LDA 255
ADD
TCS
PSH
TSB
ADD
TCS
POP
POP
POP
TSC
TCRAL
TSB
LDA 0
ADD
TCS
PSH
TSC
TCRAH
TSB
ADD
TCS
POP
POP
TMA
TSC
TCRAH
POP
TSC
TCRAL
PSH
PSH
PSH
PSH
PSH
PSH
TAS
TSC
TCM
POP
POP
POP
POP
POP
POP
TSB
LDA 1
ADD
TCS
PSH
TSB
LDA 0
ADD
TCS
PSH
PSH
PSH
PSH
PSH
$jump memcpyH memcpyL
l1:
POP
POP
POP
POP
POP
POP
$return
;memmove
;void memset(u8 *str, u8 c, u16 n)
memset:
LDA 0
POP
TSB
ADD
POP
TSB
EQADD
PSH
PSH
LDA l2H
TAS
TSC
TCPCH
LDA l2L
TAS
TSC
EQTCPCL
POP
POP
TSB
LDA 255
ADD
TCS
PSH
TSB
ADD
TCS
POP
POP
POP
POP
LDA 0
TSC
TCRAL
TSB
ADD
TCS
PSH
TSC
TCRAH
TSB
ADD
TCS
PSH
TSC
TCM
PSH
PSH
PSH
$jump memsetH memsetL
l2:
POP
POP
POP
POP
POP
$return
;void strcat(i8 *dest, i8 *src)
strcat:
POP
POP
POP
TSB
POP
TSC
PSH
PSH
PSH
PSH
LDA l4L
TAS
PSH
LDA l4H
TAS
PSH
TCS
PSH
TBS
PSH
$jump strlenH strlenL
l4:
TBS
POP
POP
POP
TSB
ADD
TCS
PSH
PSH
PSH
TSB
POP
POP
POP
POP
TSA
ADD
TCS
PSH
PSH
PSH
PSH
$jump strcpyH strcpyL
;void strncat(i8 *dest, i8 *src, u16 n)
;i8 *strchr(i8 *str, i8 c)
strchr:
POP
POP
TSB
POP
TSC
PSH
PSH
PSH
LDA l5L
TAS
PSH
LDA l5H
TAS
PSH
TCS
PSH
TBS
PSH
$jump strlenH strlenL
l5:
TBS
PSH
TAS
PSH
$jump memchrH memchrL
;strcmp
;strncmp
;void strcpy(i8 *dest, i8 *src)
strcpy:
POP
TSB
POP
TSC
PSH
PSH
LDA l3L
TAS
PSH
LDA l3H
TAS
PSH
TCS
PSH
TBS
PSH
$jump strlenH strlenL
l3:
TAS
LDA 1
ADD
LDA 0
TSB
TCS
ADD
PSH
TCS
PSH
$jump memcpyH memcpyL
;void strncpy(i8 *dest, i8 *src, u16 n)
;u16 strcspn(i8 *str1, i8 *str2)
;u16 strlen(i8 *str)
strlen:
LDA 0
TAS
TSB
PSH
TAS
PSH
l7:
POP
POP
POP
TSC
TCRAH
POP
TSC
TCRAL
TMA
SUB
PSH
PSH
PSH
PSH
LDA l8H
TAS
TSC
TCPCH
LDA l8L
TAS
TSC
EQTCPCL
LDA 1
TAS
TSB
POP
POP
TSA
ADD
TCS
PSH
LDA 0
TSB
ADD
TCS
POP
POP
POP
LDA 1
TSB
ADD
TCS
PSH
LDA 0
TSB
ADD
TCS
PSH
PSH
PSH
TAS
TSB
$jump l7H l7L
l8:
POP
TSA
POP
TSB
POP
POP
$return
;i8 *strpbrk(i8 *str1, i8 *str2)
;i8 *strrchr(i8 *str, i8 c)
;u16 strspn(i8 *str1, i8 *str2)
;i8 *strstr(i8 *haystack, i8 *needle)
;i8 *strtok(i8 *str, i8 *delim)
;i8 atoi(i8 *str)
;i16 atol(i8 *str)
;i8 rand8()
rand8:
LDA randseedH
TAS
TSC
TCRAH
LDA randseedL
TAS
TSC
TCRAL
TMA
TAS
TSB
ADD
CLC
TCS
TSA
TSB
ADD
SEC
TCS
TSB
TMA
ADD
TCS
TCM
LDA randseedL+1
PSH
TAS
TSC
TCRAL
TMA
TAS
TSB
CLC
ADD
TCS
TSB
LDA 0
ADD
TCS
LDA 16
AND
TSB
LDA l10H
TAS
TSC
TCPCH
LDA l10L
TAS
TSC
NETCPCL
TBS
PSH
LDA 0
TAS
TSB
POP
TSA
SUB
TCS
TSB
l10:
POP
TSA
XOR
TCS
TSB
$return
;i16 rand16()
rand16:
LDA l11H
TAS
TSC
TCPCH
PSH
LDA l11L
TAS
TSC
PSH
TCPCL
l11:
CLC
TBS
PSH
LDA l12H
TAS
TSC
TCPCH
PSH
LDA l12L
TAS
TSC
TCPCL
l12:
POP
TSA
$return
;void srand(u16 seed)
srand:
LDA randseedH
TAS
TSC
TCRAH
LDA randseedL
TAS
TSC
TCRAL
POP
TSC
TCM
LDA randseedL+1
TAS
TSC
TCRAL
POP
TSC
TCM
$return
;u8 *calloc(u16 size)
;void free(u8* ptr)
;u8 *malloc(u16 size)
;u8 *bsearch(u8 *key, u8 *base, u16 num, u16 size, i8 (*compar)(i8*,i8*))
;void qsort(u8 *base, u16 num, u16 size, i8 (*compar)(u8*,u8*))
;2i8 div(i8 numer, i8 denom)
;i16* ldiv(i16 numer, i16 denom)
;u16 sprintf(i8 *str, i8 *format, u8 **args)
;u16 snprintf(i8 *s, u16 n, i8 *format, u8 **args)
;void swap(u8 *str1, u8 *str2, u16 n)
;void print(u8 *str)
print:
POP
TSC
TCRAH
POP
TSC
TCRAL
LDA 1
TSB
ADD
TCS
PSH
LDA 0
TSB
ADD
TCS
TMA
PSH
TAS
TSB
LDA 128
TAS
TSC
TCRAH
LDA 0
XOR
TAS
TSC
TCRAL
LDA l9H
TAS
TSC
TCPCH
LDA l9L
TAS
TSC
EQTCPCL
TBS
TSC
TCM
$jump printH printL
l9:
POP
POP
$return
endstdlib: