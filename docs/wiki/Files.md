# Files
Frequently, Source engine games will automatically execute cfg files with certain names (like listenserver or autoexec). It is useful to be able to hook these files into scalu to know more about the gamestate.

The way this is done in scalu is by linking files to single events.

```
file {
  autoexec : my_event1
  listenserver : my_event2
}
```
This tells the compiler to output files called `autoexec.cfg` and `listenserver.cfg`, and exclusively link those files to `my_event1` and `my_event2` respectively. Files, like binds, can only be bound to a single event, and the compiler will throw an error if two files share the same event.