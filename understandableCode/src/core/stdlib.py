"""
===========================================
UnderstandableCode Standard Library (stdlib)
===========================================
Every function name tells you EXACTLY what it does.
No cryptic names here!

Usage in UnderstandableCode:
    import stdlib
    stdlib.math_add(5, 3)
    stdlib.string_reverse("hello")
"""

# ==============================
# MATH UTILITIES
# ==============================

def math_add(a, b):
    """Add two numbers together."""
    return a + b

def math_subtract(a, b):
    """Subtract b from a."""
    return a - b

def math_multiply(a, b):
    """Multiply two numbers."""
    return a * b

def math_divide(a, b):
    """Divide a by b. Returns error if b is 0."""
    if b == 0:
        return "ERROR: Cannot divide by zero!"
    return a / b

def math_power(base, exp):
    """Raise base to the power of exp."""
    return base ** exp

def math_squareroot(n):
    """Return the square root of n."""
    return n ** 0.5

def math_absolute(n):
    """Return the absolute value of n (makes negative numbers positive)."""
    return n if n >= 0 else -n

def math_round(n, digits=0):
    """Round n to the given number of digits after decimal."""
    return round(n, digits)

def math_bigger(a, b):
    """Return the larger of a and b."""
    return a if a > b else b

def math_smaller(a, b):
    """Return the smaller of a and b."""
    return a if a < b else b

def math_random(min_val=0, max_val=100):
    """Return a random whole number between min_val and max_val."""
    import random
    return random.randint(min_val, max_val)

def math_sum(numbers):
    """Add up all numbers in a list and return the total."""
    total = 0
    for n in numbers:
        total += n
    return total

def math_average(numbers):
    """Return the average (mean) of a list of numbers."""
    if len(numbers) == 0:
        return 0
    return math_sum(numbers) / len(numbers)

def math_remainder(a, b):
    """Get the remainder after dividing a by b."""
    if b == 0:
        return "ERROR: Cannot divide by zero!"
    return a % b

def math_is_even(n):
    """Check if a number is even. Returns yeah or nah."""
    return n % 2 == 0

def math_is_odd(n):
    """Check if a number is odd. Returns yeah or nah."""
    return n % 2 != 0


# ==============================
# STRING UTILITIES
# ==============================

def string_length(s):
    """Return how many characters are in a string."""
    return len(s)

def string_uppercase(s):
    """Convert string to ALL CAPS."""
    return str(s).upper()

def string_lowercase(s):
    """Convert string to all lowercase."""
    return str(s).lower()

def string_reverse(s):
    """Reverse a string backwards."""
    return str(s)[::-1]

def string_contains(text, keyword):
    """Check if text contains the keyword. Returns yeah or nah."""
    return keyword in str(text)

def string_starts_with(text, prefix):
    """Check if text starts with a certain word/letter. Returns yeah or nah."""
    return str(text).startswith(prefix)

def string_ends_with(text, suffix):
    """Check if text ends with a certain word/letter. Returns yeah or nah."""
    return str(text).endswith(suffix)

def string_split(text, separator=" "):
    """Split a string into a list, cutting at the separator."""
    return str(text).split(separator)

def string_join(list_of_strings, glue=""):
    """Join a list of strings into one string, with glue between them."""
    return glue.join(str(item) for item in list_of_strings)

def string_replace(text, old, new):
    """Replace every occurrence of 'old' with 'new' in the text."""
    return str(text).replace(old, new)

def string_removespaces(text):
    """Remove spaces from both the beginning and end of a string."""
    return str(text).strip()

def string_getrange(text, start, end=None):
    """Get a piece of a string from position start to position end."""
    if end is None:
        return str(text)[start:]
    return str(text)[start:end]

def string_getcharacter(text, position):
    """Get the character at a specific position in a string."""
    return str(text)[position]

def string_count(text, word):
    """Count how many times a word appears in the text."""
    return str(text).count(word)


# ==============================
# LIST UTILITIES
# ==============================

def list_length(lst):
    """Return how many items are in a list."""
    return len(lst)

def list_additem(lst, item):
    """Add an item to the end of a list."""
    lst.append(item)
    return lst

def list_additematstart(lst, item):
    """Add an item to the beginning of a list."""
    lst.insert(0, item)
    return lst

def list_removelast(lst):
    """Remove and return the last item from a list."""
    if len(lst) == 0:
        return "ERROR: Cannot remove from empty list!"
    return lst.pop()

def list_removefirst(lst):
    """Remove and return the first item from a list."""
    if len(lst) == 0:
        return "ERROR: Cannot remove from empty list!"
    return lst.pop(0)

def list_removeat(lst, index):
    """Remove and return the item at a specific position in a list."""
    if len(lst) == 0:
        return "ERROR: Cannot remove from empty list!"
    if index < 0 or index >= len(lst):
        return f"ERROR: Index {index} is out of range!"
    return lst.pop(index)

