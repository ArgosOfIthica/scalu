# Services
Services are the core functionality of scalu, allowing use of typical programming constructs.

```
service my_service1 {
  a = 5 + 5
  ...
}
```

## Assignment

Assignments are when some variable is set to be equivalent to some expression. By default, all numbers in scalu are unsigned 8-bit. This means they can represent the numbers `0` through `255`. 
```
a = !5
b = a & 5
c = (a & b) + 5
```

### Binary Operators

`+` : addition <br>
`-` : subtraction <br>
`&` : bitwise and <br>
`|` : bitwise or <br>

### Unary Operators
`?` : passes the current value, but prints it to the console, in binary <br>
`!` : bitwise negation

### Precedence
Currently, scalu has no concept of precedence. It simply evaluates left to right and respects parentheses. This may change though, so its best to write expressions using parentheses.

## Service Calls
Services can call other services, similar to how functions can call other functions in other languages.

```
a = 5
@some_other_service /*this calls out to some other service in the sandbox*/
a = 6 /* this executes after the call is finished*/
```
## If Statements
Services can conditionally execute code, depending on the truth value of some conditional. Note that, for technical reasons, conditionals and expressions are different; conditionals cannot be nested or mixed with expressions.

```
a = 5
if (a == 5){
  @do_something
}
else {
  @do_something_else
}
```
### Binary Conditionals

`==` : equality <br>
`!=` : inequality <br>
`>` : greater than <br>
`<` : less than <br>
`>=` : greater than or equal to <br>
`<=` : less than or equal to <br>

## Jump Statements
Jump statements are a way of quickly jumping to some block of code based on the value of a variable, similar to a switch statement in other languages. Jump statements can have a maximum of 127 different jump blocks. Jump statements do not validate the argument given, meaning an argument greater than the number of available blocks will jump in accordance to its underlying bit representation.

```
a = 2
jump (a) { {[echo a is 0] @someotherservice} {[echo a is 1] a = 63} {[echo a is 2]}}
```

## Source Calls
Source calls directly execute engine code.

```
a = 5
[echo foo]
[echo bar]
[echo foo bar]
...
```
Note that source calls do not know anything about scalu and cannot yet be changed at compile time. Additionally, source calls cannot have quotes of any kind put in them, as they will already be in a quote layer in the output file.


