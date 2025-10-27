import sys
import os
from pathlib import Path
from typing import List, Optional
from .utils import DEFAULT_SEPARATOR, read_ignore_file, warn


def list_files(
    startpath: Path,
    output_file: Optional[Path],
    extensions: Optional[List[str]],
    max_lines: Optional[int],
    strict_extensions: Optional[List[str]],
    ignore: List[str],
) -> None:
    allowed_extensions = set(ext.lower() for ext in extensions) if extensions else set()
    strict_allowed_extensions = set(ext.lower() for ext in strict_extensions) if strict_extensions else set()

    ignore.append(".flattreeignore")
    ignore_set = set(ignore)
    ignore_set.update(read_ignore_file(startpath / ".flattreeignore"))

    if output_file:
        ignore_set.add(output_file.name)

    output_stream = open(output_file, "w", encoding="utf-8") if output_file else sys.stdout

    def is_ignored(path: Path) -> bool:
        rel = path.relative_to(startpath)
        for pattern in ignore_set:
            if rel.match(pattern) or str(rel).startswith(pattern):
                return True
        return False

    total, included = 0, 0
    with output_stream as f_out:
        for root, dirs, files in os.walk(startpath, topdown=True):
            dirs[:] = [d for d in dirs if not is_ignored(Path(root) / d)]
            for name in files:
                path = Path(root) / name
                if is_ignored(path):
                    continue
                rel = path.relative_to(startpath)
                f_out.write(f"{DEFAULT_SEPARATOR}\n{rel}\n")
                total += 1

                ext = path.suffix[1:].lower()
                base = path.stem
                include = False

                if strict_allowed_extensions:
                    if "." not in base and ext in strict_allowed_extensions:
                        include = True
                elif not allowed_extensions or ext in allowed_extensions:
                    include = True

                if include:
                    included += 1
                    process_file_content(f_out, path, max_lines)

        print(f"{total} fichiers listés, {included} fichiers avec contenu inclus.")


def process_file_content(f_out, path: Path, max_lines: Optional[int]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")
        if max_lines is None or len(lines) <= max_lines:
            f_out.write(f"{content}\n\n")
    except UnicodeDecodeError:
        warn(f"Cannot decode file {path}. Skipping.")
    except Exception as e:
        warn(f"Error reading {path}: {e}")
        sys.exit(1)


def write_tree(input_file: Path, output_dir: Path) -> None:
    if not input_file.exists():
        warn(f"Input file {input_file} not found.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    with input_file.open("r", encoding="utf-8") as f:
        content = f.read().split(DEFAULT_SEPARATOR)

    for block in content:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        header = lines[0]
        if header.endswith("/"):
            (output_dir / header).mkdir(parents=True, exist_ok=True)
        else:
            path = output_dir / header
            path.parent.mkdir(parents=True, exist_ok=True)
            body = "\n".join(lines[1:])
            path.write_text(body, encoding="utf-8")
