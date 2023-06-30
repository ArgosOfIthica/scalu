# Sandboxes

scalu is very concerned with modularity. Scripting in Source has a tradition of sharing, as well as "plug and play"; endusers want scripts that do something, and they do not want to overly concern themselves with integrating that functionality. scalu encapsulates this idea with sandboxes, top-level namespaces that all have their own state and functionality. Unlike other languages, scalu has no concept of a "main" function; sandboxes do not exist in a hierarchy, but rather are all equal, and negotiate when they should run at compile time. This federated approach to namespaces means that endusers can simply copy a script into their scripts folder and the script will automatically integrate itself with other scripts.

An escape hatch to sandboxes is provided where necessary with dot notation: `my_sandbox.my_var`. Be mindful of the coupling this ability creates. 

```
sandbox my_sandbox

service my_service {
a = 7
}
service other_service {
b = a /*this is valid. b equals 7 */
}

sandbox other_sandbox

service other_service {
b = a /* this will not compile. a is not declared */
}

service other_other_service {
b = my_sandbox.a /* this will compile */
}
```

Sandboxes contain file blocks, map blocks, bind blocks, and service blocks.

[Files](https://github.com/ArgosOfIthica/scalu/wiki/Files) <br>
[Binds](https://github.com/ArgosOfIthica/scalu/wiki/Binds) <br>
[Maps](https://github.com/ArgosOfIthica/scalu/wiki/Maps-and-Events) <br>
[Services](https://github.com/ArgosOfIthica/scalu/wiki/Services) <br>

