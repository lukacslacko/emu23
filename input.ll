/*
fun add_fp(a: i8, b: i8; result: i8) {
  result := a + b;
};

fun mul_fp(a: i8, b: i8; result: i8) {
  result := 99;
  if (a == 0) {
    result := 0;
    return;
  }
  if (b == 0) {
    result := 0;
    return;
  }
  result := mul_fp(a-1, b) + b;
};

static e: i8;
static fn: ptr;

fn := add_fp;

e := fn(23, 32);
e := mul_fp(5, 7);
*/

static a: i8;
a := 42;

local b: i8;
b := (a+1)*3;

{ local hello: i8; };

if (b > 10) {
  local x: i8;
  x := a + b;
};

while (a > 1) {
  a := a - 1;
  b := b + 1;
};

local c: i8;
c := 4;
c := b + c + a +10;
b := 2 * c;
local d: i8;
d := a * b + c * 2;

local e: i8;
e := 1;
local i: i8;
for (i := 0;i < 20;i+=1) {
e *= 3;
};


/*
static val: i8;
static other: i8;
static p: ptr;

val := 9;
other := 11;
p := &other;
val := *p;
*/
/*
local u: i8;
local v: i8;
v := 42;
u := 110;
{
  local y: i8;
  u := 100;
  break;
  u := 115;
};
v := u;
*/
/*
while (1) {
  u := u - 1;
  if (u == 93) break;
};
*/