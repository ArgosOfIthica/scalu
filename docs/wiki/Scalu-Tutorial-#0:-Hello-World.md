## Welcome
This series is a basic introduction to scalu programming; this guide will cover syntax, semantics, and a hopefully a path to achieving your particular goals through the scalu model. This is for experienced and inexperienced scripters alike. Do note this guide does not cover installation instructions or how to use the command line; those are covered TODO.

## Setup
This is a test make sure that your compiler works and can emit something in-game; we will make the console say "hello world!".

## Execution

First, we need to declare our top-level sandbox. A sandbox is a top-level namespace, and is responsible for hiding variables and functionality so that other sandboxes cannot accidentally use them.

`sandbox my_sandbox`

Now, we need to let the console know what to say. Lets declare a service called `my_service`. Services are similar to functions in other languages; its a little packet of functionality that does something.

```
sandbox my_sandbox

service my_service {

}
```

Great, now lets make `my_service` do something. We're going to make what's called a 'Source Call'. scalu cannot make the Source engine echo something to the console, it can only ask nicely. We'll use the `echo` command wrapped in `[]`, which is scalu notation for a source call.

```
sandbox my_sandbox

service my_service {
	[echo hello world!]
}
```
Excellent. While we now have _what_ we want scalu to do, we have not told it __when__ we want that thing to happen. scalu is an event-oriented language; to do something, `my_sandbox` must listen for an event to tell it what to do. Since we want `hello world!` to display immediately after we run our script, we will tell `my_sandbox` to listen for the special `boot` event; this event is triggered automatically and immediately after a scalu script is executed. We will do this with a map between the `boot` event and the `my_service` service.

```
sandbox my_sandbox

map {
	boot : @my_service
}

service my_service {
	[echo hello world!]
}
```

We're finished! After you compile this script and place `scalu.cfg` in your config directory, launch your game and run `exec scalu` in the console. You should see your program run.

