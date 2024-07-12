import argparse
import sys
from pathlib import Path
from typing import List, Optional

DEFAULT_SEPARATOR = "*----flattree-file-separator----*"

def list_files(startpath: Path, output_file: Optional[Path], extensions: Optional[List[str]], max_lines: Optional[int], strict_extensions: Optional[List[str]]) -> None:
    allowed_extensions = set(ext.lower() for ext in extensions) if extensions else set()
    strict_allowed_extensions = set(ext.lower() for ext in strict_extensions) if strict_extensions else set()

    output_stream = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout

    with output_stream as f_out:
        for path in startpath.rglob('*'):
            if path.is_dir():
                f_out.write(f"{DEFAULT_SEPARATOR}\n{path.relative_to(startpath)}/\n")
            elif path.is_file():
                f_out.write(f"{DEFAULT_SEPARATOR}\n{path.relative_to(startpath)}\n")
                
                file_suffix = path.suffix[1:].lower()
                base_name, ext = path.stem, file_suffix
                
                if strict_allowed_extensions:
                    base_name_parts = base_name.split('.')
                    if len(base_name_parts) == 1 and ext in strict_allowed_extensions:
                        process_file_content(f_out, path, max_lines)
                elif not allowed_extensions or ext in allowed_extensions:
                    process_file_content(f_out, path, max_lines)

def process_file_content(f_out, path, max_lines):
    try:
        content = path.read_text(encoding='utf-8').strip()
        lines = content.split('\n')
        if max_lines is None or len(lines) < max_lines:
            f_out.write(f"{content}\n")
    except UnicodeDecodeError:
        print(f"Warning: Cannot decode file {path}. Skipping.", file=sys.stderr)
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files and their content in a directory tree.')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-d', '--directory', help='Directory to analyze (default: current directory)')
    parser.add_argument('--extensions', help='Comma-separated list of file extensions to display fully (e.g. js,ts,py)')
    parser.add_argument('-n', '--max-lines', type=int, help='Maximum number of lines in files to display their content')
    parser.add_argument('--strict-extensions', help='Comma-separated list of strict file extensions to display fully (e.g. js,ts,py)')
    args = parser.parse_args()

    directory = Path(args.directory) if args.directory else Path.cwd()

    extensions = args.extensions.split(',') if args.extensions else None
    strict_extensions = args.strict_extensions.split(',') if args.strict_extensions else None
    list_files(directory, Path(args.output) if args.output else None, extensions, args.max_lines, strict_extensions)
