"""
SimpLang Lexer — Tokenizes source code into tokens with position info.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Token:
    """A single token with its type, value, and position."""
    type: str  # e.g. 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'STRING', etc.
    value: str
    line: int
    col: int
    source: str = ""

    def pos_str(self):
        if self.source:
            return f"{self.source}:{self.line}:{self.col}"
        return f"line {self.line}, col {self.col}"

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.pos_str()})"


# Token types
TOKEN = {
    # Keywords
    'SAY': 'SAY',
    'ASK': 'ASK',
    'IF': 'IF',
    'ELSE': 'ELSE',
    'ELIF': 'ELIF',
    'ELSEIF': 'ELSEIF',
    'END': 'END',
    'LOOP': 'LOOP',
    'WHILE': 'WHILE',
    'TO': 'TO',
    'IN': 'IN',
    'FUN': 'FUN',
    'RET': 'RET',
    'IMPORT': 'IMPORT',
    'EXPORT': 'EXPORT',
    'YEAH': 'YEAH',
    'NAH': 'NAH',
    'NOPE': 'NOPE',
    'NUM': 'NUM',
    'DEC': 'DEC',
    'TXT': 'TXT',
    'DICT': 'DICT',
    'AND': 'AND',
    'OR': 'OR',
    'NOT': 'NOT',
    'IS': 'IS',
    'BIGGER': 'BIGGER',
    'SMALLER': 'SMALLER',
    'EQUAL': 'EQUAL',
    'THAN': 'THAN',
    # Literals / identifiers
    'IDENTIFIER': 'IDENTIFIER',
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    # Operators
    'PLUS': 'PLUS',
    'MINUS': 'MINUS',
    'MUL': 'MUL',
    'DIV': 'DIV',
    'MOD': 'MOD',
    'EQ': 'EQ',
    'NEQ': 'NEQ',
    'LT': 'LT',
    'GT': 'GT',
    'LTE': 'LTE',
    'GTE': 'GTE',
    'ASSIGN': 'ASSIGN',
    # Punctuation
    'LPAREN': 'LPAREN',
    'RPAREN': 'RPAREN',
    'LBRACKET': 'LBRACKET',
    'RBRACKET': 'RBRACKET',
    'LBRACE': 'LBRACE',
    'RBRACE': 'RBRACE',
    'COMMA': 'COMMA',
    'DOT': 'DOT',
    'COLON': 'COLON',
    # End of file
    'EOF': 'EOF',
}


KEYWORDS = {
    'say': TOKEN['SAY'],
    'ask': TOKEN['ASK'],
    'if': TOKEN['IF'],
    'else': TOKEN['ELSE'],
    'elif': TOKEN['ELIF'],
    'else if': TOKEN['ELSEIF'],
    'end': TOKEN['END'],
    'loop': TOKEN['LOOP'],
    'while': TOKEN['WHILE'],
    'to': TOKEN['TO'],
    'in': TOKEN['IN'],
    'fun': TOKEN['FUN'],
    'ret': TOKEN['RET'],
    'import': TOKEN['IMPORT'],
    'export': TOKEN['EXPORT'],
    'yeah': TOKEN['YEAH'],
    'nah': TOKEN['NAH'],
    'nope': TOKEN['NOPE'],
    'num': TOKEN['NUM'],
    'dec': TOKEN['DEC'],
    'txt': TOKEN['TXT'],
    'dict': TOKEN['DICT'],
    'and': TOKEN['AND'],
    'or': TOKEN['OR'],
    'not': TOKEN['NOT'],
    'is': TOKEN['IS'],
    'bigger': TOKEN['BIGGER'],
    'smaller': TOKEN['SMALLER'],
    'equal': TOKEN['EQUAL'],
    'than': TOKEN['THAN'],
}


class SimpLangError(Exception):
    """Base error with position info."""
    def __init__(self, message: str, line: int = 0, col: int = 0, source: str = ""):
        self.line = line
        self.col = col
        self.source = source
        location = f"{source}:{line}:{col}" if source else f"line {line}, col {col}"
        super().__init__(f"Error at {location}: {message}")


class LexerError(SimpLangError):
    """Lexer-specific error."""
    pass


class Lexer:
    """Tokenizes SimpLang source code."""

    def __init__(self, source: str, filename: str = "<unknown>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []

    def error(self, message: str) -> LexerError:
        return LexerError(message, self.line, self.col, self.filename)

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return '\0'

    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source):
            ch = self.peek()
            if ch in ' \t\r\n':
                self.advance()
            else:
                break

    def skip_comment(self):
        # Skip to end of line
        while self.pos < len(self.source) and self.peek() != '\n':
            self.advance()

    def read_string(self, quote: str) -> str:
        """Read a string literal."""
        value = ""
        self.advance()  # skip opening quote
        while self.pos < len(self.source):
            ch = self.peek()
            if ch == '\\':
                self.advance()
                next_ch = self.advance()
                escapes = {'n': '\n', 't': '\t', '\\': '\\', '"': '"', "'": "'"}
                value += escapes.get(next_ch, next_ch)
            elif ch == quote:
                self.advance()  # skip closing quote
                return value
            else:
                value += self.advance()
        raise self.error("Unterminated string")

    def read_number(self) -> str:
        """Read a numeric literal."""
        value = ""
        has_dot = False
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isdigit():
                value += self.advance()
            elif ch == '.' and not has_dot:
                has_dot = True
                value += self.advance()
            else:
                break
        return value

    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        value = ""
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isalnum() or ch == '_':
                value += self.advance()
            else:
                break
        return value

    def tokenize(self) -> list:
        """Convert source code into a list of Tokens."""
        tokens = []

        while self.pos < len(self.source):
            line = self.line
            col = self.col
            ch = self.peek()

            # Whitespace
            if ch in ' \t\r\n':
                self.skip_whitespace()
                continue

            # Comments
            if ch == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue

            # Strings
            if ch in ('"', "'"):
                value = self.read_string(ch)
                tokens.append(Token(TOKEN['STRING'], value, line, col, self.filename))
                continue

            # Numbers
            if ch.isdigit() or (ch == '.' and self.peek(1).isdigit()):
                value = self.read_number()
                tokens.append(Token(TOKEN['NUMBER'], value, line, col, self.filename))
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                value = self.read_identifier()
                tok_type = KEYWORDS.get(value, TOKEN['IDENTIFIER'])
                tokens.append(Token(tok_type, value, line, col, self.filename))
                continue

            # Multi-character operators
            next_ch = self.peek(1) if self.pos + 1 < len(self.source) else '\0'

            if ch == '=' and next_ch == '=':
                tokens.append(Token(TOKEN['EQ'], '==', line, col, self.filename))
                self.advance()
                self.advance()
                continue
            if ch == '&' and next_ch == '&':
                tokens.append(Token(TOKEN['AND'], 'and', line, col, self.filename))
                self.advance()
                self.advance()
                continue
            if ch == '|' and next_ch == '|':
                tokens.append(Token(TOKEN['OR'], 'or', line, col, self.filename))
                self.advance()
                self.advance()
                continue
            if ch == '&':
                tokens.append(Token(TOKEN['AND'], 'and', line, col, self.filename))
                self.advance()
                continue
            if ch == '|':
                tokens.append(Token(TOKEN['OR'], 'or', line, col, self.filename))
                self.advance()
                continue
            if ch == '!' and next_ch == '=':
                tokens.append(Token(TOKEN['NEQ'], '!=', line, col, self.filename))
                self.advance()
                self.advance()
                continue
            if ch == '<' and next_ch == '=':
                tokens.append(Token(TOKEN['LTE'], '<=', line, col, self.filename))
                self.advance()
                self.advance()
                continue
            if ch == '>' and next_ch == '=':
                tokens.append(Token(TOKEN['GTE'], '>=', line, col, self.filename))
                self.advance()
                self.advance()
                continue

            # Single-character operators and punctuation
            single_map = {
                '+': TOKEN['PLUS'],
                '-': TOKEN['MINUS'],
                '*': TOKEN['MUL'],
                '/': TOKEN['DIV'],
                '%': TOKEN['MOD'],
                '=': TOKEN['ASSIGN'],
                '<': TOKEN['LT'],
                '>': TOKEN['GT'],
                '(': TOKEN['LPAREN'],
                ')': TOKEN['RPAREN'],
                '[': TOKEN['LBRACKET'],
                ']': TOKEN['RBRACKET'],
                '{': TOKEN['LBRACE'],
                '}': TOKEN['RBRACE'],
                ',': TOKEN['COMMA'],
                '.': TOKEN['DOT'],
                ':': TOKEN['COLON'],
            }
            if ch in single_map:
                tokens.append(Token(single_map[ch], ch, line, col, self.filename))
                self.advance()
                continue

            raise self.error(f"Unexpected character: '{ch}'")

        tokens.append(Token(TOKEN['EOF'], '', self.line, self.col, self.filename))
        return tokens