#!/usr/bin/env python3
"""
SimpLang v2.0 - The Straightforward Programming Language
=========================================================
Full AST pipeline | Clear error messages | Stable functions
Modules | Interactive REPL

Just run:  python simp.py yourfile.simp
REPL:     python simp.py repl
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

# Import the SimpLang modules
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
    print("     SimpLang v2.0")
    print("     Code so simple, it clicks.")
    print("  ==========================================")
    print()


def print_usage():
    print_banner()
    print("  Commands:")
    print("    python simp.py <file.simp>       Run a SimpLang file")
    print("    python simp.py run <file.simp>   Run a SimpLang file")
    print("    python simp.py build <file.simp> Transpile to Python")
    print("    python simp.py build <in> <out>  Transpile with custom output")
    print("    python simp.py repl              Interactive REPL")
    print("    python simp.py test              Run tests")
    print("    python simp.py demo              Show demo programs")
    print("    python simp.py help              Show this help")
    print()


def run_simp_file(filepath):
    """Compile and run a .simp file using the AST pipeline."""
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
        "SimpLang_input": stdlib.simp_input,
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
    """Transpile a .simp file to .py."""
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
        if infile.endswith(".simp"):
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
            path = os.path.join(SIMPLANG_DIR, "examples", f"{demo}.simp")
            if os.path.exists(path):
                print(f"    python simp.py examples/{demo}.simp")
        print()
        print("  Modules Demo:")
        print("    python simp.py src/myutils.simp")
        print()
        return

    if command == "run":
        if len(sys.argv) < 3:
            print("  Usage: python simp.py run <file.simp>")
            return
        run_simp_file(sys.argv[2])
        return

    if command == "build":
        if len(sys.argv) < 3:
            print("  Usage: python simp.py build <file.simp> [output.py]")
            return
        infile = sys.argv[2]
        outfile = sys.argv[3] if len(sys.argv) > 3 else None
        build_simp_file(infile, outfile)
        return

    # Default: treat first argument as a file to run
    if command.endswith(".simp"):
        run_simp_file(command)
    else:
        print(f"  Unknown command or file: {command}")
        print("  Run 'python simp.py help' for usage.")


if __name__ == "__main__":
    main()