# sysutil
Collection of scripts of various functionalities


## clean_node
Find and optionally delete npm module folders.

- Recursively searches for directories named "node_modules" or "npm_modules"
  under a given root (default: current directory).
- Prints all matches with index numbers.
- Prompts once: move all to Recycle Bin (preferred) or delete permanently.
- Use --permanent to skip Recycle Bin and delete immediately.

Tip: install send2trash for safe deletion:
    pip install send2trash

Example Run Command:
`python clean_node "C:\path\to\target"`


## extract_all
Moves all files from subdirectories to the top-level directory.

:param target_directory: The root directory to search for files.

## del_suffix
Deletes files that end with the specified suffix (before the file extension)
in the target directory and its subdirectories.

:param target_directory: The root directory to search for files.
:param suffix: The suffix of the files to delete (before the extension).
