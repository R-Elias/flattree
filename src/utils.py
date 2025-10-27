import sys
from pathlib import Path
from typing import List

DEFAULT_SEPARATOR = "*----flattree-file-separator----*"


def read_ignore_file(ignore_file: Path) -> List[str]:
    if ignore_file.exists():
        with ignore_file.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


def warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)
