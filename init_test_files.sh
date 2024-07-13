#!/bin/bash

mkdir -p testdir/subdir1
mkdir -p testdir/subdir2/subsubdir1
mkdir -p testdir/subdir3

echo "Content of text file 1." > testdir/file1.txt
echo "Content of text file 2." > testdir/file2.md
echo "Content of Python file." > testdir/script.py

echo "Content of JavaScript file." > testdir/subdir1/app.js
echo "Content of TypeScript file." > testdir/subdir1/app.ts
echo "Content of HTML file." > testdir/subdir1/index.html

echo "Content of CSS file." > testdir/subdir2/subsubdir1/styles.css
echo "Content of JSON file." > testdir/subdir2/subsubdir1/config.json

echo "Content of README file." > testdir/subdir3/README.md
echo "Content of Markdown file." > testdir/subdir3/docs.md
echo "Content of YAML file." > testdir/subdir3/config.yaml

echo "Content of file without extension." > testdir/subdir3/file_without_extension
echo "Content of another file without extension." > testdir/subdir3/another_file

echo "Initialization complete. Directory structure and files created."
