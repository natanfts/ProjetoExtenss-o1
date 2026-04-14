"""Utility to patch common Flet 0.84 compatibility issues in local sources."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = list((ROOT / "views").glob("*.py")) + [ROOT / "main.py"]


ALIGNMENT_FIXES = [
    ("ft.alignment.center", "ft.Alignment.CENTER"),
    ("ft.alignment.top_center", "ft.Alignment.TOP_CENTER"),
    ("ft.alignment.top_left", "ft.Alignment.TOP_LEFT"),
    ("ft.alignment.top_right", "ft.Alignment.TOP_RIGHT"),
    ("ft.alignment.bottom_left", "ft.Alignment.BOTTOM_LEFT"),
    ("ft.alignment.bottom_right", "ft.Alignment.BOTTOM_RIGHT"),
]

BUTTON_CALLS = [
    "ft.ElevatedButton(",
    "ft.TextButton(",
    "ft.OutlinedButton(",
]


def _find_matching_paren(source: str, open_paren_index: int) -> int:
    depth = 0
    in_string = None
    escaped = False

    for i in range(open_paren_index, len(source)):
        ch = source[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            continue

        if ch in ("'", '"'):
            in_string = ch
            continue

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i

    return -1


def _replace_top_level_text_kwarg(args: str) -> str:
    """Replace top-level `text=` with `content=` inside a function arg list."""
    level = 0
    in_string = None
    escaped = False
    i = 0

    while i < len(args):
        ch = args[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch in ("'", '"'):
            in_string = ch
            i += 1
            continue

        if ch in "([{":
            level += 1
            i += 1
            continue
        if ch in ")]}":
            if level > 0:
                level -= 1
            i += 1
            continue

        if level == 0 and args.startswith("text", i):
            j = i + 4
            while j < len(args) and args[j].isspace():
                j += 1
            if j < len(args) and args[j] == "=":
                return args[:i] + "content" + args[i + 4:]

        i += 1

    return args


def _replace_kwarg_in_calls(source: str, call_prefix: str) -> str:
    cursor = 0

    while True:
        start = source.find(call_prefix, cursor)
        if start == -1:
            break

        open_paren = start + len(call_prefix) - 1
        close_paren = _find_matching_paren(source, open_paren)
        if close_paren == -1:
            cursor = open_paren + 1
            continue

        args = source[open_paren + 1:close_paren]
        fixed_args = _replace_top_level_text_kwarg(args)

        if fixed_args != args:
            source = source[:open_paren + 1] + fixed_args + source[close_paren:]
            close_paren = open_paren + 1 + len(fixed_args)

        cursor = close_paren + 1

    return source


def apply_fixes(content: str) -> str:
    for old, new in ALIGNMENT_FIXES:
        content = content.replace(old, new)

    for call_prefix in BUTTON_CALLS:
        content = _replace_kwarg_in_calls(content, call_prefix)

    return content


def main() -> None:
    modified = 0

    for path in FILES:
        before = path.read_text(encoding="utf-8")
        after = apply_fixes(before)

        if after != before:
            path.write_text(after, encoding="utf-8")
            modified += 1
            print(f"Fixed: {path.name}")
        else:
            print(f"OK: {path.name}")

    print(f"\nTotal files modified: {modified}")


if __name__ == "__main__":
    main()
