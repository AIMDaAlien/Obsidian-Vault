---
tags: [linux, cli]
created: 2025-09-15
updated: 2026-10-25
publish: true
---
> Merged 2026-10-25 from: Viewing Man Pages, Sections Within Man Pages, Searching Man Pages, Man Pages Sections Categorized, Where Are These Commands Located, Using Help Option.

UNIX is the operating system that Linux was modeled after. The unix devs created help documents called *man pages* (short for manual pages).

Man pages are used to describe the features of cmds, providing basic descriptions of purposes of cmds, as well as details regarding available options.

## Viewing Man Pages

`man command`

For example, the following shows the man page for `ls`:
<!-- embed removed: Pasted image 20230610152720.png (file not in vault) -->

Navigate the doc using the arrow keys
<!-- embed removed: Pasted image 20230610152753.png (file not in vault) -->

<!-- embed removed: Pasted image 20230611185210.png (file not in vault) -->

**The `man` command uses a pager to display documents. Usually, this pager is the `less` command, but on some distributions, it may be the `more` command.
To view the various movement cmds that are available, use H while viewing a man page. This shows a help page.

Man pages are broken into sections. [[Man Pages#Sections Within Man Pages|Sections Within Man Pages]]

## Sections Within Man Pages

Each section is made to give specific info about a cmd. While there are common sections seen in most man pages, some devs also create sections only available on specific man pages. [[Man Pages#Searching Man Pages|Searching Man Pages]]

##### Name
Gives name of cmd and brief description.
<!-- embed removed: Pasted image 20230610185051.png (file not in vault) -->

##### Synopsis
Gives examples of how cmd is executed
<!-- embed removed: Pasted image 20230610185130.png (file not in vault) -->

The `SYNOPSIS` section can be hard to understand but is important because it gives concise example of how to use cmd.
For example, the synopsis of the `cal` cmd:
<!-- embed removed: Pasted image 20230610185326.png (file not in vault) -->
The [] are used to indicate that this feature is not required to run the cmd. They simply are options.

Another component of the synopsis that might confuse can be seen in `date` cmd:
<!-- embed removed: Pasted image 20230610185506.png (file not in vault) -->
There are two syntaxes for `date`. The first one is used to show system date while second is for setting date.

The ellipses . . . Following `[OPTION]` indicates that one or more items before it may be used. Additionally, the `[-u|--utc|--universal]` notation means that `-u` or `--utc` or `--universal` may be used. Typically, all three options do the same thing, but sometimes | is used to indicate that the options cant be used in combos, such as  [[Double Pipe]].

###### Description
Gives more detailed description of the cmd
<!-- embed removed: Pasted image 20230610201401.png (file not in vault) -->

###### Options
Lists the options for the smd as well as a description of how the y are used. This info might be found in `DESCRIPTION` and not in a separate `OPTIONS` section.
<!-- embed removed: Pasted image 20230610201605.png (file not in vault) -->

###### Files
Lists the files that are associated with the cmd as well as a description of how theyre used. These files can be used to configure the cmd's advanced features. This info is often found in `DESCRIPTION` section and not in a separate `FILES` section.

###### Author
Gives name of whoever created the man page and sometimes how to contact them.

###### Reporting  Bugs
Gives details on how to report problems
<!-- embed removed: Pasted image 20230610201937.png (file not in vault) -->

###### Copyright
Gives basic copyright info
<!-- embed removed: Pasted image 20230610202003.png (file not in vault) -->

###### SEE ALSO
Gives idea of where to find more info. Often includes other cmds related to the cmd.
<!-- embed removed: Pasted image 20230610202129.png (file not in vault) -->

## Searching Man Pages

To search a term in Man Pages, type /

If match found, itll be highlighted. Press N to move to next term.
To return to  previous match of term, press shift+N.
If term not found, program will report  `Pattern not found (press Return)`.

<!-- embed removed: LEv2_6_1 1.gif (file not in vault) -->

## Man Pages Sections Categorized

We have been showing Man Pages for cmds. However, there are many different types of cmds  (user commands, system commands, and administration commands), configuration files and other features, such as libraries and kernel components, that require documentation.

There are thousands of man pages on a typical distro. To organize these pages, they are categorized by sections:

- General Commands
- System Calls
- Library Calls
- Special Files
- File Formats and Conventions
- Games
- Miscellaneous
- Sysadmin Commands
- Kernel Routines

`man` searches each of these sections until it finds first match. If you execute `man cal`, the first section (General Commands) is searched for a man page called `cal`. If not found, then second section is searched and so on. If no matches, an error is returned.
<!-- embed removed: Pasted image 20230610203449.png (file not in vault) -->

To determine which section a man page belongs to, look at numbers on first line of the output. For example,  `cal` belongs to the first section:
<!-- embed removed: Pasted image 20230610203617.png (file not in vault) -->

Sometimes there are man pages with the same name in different sections. Int those cases, you may have to specify the section of the correct man page.

For example, `passwd` allows you to change password. Theres also a file called   *passwd* that stores account info.

`passwd` is a user cmd, so the associated man page is in the first section. `man` displays the man page for `passwd` by default.
<!-- embed removed: Pasted image 20230610214312.png (file not in vault) -->

How to show man page for *passwd* file? First, determine what section the man page is located. To search by name, use `-f` to the `man`
<!-- embed removed: Pasted image 20230610214451.png (file not in vault) -->

**Note:** *On most Linux distributions, the `whatis` command does the same thing as `man -f`. On those distributions, both will produce the same output.*

To specify a different section, give section number
<!-- embed removed: Pasted image 20230610215248.png (file not in vault) -->

Each man page has a short desc associated with it. `-k` to `man` searches both names and descs of the man pages for a keyword.

To find a man page that shows how to copy directories,
<!-- embed removed: Pasted image 20230610215531.png (file not in vault) -->

When searching for a keyword, be very specific.

**Note:** *On most Linux distributions, the `apropos` command does the same thing as `man -k`. On those distributions, both produce the same output.*

## Where Are These Commands Located

Use `whereis` to search for location of a cmd or source files or Man Pages.
<!-- embed removed: Pasted image 20230610220359.png (file not in vault) -->

Man pages are easily distinguished from cmds as they are typically compressed with a program called `gzip` resulting in a filename *.gz* . Notice there are ttwo man pages listed above, but one cmd: */bin/ls*. Thats becuase `ls` can be used with features/options described by either man page.

## Using Help Option

Many cmds will give basic info similar to `SYNOPSIS` in Man Pages by using `--help`  after whatever cmd.

`cat --help`
<!-- embed removed: Pasted image 20230611184407.png (file not in vault) -->
