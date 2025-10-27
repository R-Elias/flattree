import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

DEFAULT_SEPARATOR = "*----flattree-file-separator----*"

def read_ignore_file(ignore_file: Path) -> List[str]:
    if ignore_file.exists():
        with ignore_file.open('r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def list_files(startpath: Path, output_file: Optional[Path], extensions: Optional[List[str]], max_lines: Optional[int], strict_extensions: Optional[List[str]], ignore: List[str]) -> None:
    allowed_extensions = set(ext.lower() for ext in extensions) if extensions else set()
    strict_allowed_extensions = set(ext.lower() for ext in strict_extensions) if strict_extensions else set()
    ignore.append('.flattreeignore')
    ignore_set = set(ignore)
    ignore_set.update(read_ignore_file(startpath / '.flattreeignore'))
    output_path = Path(output_file) if output_file else None
    if output_path and output_path.exists():
        ignore_set.add(str(output_path.name))
    output_stream = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    def is_ignored(path: Path) -> bool:
        relative_path = path.relative_to(startpath)
        for pattern in ignore_set:
            if relative_path.match(pattern) or str(relative_path).startswith(pattern):
                return True
        return False
    with output_stream as f_out:
        total_files = 0
        included = 0
        for root, dirs, files in os.walk(startpath, topdown=True):
            dirs[:] = [d for d in dirs if not is_ignored(Path(root) / d)]
            for name in files:
                path = Path(root) / name
                if is_ignored(path):
                    continue
                relative_path = path.relative_to(startpath)
                f_out.write(f"{DEFAULT_SEPARATOR}\n{relative_path}\n")
                total_files += 1
                file_suffix = path.suffix[1:].lower()
                base_name, ext = path.stem, file_suffix
                include = False
                if strict_allowed_extensions:
                    base_name_parts = base_name.split('.')
                    if len(base_name_parts) == 1 and ext in strict_allowed_extensions:
                        include = True
                elif not allowed_extensions or ext in allowed_extensions:
                    include = True
                if include:
                    included += 1
                    process_file_content(f_out, path, max_lines)
        print(f"{total_files} fichiers listés, {included} fichiers avec contenu inclus.")

def process_file_content(f_out, path, max_lines):
    try:
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        if max_lines is None or len(lines) <= max_lines:
            f_out.write(f"{content}\n\n")
    except UnicodeDecodeError:
        print(f"Warning: Cannot decode file {path}. Skipping.", file=sys.stderr)
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        sys.exit(1)

def write_tree(input_file: Path, output_dir: Path):
    if not input_file.exists():
        print(f"Input file {input_file} not found.", file=sys.stderr)
        sys.exit(1)
    output_dir.mkdir(parents=True, exist_ok=True)
    with input_file.open('r', encoding='utf-8') as f:
        content = f.read().split(DEFAULT_SEPARATOR)
    for block in content:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        header = lines[0]
        if header.endswith('/'):
            (output_dir / header).mkdir(parents=True, exist_ok=True)
        else:
            path = output_dir / header
            path.parent.mkdir(parents=True, exist_ok=True)
            body = '\n'.join(lines[1:])
            path.write_text(body, encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flatten or rebuild a directory tree.')
    parser.add_argument('mode', choices=['read', 'write'], help='Mode: read to flatten, write to rebuild')
    parser.add_argument('-o', '--output', help='Output file name (for read mode)')
    parser.add_argument('-i', '--input', help='Input flat file (for write mode)')
    parser.add_argument('-d', '--directory', help='Directory to analyze or write to (default: current directory)')
    parser.add_argument('--extensions', help='Comma-separated list of file extensions to display fully (e.g. js,ts,py)')
    parser.add_argument('-n', '--max-lines', type=int, help='Maximum number of lines in files to display their content')
    parser.add_argument('--strict-extensions', help='Comma-separated list of strict file extensions to display fully (e.g. js,ts,py)')
    parser.add_argument('--ignore', help='Comma-separated list of files or directories to ignore')
    args = parser.parse_args()
    directory = Path(args.directory) if args.directory else Path.cwd()
    if args.mode == 'read':
        extensions = args.extensions.split(',') if args.extensions else None
        strict_extensions = args.strict_extensions.split(',') if args.strict_extensions else None
        ignore_list = args.ignore.split(',') if args.ignore else []
        list_files(directory, Path(args.output) if args.output else None, extensions, args.max_lines, strict_extensions, ignore_list)
    elif args.mode == 'write':
        if not args.input:
            print("Error: --input is required in write mode.", file=sys.stderr)
            sys.exit(1)
        write_tree(Path(args.input), directory)
