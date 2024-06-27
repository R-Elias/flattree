import argparse
import sys
from pathlib import Path
from typing import List, Optional

DEFAULT_SEPARATOR = "?-file-separator-?"

def list_files(startpath: Path, output_file: Path, extensions: Optional[List[str]]) -> None:
    allowed_extensions = set(ext.lower() for ext in extensions) if extensions else set()

    with output_file.open('w', encoding='utf-8') as f_out:
        for path in startpath.rglob('*'):
            if path.is_dir():
                f_out.write(f"{DEFAULT_SEPARATOR}\n{path.relative_to(startpath)}/\n")
            elif path.is_file():
                f_out.write(f"{DEFAULT_SEPARATOR}\n{path.relative_to(startpath)}\n")
                
                if not allowed_extensions or path.suffix[1:].lower() in allowed_extensions:
                    try:
                        content = path.read_text(encoding='utf-8').strip()
                        f_out.write(f"{content}\n")
                    except UnicodeDecodeError:
                        print(f"Warning: Cannot decode file {path}. Skipping.")
                    except Exception as e:
                        print(f"Error reading {path}: {e}")
                        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files and their content in a directory tree.')
    parser.add_argument('-o', '--output', required=True, help='Output file name')
    parser.add_argument('-d', '--directory', required=True, help='Directory to analyze')
    parser.add_argument('--extensions', help='Comma-separated list of file extensions to display fully (e.g. js,ts,py)')
    args = parser.parse_args()

    extensions = args.extensions.split(',') if args.extensions else None
    list_files(Path(args.directory), Path(args.output), extensions)