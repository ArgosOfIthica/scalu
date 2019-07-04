## Introduction

scalu is a general purpose implementation of arithmetic built almost entirely from the Source engine's "alias" command. This interface acts as a pseudo-assembly language to provide more computational power to script writers. By default, the library provides immediate access to 8-bit "registers" and an instruction set capable of basic bitwise operations, conditional branching, addition, subtraction, and random number generation.

## Setup

To install the scalu libraries, merge the cfg directory in this repo with the cfg directory of the Source game you want to install this with. This is typically located in:

```
C:\Program Files (x86)\Steam\steamapps\common\yourgamehere\cfg
```

but this might vary per game or Source build.

This project also contains Python scripts for help in automating the creation of registers and constants. These should be run with arguments at the command line; run them for more specific options and documentation.


## Examples

This is a script to compute and display the first 10 Fibonacci numbers:

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
