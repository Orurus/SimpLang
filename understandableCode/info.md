# Understandble Code v2.0 — The Straightforward Language

> **"Code so simple, it clicks."**

UnderstandableCode is a custom programming language designed to be **extremely straightforward**. It reads like English, keeps symbols available for power users, and compiles directly into Python.

The current version also includes:
- natural-language comparisons such as `is bigger than`, `is smaller than`, and `is equal to`
- natural-language logical operators such as `and` and `or`
- symbolic comparisons such as `>`, `<`, `==`, and `!=`
- symbolic logical operators such as `&&`, `||`, `&`, and `|`
- tensor and matrix helpers for ML-style experiments
- advanced ML helpers for attention, optimization, and training-state ideas
- **elif/else if support**: Chain multiple conditions with `elif` or `else if`
- **Dictionary support**: Store key-value pairs with `{key: value, ...}` syntax
- **Dictionary helpers**: Use `stdlib.dict_*` functions for managing dictionaries

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [How It Works](#how-it-works)
3. [Commands](#commands)
4. [Language Reference](#language-reference)
5. [Standard Library](#standard-library)
6. [Examples](#examples)
7. [Interactive REPL](#interactive-repl)
8. [Modules](#modules)
9. [Error Messages](#error-messages)
10. [Project Structure](#project-structure)

---

## Quick Start

```bash
cd understandableCode
python understand.py examples/hello.und
```

### Prerequisites

- **Python 3** installed on your computer
- That's it. No other dependencies.

---

## How It Works

UnderstandableCode uses a **proper compiler pipeline** (not regex):

```
yourfile.und  ──→  Lexer  ──→  Parser  ──→  Code Generator  ──→  Python  ──→  Runs!
```

The Lexer breaks code into tokens, the Parser builds an AST (Abstract Syntax Tree), and the Code Generator walks the tree to produce Python. This means **better error messages** and **stable, reliable code**.

### Keyword Cheat Sheet

| UnderstandableCode | Python | What it does |
|----------|--------|-------------|
| `say()` | `print()` | Prints text to the screen |
| `ask()` | `input()` | Gets input from the user |
| `if` | `if` | Checks a condition |
| `else` | `else` | Otherwise branch |
| `loop while` | `while` | Loop while a condition is true |
| `loop x = a to b` | `for x in range(a, b+1)` | Count from a to b |
| `loop x in y` | `for x in y` | Loop over items in a list |
| `is bigger than` | `>` | Compare values in a beginner-friendly way |
| `bigger than` | `>` | One symbolic comparison word + joining word |
| `is smaller than` | `<` | Compare values in a beginner-friendly way |
| `smaller or equal to` | `<=` | Use one symbolic word with optional joining words |
| `is equal to` | `==` | Check for equality |
| `is not` | `!=` | Check for inequality |
| `and` / `&&` / `&` | `and` | Combine conditions |
| `or` / `||` / `|` | `or` | Either condition |
| `elif` / `else if` | `elif` | Additional condition in if-block |
| `fun` | `def` | Define a function |
| `ret` | `return` | Return a value |
| `yeah` | `True` | Boolean true |
| `nah` | `False` | Boolean false |
| `nope` | `None` | Null/nothing |
| `end` | *(un-indent)* | Ends a block |
| `//` | `#` | Comment |

---

## Commands

```bash
python understand.py <file.und>       # Run a UnderstandableCode file
python understand.py run <file.und>   # Run a UnderstandableCode file
python understand.py build <file.und> # Transpile to Python (no run)
python understand.py build <in> <out>  # Transpile with custom output name
python understand.py repl              # Interactive REPL
python understand.py test              # Run the test suite
python understand.py demo              # Show demo programs
python understand.py help              # Show this help
```

---

## Language Reference

### Comments

```python
// This is a comment
x = 5  // This is also a comment
```

Comments start with `//` and go to end of line. They are removed during compilation.

### Variables

```python
name = "Alice"
age = 25
price = 19.99
is_cool = yeah
```

- Strings use `"double quotes"` or `'single quotes'`
- Numbers are plain digits
- Decimals (floats) use a dot

### Printing — say()

```python
say("Hello, World!")
say("The answer is " + convert_to_txt(42))
```

- `say()` prints text to the screen (like Python's `print()`)
- Use `convert_to_txt()` to turn numbers into text before joining with strings

### Input — ask()

```python
say("What's your name?")
name = ask()

say("How old are you?")
age = convert_to_num(ask())
```

- `ask()` reads a line from the user (always returns text)
- Use `convert_to_num()` to turn input into a number

### Types

| Keyword | What it does | Example |
|---------|-------------|---------|
| `num()` | Convert to whole number | `num("5")` → `5` |
| `dec()` | Convert to decimal | `dec("3.14")` → `3.14` |
| `txt()` | Convert to text | `txt(42)` → `"42"` |

### Conditions — if/else/end

UnderstandableCode supports both symbolic and English-driven comparisons.

- One symbolic comparison word such as `bigger`, `smaller`, or `equal`
- Optional joining words such as `is`, `than`, and `to`
- Use `and` / `or` only to connect separate full comparisons, not to chain comparison words together
- Examples: `guess is bigger than secret`, `guess bigger than secret`, `if guess is bigger and if guess is equal to secret`

```python
if score >= 100
    say("You win!")
end

if age < 18
    say("Child")
else
    say("Adult")
end
```

### Loops

**While loop:**
```python
x = 1
loop while x <= 5
    say(x)
    x = x + 1
end
```

**Count loop:**
```python
loop i = 1 to 10
    say(i)
end
```

**For-each loop:**
```python
fruits = ["apple", "banana", "cherry"]
loop fruit in fruits
    say(fruit)
end
```

### Functions — fun/ret/end

```python
fun add(a, b)
    ret a + b
end

result = add(5, 3)
say(result)  // 8
```

### Booleans

```python
is_happy = yeah     // True
is_tired = nah      // False
my_none = nope      // None (null)
```

### Dictionaries

```python
// Create a dictionary
person = {
    name: "Alice",     // Keys are bare identifiers (auto-converted to strings)
    age: 30,
    city: "New York"
}

// Access values - use QUOTED strings for bracket notation
say(person["name"])   // Use quotes!
say(person["age"])    // Use quotes!

// Use dict helpers
stdlib.dict_set(person, "email", "alice@example.com")
say(stdlib.dict_has(person, "email"))  // yeah

// Get all keys
loop key in stdlib.dict_keys(person)
    say(key + ": " + convert_to_txt(person[key]))
end

// Dot notation (for simple keys):
say(person.name)      // Equivalent to person["name"]
```

**Important**: Dictionary keys are bare identifiers that are automatically converted to strings. When accessing values with brackets, use quoted strings: `person["name"]`, not `person[name]` (which would look up a variable).

For more details, see [Dictionary Library](DICTIONARY_LIBRARY.md).

### Importing stdlib

```python
import stdlib

// Use stdlib functions:
result = stdlib.math_add(10, 5)
say(result)
```

Every function name in stdlib **tells you exactly what it does**.

---

## Standard Library

### Conversion Functions (built-in — no import needed)

These work anywhere without importing stdlib:

| Function | What it does | Example |
|----------|-------------|---------|
| `convert_to_text(value)` | Turn anything into text | `convert_to_txt(42)` → `"42"` |
| `convert_to_number(text)` | Turn text into a whole number | `convert_to_num("10")` → `10` |
| `convert_to_decimal(text)` | Turn text into a decimal | `convert_to_decimal("3.14")` → `3.14` |
| `convert_to_list(value)` | Split into a list of characters | `convert_to_list("hi")` → `["h", "i"]` |
| `get_type(value)` | Tell you the type of a value | `get_type("hi")` → `"txt"` |

---

### Math Functions (use with `stdlib.` prefix)

| Function | What it does | Example |
|----------|-------------|---------|
| `math_add(a, b)` | Add two numbers | `stdlib.math_add(5, 3)` → `8` |
| `math_subtract(a, b)` | Subtract b from a | `stdlib.math_subtract(10, 4)` → `6` |
| `math_multiply(a, b)` | Multiply two numbers | `stdlib.math_multiply(3, 7)` → `21` |
| `math_divide(a, b)` | Divide a by b | `stdlib.math_divide(10, 3)` → `3.33` |
| `math_power(base, exp)` | Raise base to the power of exp | `stdlib.math_power(2, 10)` → `1024` |
| `math_squareroot(n)` | Get the square root | `stdlib.math_squareroot(9)` → `3.0` |
| `math_absolute(n)` | Make a negative number positive | `stdlib.math_absolute(-5)` → `5` |
| `math_round(n, digits)` | Round to a number of decimal places | `stdlib.math_round(3.14159, 2)` → `3.14` |
| `math_bigger(a, b)` | Return the larger number | `stdlib.math_bigger(10, 5)` → `10` |
| `math_smaller(a, b)` | Return the smaller number | `stdlib.math_smaller(10, 5)` → `5` |
| `math_random(min, max)` | Get a random whole number between min and max | `stdlib.math_random(1, 100)` → `47` |
| `math_sum(list)` | Add up all numbers in a list | `stdlib.math_sum([1,2,3])` → `6` |
| `math_average(list)` | Get the average of numbers in a list | `stdlib.math_average([1,2,3])` → `2.0` |
| `math_is_even(n)` | Check if a number is even → yeah/nah | `stdlib.math_is_even(4)` → `yeah` |
| `math_is_odd(n)` | Check if a number is odd → yeah/nah | `stdlib.math_is_odd(5)` → `yeah` |

---

### String Functions (use with `stdlib.` prefix)

| Function | What it does | Example |
|----------|-------------|---------|
| `string_length(s)` | Count how many characters | `stdlib.string_length("hi")` → `2` |
| `string_uppercase(s)` | Convert to ALL CAPS | `stdlib.string_uppercase("hi")` → `"HI"` |
| `string_lowercase(s)` | Convert to all lowercase | `stdlib.string_lowercase("HI")` → `"hi"` |
| `string_reverse(s)` | Reverse a string backwards | `stdlib.string_reverse("abc")` → `"cba"` |
| `string_contains(text, word)` | Check if text contains a word → yeah/nah | `stdlib.string_contains("hello", "el")` → `yeah` |
| `string_starts_with(text, prefix)` | Check if text starts with something → yeah/nah | `stdlib.string_starts_with("hello", "he")` → `yeah` |
| `string_ends_with(text, suffix)` | Check if text ends with something → yeah/nah | `stdlib.string_ends_with("hello", "lo")` → `yeah` |
| `string_split(text, sep)` | Split a string into a list | `stdlib.string_split("a b c")` → `["a","b","c"]` |
| `string_join(list, glue)` | Join a list of strings into one | `stdlib.string_join(["a","b"], "-")` → `"a-b"` |
| `string_replace(text, old, new)` | Replace every occurrence of old with new | `stdlib.string_replace("hi hi", "hi", "yo")` → `"yo yo"` |
| `string_removespaces(text)` | Remove spaces from both ends | `stdlib.string_removespaces("  hi  ")` → `"hi"` |
| `string_getrange(text, start, end)` | Get a piece of a string | `stdlib.string_getrange("hello", 1, 4)` → `"ell"` |
| `string_getcharacter(text, pos)` | Get the character at a position | `stdlib.string_getcharacter("hello", 1)` → `"e"` |
| `string_count(text, word)` | Count how many times a word appears | `stdlib.string_count("hello hello", "hello")` → `2` |

---

### List Functions (use with `stdlib.` prefix)

| Function | What it does | Example |
|----------|-------------|---------|
| `list_length(lst)` | Count items in a list | `stdlib.list_length([1,2,3])` → `3` |
| `list_additem(lst, item)` | Add an item to the end | `stdlib.list_additem([1,2], 3)` → `[1,2,3]` |
| `list_additematstart(lst, item)` | Add an item to the beginning | `stdlib.list_additematstart([2,3], 1)` → `[1,2,3]` |
| `list_removelast(lst)` | Remove and return the last item | `stdlib.list_removelast([1,2,3])` → `3` |
| `list_removefirst(lst)` | Remove and return the first item | `stdlib.list_removefirst([1,2,3])` → `1` |
| `list_removeat(lst, index)` | Remove and return item at a position | `stdlib.list_removeat([1,2,3], 1)` → `2` |
| `list_removeitem(lst, item)` | Remove the first occurrence of an item | `stdlib.list_removeitem([1,2,3], 2)` → `[1,3]` |
| `list_sort_ascending(lst)` | Sort from smallest to biggest | `stdlib.list_sort_ascending([3,1,2])` → `[1,2,3]` |
| `list_sort_descending(lst)` | Sort from biggest to smallest | `stdlib.list_sort_descending([1,2,3])` → `[3,2,1]` |
| `list_reverse(lst)` | Reverse the order of items | `stdlib.list_reverse([1,2,3])` → `[3,2,1]` |
| `list_contains(lst, item)` | Check if a list has an item → yeah/nah | `stdlib.list_contains([1,2], 2)` → `yeah` |
| `list_findindex(lst, item)` | Find the position of an item (returns -1 if not found) | `stdlib.list_findindex(["a","b"], "b")` → `1` |
| `list_getitem(lst, index)` | Get the item at a position | `stdlib.list_getitem([10,20,30], 1)` → `20` |
| `list_getrange(lst, start, end)` | Get a piece of a list | `stdlib.list_getrange([1,2,3,4], 1, 3)` → `[2,3]` |
| `list_transform(lst, func)` | Apply a function to every item | `stdlib.list_transform([1,2,3], double)` |

---

### File I/O Functions (use with `stdlib.` prefix)

| Function | What it does | Example |
|----------|-------------|---------|
| `file_read(path)` | Read entire file as text | `stdlib.file_read("data.txt")` |
| `file_write(path, content)` | Write to a file (overwrites) | `stdlib.file_write("out.txt", "hello")` |
| `file_append(path, content)` | Add to the end of a file | `stdlib.file_append("log.txt", "new line")` |
| `file_exists(path)` | Check if a file exists → yeah/nah | `stdlib.file_exists("data.txt")` |
| `file_readlines(path)` | Read all lines into a list | `stdlib.file_readlines("data.txt")` |

---

### Time Functions (use with `stdlib.` prefix)

| Function | What it does | Example |
|----------|-------------|---------|
| `time_now()` | Get the current date and time | `stdlib.time_now()` → `"2026-06-11 22:30:00"` |
| `time_date()` | Get today's date | `stdlib.time_date()` → `"2026-06-11"` |
| `time_sleep(seconds)` | Pause the program | `stdlib.time_sleep(2)` (waits 2 seconds) |

---

## Examples

### Hello World

```bash
python understand.py examples/hello.und
```

```python
say("Hello, World!")
name = "Alex"
say("My name is " + name)

say("What's your name?")
user_name = ask()
say("Nice to meet you, " + user_name + "!")
```

### Calculator

```bash
python understand.py examples/calculator.und
```

```python
import stdlib

a = convert_to_num(ask("Enter first number: "))
b = convert_to_num(ask("Enter second number: "))

say("Add: " + stdlib.math_add(a, b))
say("Subtract: " + stdlib.math_subtract(a, b))
say("Multiply: " + stdlib.math_multiply(a, b))
say("Divide: " + stdlib.math_divide(a, b))
```

### Number Guessing Game

```bash
python understand.py examples/guess.und
```

```python
import stdlib

secret = stdlib.math_random(1, 100)
guess = 0

loop while guess != secret
    guess = convert_to_num(ask("Your guess: "))

    if guess < secret
        say("Too low!")
    end

    if guess > secret
        say("Too high!")
    end
end

say("You got it!")
```

---

## Interactive REPL

The REPL lets you type UnderstandableCode code directly and see results instantly.

```bash
python understand.py repl
```

```
  ╔══════════════════════════════════════╗
  ║     UnderstandableCode REPL v1.0               ║
  ║     Type 'help' for commands          ║
  ║     Ctrl+C or 'exit' to quit          ║
  ╚══════════════════════════════════════╝

  ⟫ say("hello!")
  hello!
  
  ⟫ x = 5 + 3 * 2
  
  ⟫ say(x)
  11
  
  ⟫ stdlib.math_random(1, 100)
  
  ⟫ vars
      x = 11
```

REPL Commands:
- `exit` / `quit` — exit the REPL
- `help` — show help
- `vars` — show all defined variables
- `clear` — clear the screen

---

## Modules

UnderstandableCode supports both built-in libraries and custom modules.

### Built-in ML and tensor helpers

The runtime now includes ML-oriented helpers under `src/modules/`:
- `tensor_matrix_library.py` — tensor shape inference, broadcast checks, and broadcasted addition
- `advanced_ml_library.py` — attention, optimizer state, training-loop helpers, and tensor-style utilities

You can import these modules from UnderstandableCode code using the same import system as other modules.

### Custom modules

You can create your own UnderstandableCode modules and import them!

Create a file `myutils.und`:
```python
fun greet(name)
    say("Hello, " + name + "!")
end

fun double(n)
    ret n * 2
end
```

Then use it from another file:
```python
import myutils
myutils.greet("Bob")
result = myutils.double(10)
say(result)
```

Run it like any other `.und` file:
```bash
python understand.py src/myutils.und
```

---

## Error Messages

UnderstandableCode v2.0 gives you **real error messages** with file name, line number, and column:

```
  Compilation Error: Error at examples/hello.und:11:6:
  Expected 'IDENTIFIER' but got '=' (ASSIGN)
```

Errors come from:
- **Lexer** — unexpected characters, unterminated strings
- **Parser** — wrong token types, missing keywords
- **Runtime** — Python exceptions with full tracebacks

---

## Project Structure

```
understandableCode/
├── understand.py                    # Main runner / CLI
├── README.md                  # This file
├── test_understandableCode.py           # Regression tests for the runtime
├── ADVANCED_ML_LIBRARY.md     # Notes on the ML helper upgrade path
├── TENSOR_MATRIX_LIBRARY.md   # Tensor and matrix helper reference
├── examples/
│   ├── hello.und             # Hello World example
│   ├── calculator.und        # Calculator example
│   ├── guess.und             # Number guessing game
│   └── importtest.und        # Import and module demo
└── src/
    ├── __init__.py
    ├── core/
    │   ├── lexer.py            # Tokenizes source code
    │   ├── parser.py           # Builds the AST
    │   ├── ast_nodes.py        # AST node types
    │   ├── codegen.py          # Emits Python code
    │   ├── repl.py             # Interactive REPL
    │   ├── stdlib.py           # Standard library helpers
    │   └── transpiler.py       # Legacy transpiler path
    └── modules/
        ├── tensor_matrix_library.py
        ├── advanced_ml_library.py
        └── myutils.und        # Example custom module
```

---

## Why UnderstandableCode?

- **No curly braces** — uses `end` to close blocks
- **Function names tell you exactly what they do** — `list_removelast`, not `pop`
- **Full Python power** — compiles to Python, so you can use any Python library
- **Built-in library** — math, strings, lists, files, time — all ready to go
- **Interactive REPL** — type code and see results instantly
- **Clear error messages** — knows exactly where things went wrong

UnderstandableCode is perfect for:
- Learning to code
- Quick scripts
- Teaching others
- Anyone who wants straightforward code

---

*Understandable Code v2.0 — "Code so simple, it clicks."*
