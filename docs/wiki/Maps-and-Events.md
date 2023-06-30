# Events

Events are abstract names given to certain game actions. They are created implicitly in file and bind blocks, or explicitly in map blocks. Events are global, and do not respect sandboxes.

```
map {
  my_event1 : @some_service
  my_event1 : @some_other_service
  my_event2 : [echo hey]
  +bifurcated_event : @bifurc_service
  -bifurcated_event : [echo key unpressed]
}
```
If some key is bound to an event, that key will then execute any services that event is mapped to, and likewise for files linked to events.

## Service Stacking

In the above map block, `my_event1` is bound to two separate services. Upon `my_event1` being executed, both `some_service` and `some_other_service` will execute. `my_event1` will also execute any services its mapped to in any map block, in any sandbox. The order in which services are executed is undefined.

## Bifurcated Events

Bifurcated events have two parts; the `+` part and `-` part. When a `+` event is bound to some key, the `+` event is executed upon the key being held down. When the key is released, the `-` event will execute. The `-` event doesn't have to be bound to anything, it simply needs to be declared somewhere.

## The Console

Events are visible at the console level, unlike services. All events can be executed or referred to in the console as `$event_name`, except for bifurcated events, which are referred to as `+$event_name` and `-$event_name`.