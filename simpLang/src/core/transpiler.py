"""
SimpLang Transpiler
Converts .simp files into Python code.
Handles:
  - if / else / end  → Python if/else with indentation
  - loop while / loop x = a to b / loop x in y → Python loops
  - fun name(args) → def name(args):
  - end → de-indent
  - say() → print(), ask() → input()
  - yeah/nah/nope → True/False/None
  - Comments with //
"""

import re

try:
    from . import stdlib  # noqa: F401
except ImportError:
    import stdlib  # noqa: F401


def transpile(code: str) -> str:
    """Convert SimpLang code to Python code with proper indentation."""
    lines = code.split("\n")
    output_lines = []
    indent_level = 0
    indent_size = 4

    for raw_line in lines:
        stripped = raw_line.strip()

        # Preserve empty lines
        if not stripped:
            output_lines.append("")
            continue

        # --- Remove inline comments (//) ---
        processed = ""
        i = 0
        str_char = None
        while i < len(stripped):
            ch = stripped[i]
            if ch in ('"', "'") and (i == 0 or stripped[i - 1] != "\\"):
                if str_char is None:
                    str_char = ch
                elif str_char == ch:
                    str_char = None
                processed += ch
            elif ch == "/" and i + 1 < len(stripped) and stripped[i + 1] == "/":
                if str_char is None:
                    break
                else:
                    processed += ch
            else:
                processed += ch
            i += 1

        line = processed.strip()
        if not line:
            output_lines.append("")
            continue

        # --- Handle "end" keyword (de-indent) ---
        if line == "end":
            indent_level = max(0, indent_level - 1)
            indent = " " * (indent_level * indent_size)
            output_lines.append(indent + "pass")
            continue

        # --- Handle lines that INCREASE indent ---
        increases_indent = False
        transformed = line

        # if condition → if condition:
        if re.match(r"^if\s+(.+)$", transformed):
            if_match = re.match(r"^if\s+(.+)$", transformed)
            transformed = "if " + if_match.group(1) + ":"
            increases_indent = True

        # else: (de-indent first, write at if level, then re-indent)
        if transformed.strip() == "else":
            indent_level = max(0, indent_level - 1)
            indent = " " * (indent_level * indent_size)
            transformed = "else:"
            output_lines.append(indent + transformed)
            indent_level += 1
            continue

        # loop while condition → while condition:
        if re.match(r"^loop\s+while\s+(.+)$", transformed):
            while_match = re.match(r"^loop\s+while\s+(.+)$", transformed)
            transformed = "while " + while_match.group(1) + ":"
            increases_indent = True

        # loop varname = start to end
        if re.match(r"^loop\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+)$", transformed):
            loop_range_match = re.match(
                r"^loop\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+)$", transformed
            )
            var = loop_range_match.group(1)
            start = loop_range_match.group(2)
            end = loop_range_match.group(3)
            transformed = f"for {var} in range({start}, ({end}) + 1):"
            increases_indent = True

        # loop varname in iterable
        if re.match(r"^loop\s+(\w+)\s+in\s+(.+)$", transformed):
            loop_in_match = re.match(r"^loop\s+(\w+)\s+in\s+(.+)$", transformed)
            var = loop_in_match.group(1)
            iterable = loop_in_match.group(2)
            transformed = f"for {var} in {iterable}:"
            increases_indent = True

        # fun name(args) → def name(args):
        if re.match(r"^fun\s+(\w+)\s*(\(.*\))\s*$", transformed):
            fun_match = re.match(r"^fun\s+(\w+)\s*(\(.*\))\s*$", transformed)
            name = fun_match.group(1)
            params = fun_match.group(2)
            transformed = f"def {name}{params}:"
            increases_indent = True

        # --- Keyword replacements ---
        # Logical operators and comparisons
        transformed = transformed.replace('&&', 'and').replace('||', 'or')
        transformed = transformed.replace('&', 'and').replace('|', 'or')
        transformed = re.sub(r"\bis\s+not\b", "!=", transformed)
        transformed = re.sub(r"\bis\s+bigger\s+than\b", ">", transformed)
        transformed = re.sub(r"\bis\s+smaller\s+than\b", "<", transformed)
        transformed = re.sub(r"\bis\s+equal\s+to\b", "==", transformed)
        transformed = re.sub(r"\bis\s+smaller\b", "<", transformed)
        transformed = re.sub(r"\bis\s+bigger\b", ">", transformed)

        # say() → print()
        transformed = re.sub(r"\bsay\s*\(", "print(", transformed)
        # ask() → input()
        transformed = re.sub(r"\bask\s*\(", "input(", transformed)

        # Type keywords (standalone only, not in convert_to_* names)
        transformed = re.sub(r"(?<![a-zA-Z0-9_])num\b", "int", transformed)
        transformed = re.sub(r"(?<![a-zA-Z0-9_])dec\b", "float", transformed)
        transformed = re.sub(r"(?<![a-zA-Z0-9_])txt\b", "str", transformed)

        # Booleans / None
        transformed = re.sub(r"\byeah\b", "True", transformed)
        transformed = re.sub(r"\bnah\b", "False", transformed)
        transformed = re.sub(r"\bnope\b", "None", transformed)

        # Return
        transformed = re.sub(r"\bret\b", "return", transformed)

        # Import
        transformed = re.sub(r"\bimport\s+", "import ", transformed)

        # --- Write the line ---
        indent = " " * (indent_level * indent_size)
        output_lines.append(indent + transformed)

        if increases_indent:
            indent_level += 1

    return "\n".join(output_lines)


def transpile_file(input_path: str, output_path: str = None):
    """Read a .simp file, transpile it, and optionally write to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        code = f.read()

    python_code = transpile(code)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"Transpiled: {input_path} > {output_path}")
    else:
        if input_path.endswith(".simp"):
            output_path = input_path[:-5] + ".py"
        else:
            output_path = input_path + ".py"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"Transpiled: {input_path} > {output_path}")

    return python_code