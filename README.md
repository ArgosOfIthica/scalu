## Introduction

scalu is an event-based programming language and compiler targeting Valve's Source Engine, used in games like Left 4 Dead, Counter-Strike: Global Offensive, Team Fortress 2, Portal, and many more. "Scripting" in these games is traditionally done in the key-binding system, where keys are bound to "aliases". These aliases are bound to multiple commands, some of which might change the value of other aliases. While this system is often used very creatively to achieve desirable in-game effects, it is chaotic, unmaintainable, and uncomposable.

scalu is a language purpose built to fix these problems by allowing script writers to write their scripts in a conventional, maintainable programming language that takes inspiration from Python, Javascript, and C. scalu allows end-users to resolve script conflicts easily and automatically. This is made possible by observing that the rudimentary alias system provided in these games is actually capable of storing complex state, as well as arbitrary computation.

## How does this work?


### Binding
scalu isolates the two basic use cases of the alias system, binding, and implementation. Keys are only bound to events, very much like traditional key-binding UI's. Events are abstract game actions, like "jump" or "move_right". Exactly how these actions are implemented is not defined in the binding system, and each key can only be bound to exactly one event. Therefore, changing your key binding for "jump" from space to mousewheel, for instance, is simply a matter of changing a couple lines in your config.


### Mapping
It doesn't matter how jump is implemented because the second use case, the logical implementation of an event, cannot see which key is bound to what event; any scripts concerned with "jump" only listen for that event. Events are global, and they are mapped to any script concerned with "jump" for execution.


### Sandboxes
The alias system has a huge problem with namespace; it only has a one global namespace, that contains the name of every piece of state and logic. This is very difficult to reason about. This is amplified by the fact that the alias system fundamentally cannot know much of the true game state, even though many scripts attempt to shadow the game state, resulting in even more confusion.

scalu attempts to solve this problem for users by introducing sandboxes. Sandboxes are namespaces as well as the primary organizational unit of the language. They contain state as well as "services", scalu's equivalent to a "function" in other programming languages.

### Composability
Reusing aliases is very difficult due to namespace issues; collisions are likely, and they may not fail hard. scalu is intended to be shared with others and highly modular. Sandboxes can only interfere with each other if they execute Source commands that interfere with each other ( a soft failure indicating that they are functionally incompatible) or two sandboxes declare mutually incompatible binding strategies (Script A is binding "move_forward" to W, but Script B is binding "move_forward" to A), which is a hard failure that will be found at compile time.

## Setup

The scalu compiler is being built in Python 3.6

scalu is currently in development and is not yet in a usable state. Stay tuned!




