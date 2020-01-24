## Introduction

scalu is a memory-bound, event-based programming language and compiler targeting Valve's Source Engine, used in games like Left 4 Dead, Counter-Strike: Global Offensive, Team Fortress 2, Portal, and many more. "Scripting" in these games is traditionally done in the key-binding system, where keys are bound to "aliases". These aliases are bound to multiple commands, some of which might change the value of other aliases. While this system is often used very creatively to achieve desirable in-game effects, it is chaotic, unmaintainable, and uncomposable.

scalu is a language purpose built to fix these problems by allowing script writers to write their scripts in a conventional, maintainable programming language that resembles C, while also allowing end-users to resolve script conflicts easily and automatically. This is made possible by observing that the rudimentary alias system provided in these games is actually capable of storing complex state, as well as arbitrary computation.

## Setup

The scalu compiler is being built in Python 3. 

The .cfg files generated by the compiler should be put in here:

```
C:\Program Files (x86)\Steam\steamapps\common\yourgamehere\cfg
```

but this might vary per game or Source build.


## Examples

This is a script to compute and display the first 10 Fibonacci numbers. Note that this script is using the deprecated "cycle" style framework. This script will not work with the "flat" framework that is currently in development:

```
exec scalu
// load the scalu interface

alias fib_r1 "alias copy_ptr1 r1; alias copy_ptr2 c1; copy"
// copy 1 into r1

alias fib_r2 "alias copy_ptr1 r2; alias copy_ptr2 c1; copy"
// copy 1 into r2

alias fib_r3 "alias copy_ptr1 r3; alias copy_ptr2 ca; copy"
//copy 10 (or 0xA) into r3

alias fib_addr1 "alias add_ptr1 r1; alias add_ptr2 r2; add"
//point the add instruction to r1 and r2, then add. Note that scalu uses Intel-style "destination, source" form for arguments

alias fib_addr2 "alias add_ptr1 r2; alias add_ptr2 r1; add"
//point the add instruction to r2 and r1, then add

alias fib_dumpr1 "alias hd_ptr r1; hd"
//point the hex dump instruction at r1, then dump

alias fib_dumpr2 "alias hd_ptr r2; hd"
//point the hex dump instruction at r2, then dump

alias fib_dec "alias dec_ptr r3; dec; 
//decrement r3

alias fib_zero "alias zero_ptr r3; alias zero_rettrue echo end ; alias zero_retfalse fib2; zero"
//point the zero instruction at r3. if true, zero will execute zero_rettrue. if false, zero will execute zero_retfalse, and therefore, fib2

alias fib2_zero "alias zero_ptr r3; alias zero_rettrue echo end ; alias zero_retfalse fib; zero"
//point the zero instruction at r3. if true, zero will execute zero_rettrue. if false, zero will execute zero_retfalse, and therefore, fib


alias fib "fib_dumpr1;fib_addr1; fib_dec; echo %%%% ; fib_zero"


alias fib2 "fib_dumpr2; fib_addr2; fib_dec; echo %%%%% ; fib2_zero"


fib_r1
fib_r2
fib_r3

fib
```

