---
tags: [linux, shell]
created: 2025-09-15
publish: true
---
These are my personal notes from a Linux command-line course.

# Command History

## Viewing the history list

The shell keeps a list of the commands I have run in a terminal, and the `history` command prints it. To see it in action, I run a command first and then ask for the history.

```bash
echo Hi
history
```

Each entry in the output has a number next to it. Those numbers matter later, because they are how I refer back to a command. While practicing I also used two other simple commands: `date` prints the current time and date on the system, and `clear` wipes the screen so the output is easier to read.

```bash
date
clear
```

## Limiting the output

The full list can get long. If I only want the most recent entries, `history` accepts a number and shows exactly that many of the latest commands. For example, this shows the last five:

```bash
history 5
```

Likewise, `history 4` would show the last four. The number is just the count of recent commands to display.

## Re-running a command by number

Once a command appears in the list, I can run it again by typing an exclamation point followed by its history number, with no space in between. If the command I want is number 9 in the list:

```bash
!9
```

The same idea works for the third entry with `!3`. The number refers to the position shown next to the command in the `history` output, so I check the list first and then pick the number.

## Re-running relative to the end of the list

Sometimes counting from the bottom is easier than reading an absolute number. To run the nth command from the bottom of the list, I type `!-n`. So to run the fifth from the bottom:

```bash
!-5
```

## Re-running the most recent command

The quickest repeat is the last command I ran. Two exclamation points do exactly that:

```bash
!!
```

I can also re-run the most recent command that started with a certain word by typing an exclamation point followed directly by the command name. For example, `!echo` would repeat my latest `echo` command.

```bash
!echo
```

## Complete result

| Command | What it does |
|---|---|
| `history` | Prints the numbered list of commands run in this terminal |
| `history N` | Shows only the last N commands (for example `history 5`) |
| `!N` | Runs the command with history number N (for example `!9`, `!3`) |
| `!-N` | Runs the Nth command counting from the bottom of the list (for example `!-5`) |
| `!!` | Runs the most recent command again |
| `!command` | Runs the most recent command that began with that name |
| `echo` | Prints text, handy for generating a history entry |
| `date` | Prints the current time and date |
| `clear` | Clears the terminal screen |
