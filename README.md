# FLATTREE(1) - User Commands

## NAME
`flattree.py` - Create a flat representation of a directory tree with file contents.
Mainly designed to simplify input management for LLM code analysis and generation.

## SYNOPSIS

`python flattree.py [-o OUTPUT_FILE] [-d DIRECTORY] [--extensions=EXT1,EXT2] [--strict-extensions=EXT1,EXT2] [-n MAX_LINES] [--ignore=IGNORE1,IGNORE2]`

## DESCRIPTION
`flattree.py` traverses a specified directory and its subdirectories, creating
a flat representation of the file tree. It writes the directory structure 
and file contents to an output file, separating entries with a default 
separator.

## OPTIONS
- `-o OUTPUT_FILE`, `--output OUTPUT_FILE`
  - Optional. Specify the name of the output file. If not specified, the output 
    will be printed to the standard output.

- `-d DIRECTORY`, `--directory DIRECTORY`
  - Optional. Specify the directory to analyze. If not specified, the current 
    working directory will be used.

- `--extensions=EXT1,EXT2,...`
  - Optional. Provide a comma-separated list of file extensions. Only 
    files with these extensions will have their full content included 
    in the output. Files with other extensions will only be listed by 
    name.

- `--strict-extensions=EXT1,EXT2,...`
  - Optional. Provide a comma-separated list of strict file extensions. 
    Only files with these exact extensions will have their full content 
    included in the output. For example, `--strict-extensions=js` will include
    `file.js` but not `file.spec.js`.

- `-n MAX_LINES`, `--max-lines MAX_LINES`
  - Optional. Specify the maximum number of lines for files to include 
    their content in the output. Files with more lines than this number 
    will only be listed by name.

- `--ignore=IGNORE1,IGNORE2,...`
  - Optional. Provide a comma-separated list of files or directories to ignore. 
    These files or directories will not be included in the output. The script 
    will also automatically ignore files and directories listed in a 
    `.flattreeignore` file if it exists in the specified directory.

## EXAMPLES

`python flattree.py`

Analyze the current working directory and print the output to the standard output.
All files will be listed, but only their names will be included.

`python flattree.py -o tree_output.txt -d /path/to/project`

Analyze the directory `/path/to/project` and save the output to 
`tree_output.txt`. All files will be listed, but only their names 
will be included.

`python flattree.py -o code_output.txt -d /path/to/project --extensions=py,js,css`

Analyze the directory `/path/to/project` and save the output to 
`code_output.txt`. All files will be listed, but only `.py`, `.js`, 
and `.css` files will have their content included in the output.

`python flattree.py -o code_output.txt -d /path/to/project --strict-extensions=js`

Analyze the directory `/path/to/project` and save the output to 
`code_output.txt`. All files will be listed, but only `.js` files with the exact 
extension `.js` will have their content included in the output.

`python flattree.py -o code_output.txt -d /path/to/project -n 100`

Analyze the directory `/path/to/project` and save the output to 
`code_output.txt`. All files will be listed, but only files with fewer than 
100 lines will have their content included in the output.

`python flattree.py -o code_output.txt -d /path/to/project --ignore=file1.txt,subdir3`

Analyze the directory `/path/to/project` and save the output to 
`code_output.txt`. All files will be listed, but the file `file1.txt` and the 
directory `subdir3` will be ignored.

## NOTES
- The script uses UTF-8 encoding for reading files and writing output. It 
  will skip files that cannot be decoded and exit if there's an error 
  reading a file.

- The default separator between entries in the output file is 
  `"*----flattree-file-separator----*"`.

- The script automatically ignores the `.flattreeignore` file if it exists in the specified directory.

- While this project already works, it is still in development.

## AUTHOR
Elias Aliche
