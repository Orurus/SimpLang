"""
SimpLang Code Generator — Walks the AST and produces Python code.
Also handles module imports (modules beyond stdlib).
"""

import os
import sys

try:
    from .ast_nodes import *
    from .lexer import Lexer
    from .parser import Parser
except ImportError:
    from ast_nodes import *
    from lexer import Lexer
    from parser import Parser


# Python reserved keywords that need to be renamed
PYTHON_KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
    'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
    'raise', 'return', 'try', 'while', 'with', 'yield'
}

# Additional Python builtins that should be avoided as variable names
PYTHON_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',
    'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod',
    'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr',
    'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
    'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min',
    'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range',
    'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'str', 'sum',
    'super', 'tuple', 'type', 'vars', 'zip', '__import__'
}

# Map SimpLang identifiers that conflict with Python keywords
IDENTIFIER_MAP = {
    'pass': 'pass_val',  # 'pass' is a Python keyword
}


class CodeGenError(Exception):
    """Error during code generation."""
    pass


class CodeGenerator:
    """Converts AST into Python source code."""

    def __init__(self):
        self.indent_level = 0
        self.indent_size = 4
        self.lines = []
        # Track function names for scope analysis
        self.function_names = set()
        # Module system
        self.loaded_modules = {}

    def indent(self):
        return " " * (self.indent_level * self.indent_size)

    def emit(self, code: str = ""):
        if code:
            self.lines.append(self.indent() + code)
        else:
            self.lines.append("")

    def generate(self, program: Program) -> str:
        """Generate Python code from a Program AST node."""
        self.lines = []
        self.indent_level = 0
        self.function_names = set()

        for stmt in program.statements:
            self.gen_statement(stmt)

        return "\n".join(self.lines)

    def gen_statement(self, stmt):
        """Generate code for a single statement."""
        if isinstance(stmt, SayStmt):
            self.emit(f"print({self.gen_expression(stmt.expr)})")

        elif isinstance(stmt, AskStmt):
            if stmt.expr:
                self.emit(f"SimpLang_input({self.gen_expression(stmt.expr)})")
            else:
                self.emit("SimpLang_input()")

        elif isinstance(stmt, AssignStmt):
            target = self.gen_expression(stmt.target) if stmt.target is not None else stmt.name
            self.emit(f"{target} = {self.gen_expression(stmt.expr)}")

        elif isinstance(stmt, IfStmt):
            self.emit(f"if {self.gen_expression(stmt.condition)}:")
            self.indent_level += 1
            for s in stmt.body:
                self.gen_statement(s)
            self.indent_level -= 1
            
            # Handle elif clauses
            for elif_clause in stmt.elif_clauses:
                self.emit(f"elif {self.gen_expression(elif_clause.condition)}:")
                self.indent_level += 1
                for s in elif_clause.body:
                    self.gen_statement(s)
                self.indent_level -= 1
            
            # Handle else body
            if stmt.else_body:
                self.emit("else:")
                self.indent_level += 1
                for s in stmt.else_body:
                    self.gen_statement(s)
                self.indent_level -= 1

        elif isinstance(stmt, WhileLoop):
            self.emit(f"while {self.gen_expression(stmt.condition)}:")
            self.indent_level += 1
            for s in stmt.body:
                self.gen_statement(s)
            self.indent_level -= 1

        elif isinstance(stmt, ForRangeLoop):
            self.emit(
                f"for {stmt.var_name} in range({self.gen_expression(stmt.start)}, "
                f"({self.gen_expression(stmt.end)}) + 1):"
            )
            self.indent_level += 1
            for s in stmt.body:
                self.gen_statement(s)
            self.indent_level -= 1

        elif isinstance(stmt, ForInLoop):
            self.emit(
                f"for {stmt.var_name} in {self.gen_expression(stmt.iterable)}:"
            )
            self.indent_level += 1
            for s in stmt.body:
                self.gen_statement(s)
            self.indent_level -= 1

        elif isinstance(stmt, FunDef):
            self.function_names.add(stmt.name)
            params = ", ".join(stmt.params)
            self.emit(f"def {stmt.name}({params}):")
            self.indent_level += 1
            for s in stmt.body:
                self.gen_statement(s)
            self.indent_level -= 1

        elif isinstance(stmt, ReturnStmt):
            self.emit(f"return {self.gen_expression(stmt.expr)}")

        elif isinstance(stmt, ImportStmt):
            # Handle stdlib and custom module imports.
            if stmt.name == "stdlib":
                self.emit("import sys, os")
                self.emit("_simp_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src') if '__file__' in dir() else 'src'")
                self.emit("sys.path.insert(0, _simp_src)")
                self.emit("import core.stdlib as __simp_stdlib__")
                self.emit("stdlib = __simp_stdlib__")
            else:
                self.emit("import sys, os")
                self.emit("_simp_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src') if '__file__' in dir() else 'src'")
                self.emit("sys.path.insert(0, _simp_src)")
                self.emit("from modules.loader import load_simp_module")
                self.emit(f"{stmt.name.split('/')[-1].split('.')[-2] if '.' in stmt.name else stmt.name} = load_simp_module('{stmt.name}')")
            self.loaded_modules[stmt.name] = True

        elif isinstance(stmt, ExprStmt):
            expr_code = self.gen_expression(stmt.expr)
            if expr_code:
                self.emit(expr_code)

    def gen_expression(self, expr) -> str:
        """Generate Python code for an expression AST node."""
        if isinstance(expr, NumberLiteral):
            return str(expr.value)

        if isinstance(expr, StringLiteral):
            # Escape for Python
            val = expr.value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            return f'"{val}"'

        if isinstance(expr, BoolLiteral):
            return "True" if expr.value else "False"

        if isinstance(expr, NoneLiteral):
            return "None"

        if isinstance(expr, Identifier):
            # Check for Python keyword conflicts and rename
            if expr.name in IDENTIFIER_MAP:
                return IDENTIFIER_MAP[expr.name]
            return expr.name

        if isinstance(expr, BinaryOp):
            left = self.gen_expression(expr.left)
            right = self.gen_expression(expr.right)
            if expr.op == '=':
                return f"{left} = {right}"
            return f"({left} {expr.op} {right})"

        if isinstance(expr, UnaryOp):
            right = self.gen_expression(expr.right)
            return f"({expr.op} {right})"

        if isinstance(expr, Call):
            func = self.gen_expression(expr.func)
            # Convert stdlib["function"] to stdlib.function
            if isinstance(expr.func, Subscript) and isinstance(expr.func.index, StringLiteral):
                func = f"{self.gen_expression(expr.func.expr)}.{expr.func.index.value}"
            args = ", ".join(self.gen_expression(a) for a in expr.args)
            return f"{func}({args})"

        if isinstance(expr, ListLiteral):
            items = ", ".join(self.gen_expression(i) for i in expr.items)
            return f"[{items}]"

        if isinstance(expr, Subscript):
            obj = self.gen_expression(expr.expr)
            index = self.gen_expression(expr.index)
            return f"{obj}[{index}]"

        if isinstance(expr, DictLiteral):
            items = ", ".join(
                f"{self.gen_dict_key(item.key)}: {self.gen_expression(item.value)}"
                for item in expr.items
            )
            return f"{{{items}}}"

    def gen_dict_key(self, key_expr) -> str:
        """Convert dict key to Python string key."""
        if isinstance(key_expr, StringLiteral):
            return self.gen_expression(key_expr)
        if isinstance(key_expr, Identifier):
            # Convert identifier to string key
            return f'"{key_expr.name}"'
        # For other types, use the expression directly (may need quotes)
        return f'"{self.gen_expression(key_expr)}"'

        if isinstance(expr, DictItem):
            # DictItem is only used internally in DictLiteral
            return f"{self.gen_expression(expr.key)}: {self.gen_expression(expr.value)}"

        if isinstance(expr, CallMethod):
            obj = self.gen_expression(expr.obj)
            args = ", ".join(self.gen_expression(a) for a in expr.args)
            return f"{obj}.{expr.method}({args})"

        return ""


def compile_simp_to_py(source_code: str, source_file: str = "<unknown>") -> str:
    """Full pipeline: Lex → Parse → CodeGen → Python code."""
    # Lex
    lexer = Lexer(source_code, source_file)
    tokens = lexer.tokenize()

    # Parse
    parser = Parser(tokens, source_file)
    program = parser.parse()

    # Code generation
    gen = CodeGenerator()
    return "# SimpLang compiled output\n# (Auto-generated — do not edit directly)\n" + gen.generate(program)
