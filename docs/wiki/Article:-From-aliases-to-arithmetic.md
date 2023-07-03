This is a small article investigating the computational power of the Quake/Source command `alias`, and how it can be used to model computation.

## Background

`alias` is a command in Quake-like engines that can assign shortcuts to a series of other commands. This command is in Quake 1 and Quake 2, and in many derivative engines, like the Source engine. Quake 3 changed the syntax of config files, so what's written here will not directly apply to it and its derivatives. 

An example:

```
alias printout "echo line 1; echo line 2; echo line 3"
bind key printout
```
## Behavior

Aliases can be referred to by other aliases:

```
alias a "echo hello world"
alias b "a;a" //execute a twice
b //execute b immediately
```
In this form, we essentially have functions, in some sense, though our functions lack any arguments. This unfortunately means that we cannot naively implement a lambda calculus, as its very important for functions to have at least one argument to make sense in the functional paradigm.

Despite the fact that our functions have no arguments, there is a stack here preserving an instruction pointer. In other words, we can nest our aliases arbitrarily deeply, and they will be executed in a depth-first manner.
```
alias a "echo hello"
alias b "echo hey"
alias c "a;b"
alias d "b;a"
c;d //will print hello, hey, hey, hello
```

Another tool we have is recursion. We can tell an alias to execute itself, and it will obey, even if doing so completely locks up our client.

```
alias a "a"
a //continually executes a in a loop. Locks up the engine
```

## Conditional logic

The next tool we need is something that will help us conditionally execute code. We can abuse the fact that aliases can be rewritten at any time to do operations conditionally. In doing this, we can represent aliases as state or data, like so:

```
alias true ""
alias false ""
alias bool "true"
alias print_true "echo true"
alias print_false "echo false"
alias print_bool "alias true print_true; alias false print_false; bool"
```
This is equivalent to this Python code:

```
bool = True
def print_bool():
  if bool:
    echo("True")
  else:
    echo("False")
```
Implementing conditional logic naturally gives rise to some form of booleans. The next natural question is whether we can somehow copy the boolean value of one alias to another; as it turns out, this is also possible:


```
alias true ""
alias false ""
alias bool "true"
alias bool2 ""
alias bool2_is_true "alias bool2 true"
alias bool2_is_false "alias bool2 false"
alias copy "alias true bool2_is_true; alias false bool2_is_false; bool"
```

Not only can we conditionally do things based on the value of a boolean, but we can also copy that value to other booleans. Its also clear that we can assign the opposite value to a boolean...equivalent to a NOT gate.

```
alias not "alias true bool2_is_false; alias false bool2_is_true; bool"
```
From here, we're only a few steps away from logical completeness. We can also implement the AND and OR gates in a similar manner:

```
alias true ""
alias false ""
alias bool1 "true"
alias bool2 "false"
alias bool3 ""
alias bool3_is_true "alias bool3 true"
alias bool3_is_false "alias bool3 false"

alias or "alias true bool3_is_true; alias false or2; bool1"
alias or2 "alias true bool3_is_true; alias false bool3_is_false; bool2"

alias and "alias true and2; alias false bool3_is_false; bool1"
alias and2 "alias true bool3_is_true; alias false bool3_is_false; bool2"
```

At this point, we have the same computational machinery as any finite computer. `alias` is not Turing Complete in the formal sense, since all aliases, all memory, has to be accounted for in the source file. We cannot cleverly just ask for more memory ad-hoc like we can in a higher level language. That being said, in reality, its clear `alias` is capable of computing anything, given a large enough input size.