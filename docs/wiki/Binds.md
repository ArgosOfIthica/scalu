# Binds

Binds relate the physical keys on your keyboard and mouse to events inside scalu.

```
bind {
  k : my_event1
  z : my_event2
  MWHEELUP : my_event3
}
```

The compiler does not know what keys are valid in your particular engine. Most Source games respect this list: https://developer.valvesoftware.com/wiki/Bind

Binds are exclusive, which means that two binds cannot share the same event. This allows for easy rebinding without affecting the functionality of your scripting logic.

## Rebinding in-game

Rebinding in-game is simple; suppose you want to rebind `z` to `my_event1`. To do this, you'd write

```bind z $my_event1```

Events in-game are prefixed with `$` for namespace purposes.