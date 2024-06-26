import os
import argparse
import sys

def list_files(startpath, output_file):
    default_separator = "?-file-separator-?"
    with open(output_file, 'w') as f_out:
        for root, dirs, files in os.walk(startpath):
            path = root.replace(startpath, "", 1)
            f_out.write(f"{default_separator}\n{path}/\n")
            
            for file in files:
                file_path = os.path.join(root, file)
                f_out.write(f"{default_separator}\n{file_path}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        content = f_in.read().strip()
                        f_out.write(f"{content}\n")
                except UnicodeDecodeError:
                    print(f"Warning: Cannot decode file {file_path}. Skipping.")
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files and their content in a directory tree.')
    parser.add_argument('-o', '--output', required=True, help='Output file name')
    parser.add_argument('-d', '--directory', required=True, help='Directory to analyze')
    args = parser.parse_args()

    list_files(args.directory, args.output)
