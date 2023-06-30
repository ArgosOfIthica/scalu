## Setup
For this script, we want a sandbox that is responsible for knowing what the current class is in Team Fortress 2. It should be able to keep track of any changes to our class, and be able to send that information to other sandboxes that want to know what the current class is.

## Execution
First, we need to declare our top-level sandbox.

`sandbox class`

Then, we need to decide how exactly to store the state of our current class. Ultimately, it is arbitrary, but we'll just say that Scout corresponds to 0, Soldier corresponds to 1, Pyro to 2, and so on according to their normal order.

Lets declare a service called `init` and just say that our variable `class` is initially declared as `9`; since Spy, the last class, is 8, 9 can mean that the class is undeclared right now.

```
sandbox class

service init {
	class = 9
}
```
Just like in the last section, we want `init` to execute immediately. Therefore, we'll map it to the `boot` event.

```
sandbox class

map {
	boot: @init
}

service init {
	class = 9
}

```
Now lets explicitly enumerate some services for every scenario.


```
sandbox class

map {
	boot: @init
}

service init {
	class = 9
}

service scout {
	class = 0
}

service soldier {
	class = 1
}

service pyro {
	class = 2
}

service demoman {
	class = 3
}

service heavyweapons {
	class = 4
}

service engineer {
	class = 5
}

service medic {
	class = 6
}

service sniper {
	class = 7
}

service spy {
	class = 8
}

```

Then, we should declare the abstract events of spawning as each class. Events are global, in that all of our sandboxes can see them. This means it will be trivial for a future script to react to, say, changing to the scout class.

```
sandbox class

map {
	boot: @init
	scout: @scout
	soldier: @soldier
	pyro: @pyro
	demoman: @demoman
	heavyweapons: @heavyweapons
	engineer: @engineer
	medic: @medic
	sniper: @sniper
	spy: @spy
}

service init {
	class = 9
} 

....
```
So now we've declared that an abstract "scout" event maps to the "scout" service, and so on for the other classes. Well, now what? How do we trigger these events? `boot` is special in that it is automatically triggered; scalu does not yet know the right time to trigger a `scout` event.

We're going to set our events to trigger with files; the Source engine already checks `scout.cfg`, `soldier.cfg`, etc upon switching to that class, and executes it if it sees it. We just have to tell scalu that executing these files triggers an event, and the compiler will take care of generating those files for us.

```
file {
	scout: scout
	soldier: soldier
	pyro: pyro
	demoman: demoman
	heavyweapons: heavyweapons
	engineer: engineer
	medic: medic
	sniper: sniper
	spy: spy
}
```


A `file` block tells the compiler that there is a relationship between a file name on the left side and the event on the right side. With this addition, executing `scout.cfg` now triggers the `scout` event, and every sandbox listening to that event will trigger some bit of code. We've done it! Here's our final product:

```
sandbox class

file {
	scout: scout
	soldier: soldier
	pyro: pyro
	demoman: demoman
	heavyweapons: heavyweapons
	engineer: engineer
	medic: medic
	sniper: sniper
	spy: spy
}

map {
	boot: @init
	scout: @scout
	soldier: @soldier
	pyro: @pyro
	demoman: @demoman
	heavyweapons: @heavyweapons
	engineer: @engineer
	medic: @medic
	sniper: @sniper
	spy: @spy
}

service init {
	class = 9
} 

service scout {
	class = 0
}

service soldier {
	class = 1
}

service pyro {
	class = 2
}

service demoman {
	class = 3
}

service heavyweapons {
	class = 4
}

service engineer {
	class = 5
}

service medic {
	class = 6
}

service sniper {
	class = 7
}

service spy {
	class = 8
}
