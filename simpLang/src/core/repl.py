"""
SimpLang REPL — Interactive programming environment.
Type commands directly and see results instantly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from .lexer import Lexer, LexerError
    from .parser import Parser, ParserError
    from .codegen import CodeGenerator
    from . import stdlib
except ImportError:
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from codegen import CodeGenerator
    import stdlib


class SimpLangREPL:
    """Interactive SimpLang REPL."""

    def __init__(self):
        self.globals = {
            "__builtins__": __builtins__,
            "SimpLang_input": stdlib.simp_input,
            "convert_to_txt": stdlib.convert_to_txt,
            "convert_to_num": stdlib.convert_to_num,
            "convert_to_decimal": stdlib.convert_to_decimal,
            "convert_to_dec": stdlib.convert_to_decimal,
            "convert_to_list": stdlib.convert_to_list,
            "type_of": stdlib.get_type,
            "get_type": stdlib.get_type,
            "stdlib": stdlib,
        }
        self.codegen = CodeGenerator()
        self.history = []

    def print_welcome(self):
        print()
        print("  ╔══════════════════════════════════════╗")
        print("  ║     SimpLang REPL v1.0               ║")
        print("  ║     Type 'help' for commands          ║")
        print("  ║     Ctrl+C or 'exit' to quit          ║")
        print("  ╚══════════════════════════════════════╝")
        print()

    def print_help(self):
        print()
        print("  SimpLang REPL Commands:")
        print("  ------------------------")
        print("  exit, quit    — Exit the REPL")
        print("  help           — Show this help")
        print("  vars           — Show defined variables")
        print("  clear          — Clear screen")
        print("  <any code>     — Type SimpLang code directly")
        print()
        print("  You can type things like:")
        print("    say('hello!')")
        print("    x = 5 + 3")
        print("    if x > 5  say('big')  end")
        print("    stdlib.math_random(1, 10)")
        print()

    def execute(self, code: str):
        """Compile and run a single line or block of SimpLang code."""
        try:
            # Lex
            lexer = Lexer(code, "<repl>")
            tokens = lexer.tokenize()

            # Skip if only EOF
            if len(tokens) <= 1:
                return

            # Parse
            parser = Parser(tokens, "<repl>")
            program = parser.parse()

            # Code gen
            py_code = self.codegen.generate(program)

            # Execute
            if py_code.strip():
                compiled = compile(py_code, "<repl>", "exec")
                exec(compiled, self.globals)

        except (LexerError, ParserError) as e:
            print(f"  Error: {e}")
        except SyntaxError as e:
            print(f"  Syntax Error: {e}")
        except Exception as e:
            print(f"  Runtime Error: {type(e).__name__}: {e}")

    def run(self):
        """Run the REPL interactive loop."""
        self.print_welcome()

        while True:
            try:
                code = input("  ⟫ ")

                if not code.strip():
                    continue

                if code.strip() in ("exit", "quit"):
                    print("  Goodbye!")
                    break

                if code.strip() == "help":
                    self.print_help()
                    continue

                if code.strip() == "vars":
                    print("  Variables:")
                    for k, v in sorted(self.globals.items()):
                        if not k.startswith("_") and k not in (
                            "__builtins__", "SimpLang_input",
                            "convert_to_txt", "convert_to_num",
                            "convert_to_dec", "convert_to_list",
                            "type_of", "stdlib"
                        ):
                            print(f"    {k} = {repr(v)}")
                    continue

                if code.strip() == "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    self.print_welcome()
                    continue

                self.history.append(code)
                self.execute(code)

            except KeyboardInterrupt:
                print()
                print("  Goodbye!")
                break
            except EOFError:
                print()
                break


def run_repl():
    """Entry point for the REPL."""
    repl = SimpLangREPL()
    repl.run()


if __name__ == "__main__":
    run_repl()