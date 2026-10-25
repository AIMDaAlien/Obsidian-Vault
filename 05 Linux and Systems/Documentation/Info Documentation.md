---
tags: [linux]
created: 2025-09-15
updated: 2026-10-25
publish: true
---
> Merged 2026-10-25 from: Viewing Info Documentation, Navigating Info Nodes, Exploring Info Documentation.

[[Man Pages]] are good sources, but tend to have some disadvantages. One example being that each man page is a separate doc, not related to any other man page. While some have `SEE ALSO` section, they tend to be independent sources of documentation.

`info` also provides documentation on OS cmds and features in a logical oranizational structure, making it more readable.

All documentation is merged into a single "book" representing all documentation available. Within info docs, info is broken down into categories that work like a table of contents. Hyperlinks are given to pages with info on specific topics for a cmd or feature.

Another advantage of info is the writing style is almost like learning a topic.

Consider man pages as reference resource and info docs as learning guide.

## Viewing Info Documentation

#### `info command`

For example, to show the info page of `ls`
<!-- embed removed: Pasted image 20230611182005.png (file not in vault) -->
<!-- embed removed: Pasted image 20230611182018.png (file not in vault) -->

The documentation is shown in nodes, and in the example, the stuff highlighted shows its currently in the `ls invocation` node.

#### Navigating Info Nodes

First line gives index info about current location within doc.
Next node would be `dir invocation` much like a book.
Going up a level is `Directory listing`.

Scrolling through the doc, notice menu for `ls`
<!-- embed removed: Pasted image 20230611182328.png (file not in vault) -->
The items under the menu are hyperlinks that link to nodes that describe `ls`.
Placing the cursor on the line * Sorting the output: :  and pressing enter leads to a node that describes sorting the output of `ls`

**Note:
Going into the node about sorting leads into a sub-node of the original. To go back to the previous node, use U. while U leads to the start of the node a level up, L returns to the same location as before entering the sorting mode.

## Navigating Info Nodes

Like `man` in [[Man Pages]], a listing of movement cmds is available by Shift+H while reading the info doc.
<!-- embed removed: Pasted image 20230611183406.png (file not in vault) -->

**note that to close the help screen, type L which brings back the current doc. To quit entirely, use Q

## Exploring Info Documentation

Instead of using info doc to look up info about a specific cmd or feature, consider exploring the capabilities of Linux by reading Info Documentation.

Execute `info` without arguments to be taken to top of the documentation. Good starting point to explore features offered:
<!-- embed removed: Pasted image 20230611183906.png (file not in vault) -->
