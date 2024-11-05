#!/bin/bash

# Define base directories
input_dir="Input"
output_dir="Output"

# Create nested folders and files within the Input directory
mkdir -p "$input_dir/folder1/subfolder1"
mkdir -p "$input_dir/folder1/subfolder2"
mkdir -p "$input_dir/folder2/subfolder3"

# Create dummy files in each folder
touch "$input_dir/file1.txt"
touch "$input_dir/file2.log"
touch "$input_dir/folder1/file3.md"
touch "$input_dir/folder1/subfolder1/file4.py"
touch "$input_dir/folder1/subfolder2/file5.json"
touch "$input_dir/folder2/file6.csv"
touch "$input_dir/folder2/subfolder3/file7.xml"

# Add a dummy file to the Output directory
touch "$output_dir/dummy_output.txt"

echo "Test folders and files created successfully."
