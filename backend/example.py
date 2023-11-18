from api import Backend, Type, Operation

b = Backend()

# 1  static s: i8;
# 2  s := 42;
# 3  while (1)
# 4  {  // A
# 5    s := s - 1;
# 6    if (s == 10)
# 7    {  // B
# 8      break 2;
# 9    }
#10  }
#11  s := 5;

# {  // B
B = b.begin_block()
# break 2;
b.break_block(2);

###

jump B.after
B:
B.begin:
; {  // B
nop
; break 2
mov break_counter, 2
jump B.end
; }
mov break_counter, 1
B.end:
dec break_counter
ret
B.after:

jump A.after
A:
; {  // A
nop
; s := s - 1
sub [sp], 1
; if (s == 10)
mov R0, [sp]
sub R0, 10
brne line_10:
call B
cmp break_counter, 0
brne A.end
line_10:
jump A
A.end:
dec break_counter
ret
A.after:

