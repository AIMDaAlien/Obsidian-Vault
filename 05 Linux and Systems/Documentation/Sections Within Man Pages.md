---
tags: [linux]
created: 2025-09-15
publish: true
---

[[Man Pages]]
Each section is made to give specific info about a cmd. While there are common sections seen in most man pages, some devs also create sections only available on specific man pages. [[Searching Man Pages]]

#### Name
Gives name of cmd and brief description.
<!-- embed removed: Pasted image 20230610185051.png (file not in vault) -->

#### Synopsis
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

##### Description
Gives more detailed description of the cmd
<!-- embed removed: Pasted image 20230610201401.png (file not in vault) -->

##### Options
Lists the options for the smd as well as a description of how the y are used. This info might be found in `DESCRIPTION` and not in a separate `OPTIONS` section.
<!-- embed removed: Pasted image 20230610201605.png (file not in vault) -->

##### Files
Lists the files that are associated with the cmd as well as a description of how theyre used. These files can be used to configure the cmd's advanced features. This info is often found in `DESCRIPTION` section and not in a separate `FILES` section.

##### Author
Gives name of whoever created the man page and sometimes how to contact them.

##### Reporting  Bugs
Gives details on how to report problems
<!-- embed removed: Pasted image 20230610201937.png (file not in vault) -->

##### Copyright
Gives basic copyright info
<!-- embed removed: Pasted image 20230610202003.png (file not in vault) -->

##### SEE ALSO
Gives idea of where to find more info. Often includes other cmds related to the cmd.
<!-- embed removed: Pasted image 20230610202129.png (file not in vault) -->

