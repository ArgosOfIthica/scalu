[![Liberapay](https://img.shields.io/liberapay/receives/Argos.svg?logo=liberapay&style=flat-square)](https://liberapay.com/Argos/)
<img src="https://img.shields.io/github/issues/ArgosOfIthica/scalu" alt="issues shield">   
<img src="https://img.shields.io/github/license/ArgosOfIthica/scalu" alt="license shield"> 
<img src="https://img.shields.io/github/repo-size/ArgosOfIthica/scalu" alt="size shield"> 
<img src="https://img.shields.io/github/v/release/ArgosOfIthica/scalu" alt="release shield"> </p>
<p align="center">
<img src="/assets/logo.png" alt="scalu logo" width="400">

## Introduction

scalu (server/client arithmetic logical unit) is an event based programming language that exists for the purpose of building sandboxable scripts that run on Source engine clients, or more generally, any engine which has inherited a Quake-like configuration system. Scripts in the Source Engine are otherwise written entirely by creatively using the console command ```alias```, somewhat akin to POSIX ```alias```. This command is used to construct finite state machines that can perform logical operations and store state between key presses and game actions. scalu automates this process and adds composable PL constructs to make writing scripts easier and more maintainable.


## Setup

To run scalu, you will need Python 3.6 or later installed on your system. Create a directory on your system and then clone scalu.

```git clone https://github.com/ArgosOfIthica/scalu.git```

If you do not have git installed, you can simply download the project from Github and unpack it in a directory of your choice. Once that is done, you should have a running scalu compiler.

Input files go in the ```scalu_in``` directory. To compile them, go to the ```python``` directory and run: <br>

```python scalu.py compile``` <br>

Linux users may need to run: <br>

```python3 scalu.py compile``` <br>

The output will be located in a new directory called ```scalu_out```. Copy these into your configuration files; the exact location of these files will depend on platform and game.

## Documentation

You can find documentation in the Github wiki at https://github.com/ArgosOfIthica/scalu/wiki

</p>
