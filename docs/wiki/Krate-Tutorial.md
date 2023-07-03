# Krate

[Krate](https://github.com/ArgosOfIthica/scalu/blob/master/examples/krate/scalu.cfg) is a 5 bit virtual machine implemented as a configuration file, using scalu. The advantage of this approach is that its incredibly easy to make use of; simply load the VM config in-game, and you're ready to go, no other installations or knowledge necessary.

## Registers

Like many VM's, Krate has a collection of registers where it stores values; these registers are simply labeled `a`,`b`,`c`...though `z`. Each of these registers are 5 bits in size, meaning they can store integers between 0 and 31 inclusive.

You can also simply refer to constants literally. `$13`, internally, refers to a read-only register with a value of 13.


## Sequences

You can interact with Krate through a simple assembly language. There are just two kinds of sequences in this language:

Assignment:

`reg1;reg2;reg_output;operator`

Conditional:

`reg1;reg2;operator`

### Assignment Sequences

Suppose I want to calculate 7 + 4 and store the result in a register called z, then *print* that variable to the command line. This is simple:

`$7;$4;z;add;print`

This will print `11` to the console.

A unary operation:

`unary;$7;z;copy`

The unary command tells krate to skip processing the first argument.

All assignment operators:
```
Unary:

copy
not

Binary:

add
sub
or
and
```

While useful, these commands don't really affect the "outside" world, they only affect the state inside the Krate VM. You can, however, affect the outside world with conditional sequences.

### Conditional Sequences


Suppose I want to call `my_alias` if a is 3, otherwise call `my_other_alias`.

```
alias true "my_alias"
alias false "my_other_alias"
a;$3;eq
```

This will execute "true" and thus "my_alias" if a is 3, otherwise execute "false" and "my_other_alias". "my_alias" and "my_other_alias" are conventional aliases that can be defined however you like.

All conditional operators:
```
eq - Equals
ne - Not Equals
gt - Greater Than
lt - Less Than
gte - Greater Than or Equal
lte - Less Than or Equal
```
## Composition

The great thing about Krate is that it naturally composes with the native configuration language. Suppose register b represents my current class, for instance. This can be aliased just how you imagine it would be.

Say we want to store the current class in register b:
```
alias current_class b

alias set_pyro_class "unary;$3;current_class;copy"
```
This can be further improved; aliasing a constant is sort of like declaring an enum, like in regular programming!
```
alias pyro_class $3

alias set_pyro_class "unary;pyro_class;current_class;copy"
```

## Jumps

The `z` register in Krate has a special command called `jump`; this command acts as a fast way of mapping a number to an action without using a lot of `if` statements. This is how the `print` command is implemented! Printing isn't a special part of Krate, anyone can easily recreate it.

```
alias print "alias jump0 echo 0;alias jump1 echo 1;alias jump2 echo 2;alias jump3 echo 3;alias jump4 echo 4;alias jump5 echo 5;alias jump6 echo 6;alias jump7 echo 7;alias jump8 echo 8;alias jump9 echo 9;alias jump10 echo 10;alias jump11 echo 11;alias jump12 echo 12;alias jump13 echo 13;alias jump14 echo 14;alias jump15 echo 15;alias jump16 echo 16;alias jump17 echo 17;alias jump18 echo 18;alias jump19 echo 19;alias jump20 echo 20;alias jump21 echo 21;alias jump22 echo 22;alias jump23 echo 23;%5du"

alias %5du "alias jump24 echo 24;alias jump25 echo 25;alias jump26 echo 26;alias jump27 echo 27;alias jump28 echo 28;alias jump29 echo 29;alias jump30 echo 30;alias jump31 echo 31;jump"
```
As you can see, the print statement exhaustively goes through and assigns every jump possibility to echo a certain number.

## Building (for developers)

krate.py is a python script which generates a scalu script which generates the output config; Python is only involved because scalu does not have a macro system or compile-time facilities to generate all the boilerplate needed to make compiling krate independently viable. After generation, you'll need to remove event prefixes added by scalu to avoid namespace collision (replace '$' with ''). You will also need to delete all instances of the string "delete"; this is because scalu does not allow naming an event with a number as the first character, so getting around this requires prefixing events with a string of letter characters you delete later (replace 'delete' with ''). 

