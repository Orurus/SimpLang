#!/usr/bin/env python3
"""
Understandable Code v2.0 - The Straightforward Programming Language
=========================================================
Full AST pipeline | Clear error messages | Stable functions
Modules | Interactive REPL

Just run:  python understand.py yourfile.und
REPL:     python understand.py repl
"""

import sys
import os

# Add src and module directories to the Python path
_SIMPLANG_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.join(_SIMPLANG_DIR, "src")
_CORE_DIR = os.path.join(_SRC_DIR, "core")
_MODULES_DIR = os.path.join(_SRC_DIR, "modules")
for candidate in (_SRC_DIR, _CORE_DIR, _MODULES_DIR):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

# Import the UnderstandableCode modules
from core.lexer import Lexer, LexerError
from core.parser import Parser, ParserError
from core.codegen import CodeGenerator, compile_simp_to_py
from core.repl import run_repl
from core import stdlib

# Expose directory for other functions to use
SIMPLANG_DIR = _SIMPLANG_DIR


def print_banner():
    print()
    print("  ==========================================")
    print("     UnderstandableCode v2.0")
    print("     Code so simple, it clicks.")
    print("  ==========================================")
    print()


def print_usage():
    print_banner()
    print("  Commands:")
    print("    python understand.py <file.und>       Run a UnderstandableCode file")
    print("    python understand.py run <file.und>   Run a UnderstandableCode file")
    print("    python understand.py build <file.und> Transpile to Python")
    print("    python understand.py build <in> <out>  Transpile with custom output")
    print("    python understand.py repl              Interactive REPL")
    print("    python understand.py test              Run tests")
    print("    python understand.py demo              Show demo programs")
    print("    python understand.py help              Show this help")
    print()


def run_simp_file(filepath):
    """Compile and run a .und file using the AST pipeline."""
    if not os.path.exists(filepath):
        print(f"  Error: File '{filepath}' not found!")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        python_code = compile_simp_to_py(source, filepath)
    except (LexerError, ParserError) as e:
        print(f"  Compilation Error: {e}")
        return
    except Exception as e:
        print(f"  Unexpected Error: {e}")
        return

    exec_globals = {
        "__builtins__": __builtins__,
        "stdlib": stdlib,
        "convert_to_txt": stdlib.convert_to_txt,
        "convert_to_num": stdlib.convert_to_num,
        "convert_to_decimal": stdlib.convert_to_decimal,
        "convert_to_dec": stdlib.convert_to_decimal,
        "convert_to_list": stdlib.convert_to_list,
        "type_of": stdlib.get_type,
        "get_type": stdlib.get_type,
        "UnderstandableCode_input": stdlib.und_input,
    }
    # Inject all stdlib math/string/list functions into globals
    for name in dir(stdlib):
        if not name.startswith("_"):
            exec_globals[name] = getattr(stdlib, name)

    try:
        compiled = compile(python_code, filepath, "exec")
        exec(compiled, exec_globals)
    except Exception as e:
        import traceback
        print(f"  Runtime Error: {e}")
        traceback.print_exc()


def build_simp_file(infile, outfile=None):
    """Transpile a .und file to .py."""
    if not os.path.exists(infile):
        print(f"  Error: File '{infile}' not found!")
        return

    with open(infile, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        python_code = compile_simp_to_py(source, infile)
    except (LexerError, ParserError) as e:
        print(f"  Compilation Error: {e}")
        return

    if outfile is None:
        if infile.endswith(".und"):
            outfile = infile[:-5] + ".py"
        else:
            outfile = infile + ".py"

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(python_code)
    print(f"  Transpiled: {infile} -> {outfile}")


def run_tests():
    """Run the test suite."""
    print_banner()
    print("  Running tests...")
    print()

    old_cwd = os.getcwd()
    os.chdir(SIMPLANG_DIR)
    try:
        import test_simplang
        success = test_simplang.main()
    finally:
        os.chdir(old_cwd)

    return success


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command in ("help", "--help", "-h"):
        print_usage()
        return

    if command == "repl":
        run_repl()
        return

    if command == "test":
        run_tests()
        return

    if command == "demo":
        print_banner()
        print("  Demo Programs")
        print()
        for demo in ["hello", "calculator", "guess"]:
            path = os.path.join(SIMPLANG_DIR, "examples", f"{demo}.und")
            if os.path.exists(path):
                print(f"    python understand.py examples/{demo}.und")
        print()
        print("  Modules Demo:")
        print("    python understand.py src/myutils.und")
        print()
        return

    if command == "run":
        if len(sys.argv) < 3:
            print("  Usage: python understand.py run <file.und>")
            return
        run_simp_file(sys.argv[2])
        return

    if command == "build":
        if len(sys.argv) < 3:
            print("  Usage: python understand.py build <file.und> [output.py]")
            return
        infile = sys.argv[2]
        outfile = sys.argv[3] if len(sys.argv) > 3 else None
        build_simp_file(infile, outfile)
        return

    # Default: treat first argument as a file to run
    if command.endswith(".und"):
        run_simp_file(command)
    else:
        print(f"  Unknown command or file: {command}")
        print("  Run 'python understand.py help' for usage.")


if __name__ == "__main__":
    main()