def list_removeitem(lst, item):
    """Remove the first occurrence of a specific item from a list."""
    try:
        lst.remove(item)
    except ValueError:
        pass
    return lst

def list_sort_ascending(lst):
    """Sort a list from smallest to biggest (A to Z)."""
    return sorted(lst)

def list_sort_descending(lst):
    """Sort a list from biggest to smallest (Z to A)."""
    return sorted(lst, reverse=True)

def list_reverse(lst):
    """Reverse the order of items in a list."""
    return lst[::-1]

def list_contains(lst, item):
    """Check if a list contains a specific item. Returns yeah or nah."""
    return item in lst

def list_findindex(lst, item):
    """Find the position of an item in a list. Returns -1 if not found."""
    try:
        return lst.index(item)
    except ValueError:
        return -1

def list_getitem(lst, index):
    """Get the item at a specific position in a list."""
    if index < 0 or index >= len(lst):
        return f"ERROR: Index {index} is out of range!"
    return lst[index]

def list_getrange(lst, start, end=None):
    """Get a piece of a list from position start to position end."""
    if end is None:
        return lst[start:]
    return lst[start:end]

def list_transform(lst, func):
    """Apply a function to every item in a list and return a new list."""
    return [func(item) for item in lst]


# ==============================
# FILE I/O UTILITIES
# ==============================

def file_read(path):
    """Read the entire contents of a file as a string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File '{path}' not found!"
    except Exception as e:
        return f"ERROR: {e}"

def file_write(path, content):
    """Write content to a file (overwrites anything that was there before)."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return "ok"
    except Exception as e:
        return f"ERROR: {e}"

def file_append(path, content):
    """Add content to the end of an existing file."""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return "ok"
    except Exception as e:
        return f"ERROR: {e}"

def file_exists(path):
    """Check if a file exists. Returns yeah or nah."""
    import os
    return os.path.exists(path)

def file_readlines(path):
    """Read all lines of a file into a list (each line is one item)."""
    content = file_read(path)
    if content.startswith("ERROR:"):
        return content
    return content.split("\n")


# ==============================
# TIME UTILITIES
# ==============================

def time_now():
    """Return the current date and time as a string (e.g. 2026-06-11 22:30:00)."""
    import datetime
    return str(datetime.datetime.now())

def time_date():
    """Return today's date as a string (e.g. 2026-06-11)."""
    import datetime
    return str(datetime.date.today())

def time_sleep(seconds):
    """Pause the program for a given number of seconds."""
    import time
    time.sleep(seconds)


# ==============================
# CONVERSION UTILITIES (built-in, no import needed)
# ==============================

def convert_to_num(text):
    """Convert a string to a whole number. Returns 0 if it fails."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return 0

def convert_to_decimal(text):
    """Convert a string to a decimal number. Returns 0.0 if it fails."""
    try:
        return float(text)
    except (ValueError, TypeError):
        return 0.0

def convert_to_txt(value):
    """Convert any value to text (string)."""
    return str(value)

def convert_to_list(value):
    """Convert a string to a list of individual characters."""
    return list(str(value))


# ==============================
# INPUT HELPER (used by ask() in compiled code)
# ==============================

def und_input(prompt=""):
    """Get input from the user. Used internally by ask()."""
    return input(prompt)


# ==============================
# HELPER / UTILITY
# ==============================

def get_type(value):
    """Return the type name of a value as a string (num, dec, txt, bool, list, nope)."""
    t = type(value).__name__
    mapping = {
        "int": "num",
        "float": "dec",
        "str": "txt",
        "bool": "bool",
        "list": "list",
        "NoneType": "nope",
    }
    return mapping.get(t, t)

# ==============================
# DICTIONARY UTILITIES
# ==============================

def dict_get(d, key, default=None):
    """Get a value from a dictionary, or return a default if the key doesn't exist."""
    return d.get(key, default)

def dict_set(d, key, value):
    """Set a key-value pair in a dictionary. Returns the dictionary."""
    d[key] = value
    return d

def dict_has(d, key):
    """Check if a dictionary has a key. Returns yeah or nah."""
    return key in d

def dict_remove(d, key):
    """Remove a key from a dictionary. Returns the dictionary."""
    if key in d:
        del d[key]
    return d

def dict_keys(d):
    """Get all keys from a dictionary as a list."""
    return list(d.keys())

def dict_values(d):
    """Get all values from a dictionary as a list."""
    return list(d.values())

def dict_items(d):
    """Get all key-value pairs from a dictionary as a list of (key, value) tuples."""
    return list(d.items())

def dict_length(d):
    """Get the number of key-value pairs in a dictionary."""
    return len(d)

def dict_clear(d):
    """Remove all entries from a dictionary. Returns the empty dictionary."""
    d.clear()
    return d

def dict_copy(d):
    """Create a shallow copy of a dictionary."""
    return d.copy()

def dict_update(d, other):
    """Update a dictionary with key-value pairs from another dictionary."""
    d.update(other)
    return d
