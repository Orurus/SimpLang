"""
UnderstandableCode AST Node definitions.
Each node represents a piece of code in the tree.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Position:
    """Line and column in source code."""
    line: int
    col: int
    source: str = ""

    def __str__(self):
        if self.source:
            return f"{self.source}:{self.line}:{self.col}"
        return f"line {self.line}, col {self.col}"


@dataclass
class Program:
    """Top-level program: a list of statements."""
    statements: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class SayStmt:
    """say(expression)"""
    expr: Any = None
    pos: Optional[Position] = None


@dataclass
class AskStmt:
    """ask(expression?)"""
    expr: Any = None
    pos: Optional[Position] = None


@dataclass
class AssignStmt:
    """target = expression"""
    name: str = ""
    target: Any = None
    expr: Any = None
    pos: Optional[Position] = None


@dataclass
class ElifClause:
    """elif condition: body"""
    condition: Any = None
    body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class IfStmt:
    """if condition: body [elif condition: body]* [else: else_body] end"""
    condition: Any = None
    body: list = field(default_factory=list)
    elif_clauses: list = field(default_factory=list)
    else_body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class WhileLoop:
    """loop while condition: body end"""
    condition: Any = None
    body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class ForRangeLoop:
    """loop var = start to end: body end"""
    var_name: str = ""
    start: Any = None
    end: Any = None
    body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class ForInLoop:
    """loop var in iterable: body end"""
    var_name: str = ""
    iterable: Any = None
    body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class FunDef:
    """fun name(params): body end"""
    name: str = ""
    params: list = field(default_factory=list)
    body: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class ReturnStmt:
    """ret expression"""
    expr: Any = None
    pos: Optional[Position] = None


@dataclass
class ImportStmt:
    """import name"""
    name: str = ""
    pos: Optional[Position] = None


@dataclass
class ExprStmt:
    """Expression used as a statement."""
    expr: Any = None
    pos: Optional[Position] = None


@dataclass
class BinaryOp:
    """Binary operation: left op right"""
    left: Any = None
    op: str = ""
    right: Any = None
    pos: Optional[Position] = None


@dataclass
class UnaryOp:
    """Unary operation: op right"""
    op: str = ""
    right: Any = None
    pos: Optional[Position] = None


@dataclass
class NumberLiteral:
    """Numeric literal."""
    value: Any = 0
    pos: Optional[Position] = None


@dataclass
class StringLiteral:
    """String literal."""
    value: str = ""
    pos: Optional[Position] = None


@dataclass
class BoolLiteral:
    """Boolean literal."""
    value: bool = False
    pos: Optional[Position] = None


@dataclass
class NoneLiteral:
    """None literal."""
    pos: Optional[Position] = None


@dataclass
class Identifier:
    """Variable name."""
    name: str = ""
    pos: Optional[Position] = None


@dataclass
class Call:
    """Function call: func(args)"""
    func: Any = None
    args: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class ListLiteral:
    """List literal: [items]"""
    items: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class Subscript:
    """Indexing: expr[index]"""
    expr: Any = None
    index: Any = None
    pos: Optional[Position] = None


@dataclass
class DictLiteral:
    """Dictionary literal: {key: value, ...}"""
    items: list = field(default_factory=list)
    pos: Optional[Position] = None


@dataclass
class DictItem:
    """A key-value pair in a dictionary."""
    key: Any = None
    value: Any = None
    pos: Optional[Position] = None


@dataclass
class CallMethod:
    """Method call: obj.method(args)"""
    obj: Any = None
    method: str = ""
    args: list = field(default_factory=list)
    pos: Optional[Position] = None