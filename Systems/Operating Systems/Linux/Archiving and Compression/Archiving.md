
When an archive is decompressed, and one or more files are extracted this is called un-archiving.

#### Benefits
-  When backing up directories, it is easier to keep them all in one archive than it is to version (update) each file.
- Some streaming devices such as tapes perform better if you’re sending a stream of data rather than individual files.

The traditional UNIX utility to archive files is called `tar`, short for TApe aRchive. It was used to stream many files to a tape for backups or file transfer. `tar` takes in several files and creates a single output file that can be split again into the original files.

*The `tar` command has three modes that are helpful to become familiar with:*
- Create: Make a new archive out of a series of files.
- Extract: Pull one or more files out of an archive.
- List: Show the contents of the archive without extracting.

[[Create Mode]]