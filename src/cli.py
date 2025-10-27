import sys
import argparse
from pathlib import Path
from .core import list_files, write_tree


def main() -> None:
    parser = argparse.ArgumentParser(description="Flatten or rebuild a directory tree.")
    parser.add_argument("mode", choices=["read", "write"], help="Mode: read to flatten, write to rebuild")
    parser.add_argument("-o", "--output", help="Output file name (for read mode)")
    parser.add_argument("-i", "--input", help="Input flat file (for write mode)")
    parser.add_argument("-d", "--directory", help="Directory to analyze or write to (default: current directory)")
    parser.add_argument("--extensions", help="Comma-separated list of file extensions to include (e.g. py,js)")
    parser.add_argument("--strict-extensions", help="Comma-separated list of strict file extensions to include (e.g. js)")
    parser.add_argument("-n", "--max-lines", type=int, help="Include file contents only if file has <= N lines")
    parser.add_argument("--ignore", help="Comma-separated list of files or directories to ignore")
    args = parser.parse_args()

    directory = Path(args.directory) if args.directory else Path.cwd()

    if args.mode == "read":
        extensions = args.extensions.split(",") if args.extensions else None
        strict_ext = args.strict_extensions.split(",") if args.strict_extensions else None
        ignore_list = args.ignore.split(",") if args.ignore else []
        list_files(directory, Path(args.output) if args.output else None, extensions, args.max_lines, strict_ext, ignore_list)

    elif args.mode == "write":
        if not args.input:
            print("Error: --input is required in write mode.", file=sys.stderr)
            sys.exit(1)
        write_tree(Path(args.input), directory)


if __name__ == "__main__":
    main()
