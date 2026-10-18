---
tags: [linux, shell]
created: 2025-09-15
publish: true
featured: 81
summary: "How your terminal decides what a command is: built in, a separate program, a shortcut (alias) or a function, and how to check which one runs."
---

These are my personal notes from a Linux command-line course.

# Command Types

A good way to learn more about a command is to look at where it comes from. The shell gets its commands from several sources: internal (builtin) commands, external commands, aliases, and functions. The `type` command tells me which kind I am dealing with.

```bash
type command
```

## Internal (builtin) commands

Internal commands are built into the shell itself. The classic example is `cd`, which is part of the Bash shell. When I type it, Bash is already running and knows how to interpret it, so no extra program is needed. Asking `type` about `cd` confirms this with `cd is a shell builtin`.

```bash
type cd
```

## External commands

External commands are binary executables stored in directories the shell searches. If I type `ls`, the shell walks through the directories listed in the `PATH` variable until it finds an executable file named `ls`. I can also skip the search by typing the full path, such as `/bin/ls`.

For external commands, `type` reports where the file lives:

```bash
type cal
```

This prints `cal is /usr/bin/cal`.

### Finding a command with which

When a command misbehaves or can't be reached, I want to know where the shell finds it and which version it uses. Reading every directory in `PATH` by hand is tedious, so `which` does it for me. It searches `PATH` and prints the full path of the executable, for example `/bin/ls` for `ls`, `/usr/bin/cal` for `cal`, and `/bin/date` for `date`. In other words, it tells me exactly which file runs when I type the command.

```bash
which ls
```

### Comparing type and which

The two can disagree sharply. `echo` exists both as a builtin and as a file, so `type echo` says it is a shell builtin while `which echo` shows `/bin/echo`. The `-a` option of `type` lists every location that contains the command, builtin and file together.

```bash
type -a echo
```

The output is `echo is a shell builtin` followed by `echo is /bin/echo`.

## Executable programs

The last kind is the plain executable program: software installed on the system that does a specific job. Typing `vi` makes the shell look through `PATH` and run the program it finds. Other programs, such as the open source media player `vlc`, are installed by users or admins for particular purposes, and they may not be in `PATH` unless installed in a way that puts them there. Checking both with `type` shows the difference.

```bash
type vi
cd /bin
type vlc
cd
```

## Aliases

An alias maps a long command to a shorter key sequence. When the shell sees an alias, it swaps in the longer text before interpreting the command line. For example, `ls -l` is often aliased to `l` or `ll`, which is quicker to type.

To list the aliases set in the current shell:

```bash
alias
```

Most of those came from initialization files, which exist to create aliases automatically at startup. A new alias uses this format, where `name` is the alias and `command` is what it runs:

```bash
alias name=command
```

Say I often run `cal 2019` to see that year's calendar. I can make an alias called `mycal` and run that instead. Aliases made this way last only while the shell is open, and every shell has its own set, so closing the shell loses them.

`type` can reveal aliases too. It shows that `ll` is an alias for `ls -alF`, and that even `ls` is an alias for `ls --color=auto`.

## Functions

Functions build on existing commands to make new ones, or to override builtins and commands stored in files. Like aliases, they are normally loaded from initialization files when the shell starts. They are more advanced than aliases and show up often in Bash scripts. The syntax looks like this:

```bash
function_name ()
{
   commands
}
```

The name can be anything the admin likes, and the `commands` placeholder is replaced with whatever should run. The placement of `()` and `{}` matters, and indenting the body with tabs keeps it readable.

A function lets me run a set of commands in one go instead of typing them repeatedly. My example, `my_report`, runs `ls`, `date`, and `echo`. While I type a function at the prompt, the shell shows `>` as a continuation prompt for entering the commands; the braces tell it where the function begins and ends. Once defined, I run the function by typing its name at the Bash prompt.

## Complete result

| Command | Type | What it does |
|---|---|---|
| `type command` | builtin | Reports what kind of command a name is |
| `type -a command` | builtin | Lists every location and form of a command |
| `cd` | internal (builtin) | Changes directory; part of Bash itself |
| `ls` | external, also aliased | Lists files; found by searching `PATH` |
| `/bin/ls` | external (full path) | Runs the file directly, skipping the search |
| `cal` | external | Shows a calendar; at `/usr/bin/cal` |
| `echo` | builtin and external | Prints text; exists as both a builtin and `/bin/echo` |
| `date` | external | Prints the date; at `/bin/date` |
| `which command` | external | Prints the full path found through `PATH` |
| `vi`, `vlc` | executable programs | Installed programs located via `PATH` |
| `alias` | builtin | Lists aliases currently set |
| `alias name=command` | alias | Creates a shorter name for a command |
| `ll`, `mycal` | alias | `ll` is `ls -alF`; `mycal` is `cal 2019` |
| `name () { ... }` | function | Groups commands under one name, such as `my_report` |
