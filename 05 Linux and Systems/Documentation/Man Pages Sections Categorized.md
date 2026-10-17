---
tags: [linux]
created: 2025-09-15
publish: true
---
We have been showing [[Man Pages]] for cmds. However, there are many different types of cmds  (user commands, system commands, and administration commands), configuration files and other features, such as libraries and kernel components, that require documentation.

[[Where Are These Commands Located]]

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

