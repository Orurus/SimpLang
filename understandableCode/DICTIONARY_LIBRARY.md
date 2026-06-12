# UnderstandableCode Dictionary Library

> **"Store and retrieve data with ease."**

UnderstandableCode now supports dictionaries — associative data structures that map keys to values. Dictionaries are perfect for organizing related data, like storing user profiles, configuration settings, or any key-value pairs.

---

## Table of Contents

1. [Overview](#overview)
2. [Creating Dictionaries](#creating-dictionaries)
3. [Accessing Values](#accessing-values)
4. [Dictionary Methods](#dictionary-methods)
5. [Dictionary Iteration](#dictionary-iteration)
6. [Dot Notation](#dot-notation)
7. [Examples](#examples)

---

## Overview

A dictionary in UnderstandableCode is a collection of key-value pairs, where each key is unique and maps to a value. Dictionaries are defined using curly braces `{}` with the syntax `{key: value, ...}`.

### Key Features

- **Flexible keys**: Keys can be strings, numbers, or identifiers
- **Any value type**: Values can be strings, numbers, lists, or even other dictionaries
- **Fast lookup**: Retrieve values by their keys instantly
- **Dynamic**: Add, update, and remove entries as needed

---

## Creating Dictionaries

### Basic Dictionary Syntax

```python
// Create an empty dictionary
person = {}

// Create a dictionary with initial data
person = {
    name: "Alice",
    age: 30,
    city: "New York"
}

// Dictionary with various value types
config = {
    max_attempts: 5,
    timeout: 30.5,
    enabled: yeah,
    tags: ["important", "urgent"]
}
```

### Key Types

Keys in UnderstandableCode dictionaries can be:

| Key Type | Example | Python Equivalent |
|----------|---------|-------------------|
| Bare identifier (converted to string) | `name: "Alice"` | `"name": "Alice"` |
| String literal | `"user-name": "Bob"` | `"user-name": "Bob"` |
| Number | `1: "one"` | `1: "one"` |

**Important**: When you write a bare identifier like `name` as a key in a dictionary, it's automatically converted to the string `"name"`. This is for beginner-friendliness.

---

## Accessing Values

### Bracket Notation

Access dictionary values using square brackets `[]`:

```python
person = {name: "Alice", age: 30}

// Use QUOTED strings for literal keys:
say(person["name"])  // Outputs: Alice
say(person["age"])   // Outputs: 30

// Use bare identifiers (variables) for dynamic keys:
key = "name"
say(person[key])  // Outputs: Alice (uses variable 'key')
```

**Key distinction**:
- `person["name"]` - looks up the literal key `"name"` in the dictionary
- `person[name]` - looks up the value of the variable `name` (e.g., if `name = "age"`, it would look up `person["age"]`)

### Safe Access (with default)

Since UnderstandableCode dictionaries use Python's `dict`, accessing a non-existent key raises an error. Use `get` style patterns with `stdlib.dict_get`:

```python
// Using stdlib.dict_get with default value
value = stdlib.dict_get(person, "email", "no-email")
say(value)  // Outputs: no-email (since email doesn't exist)
```

---

## Dictionary Iteration

### Looping Through Keys

Use `stdlib.dict_keys()` to get all keys and loop through them:

```python
person = {name: "Alice", age: 30, city: "NYC"}

loop key in stdlib.dict_keys(person)
    say(key + ": " + convert_to_txt(person[key]))
end

// Outputs:
// name: Alice
// age: 30
// city: NYC
```

### Looping Through Values

Use `stdlib.dict_values()` to get all values:

```python
person = {name: "Alice", age: 30}

loop val in stdlib.dict_values(person)
    say(val)
end

// Outputs:
// Alice
// 30
```

### Looping Through Key-Value Pairs

Use `stdlib.dict_items()` to get all key-value pairs:

```python
person = {name: "Alice", age: 30}

loop item in stdlib.dict_items(person)
    say(item[0] + ": " + convert_to_txt(item[1]))
end

// Outputs:
// name: Alice
// age: 30
```

### Future: Dictionary Iteration Syntax

**Note**: The following syntax is planned for future versions:

```python
// Planned syntax (not yet supported):
loop key, value in person
    say(key + ": " + convert_to_txt(value))
end
```

This would transpile to:

```python
for key, value in person.items():
    print(key + ": " + str(value))
```

The current way to iterate is:

```python
loop key in stdlib.dict_keys(person)
    say(key + ": " + convert_to_txt(person[key]))
end
```

---

## Dot Notation

### Accessing with Dot Notation

For simple string keys (identifiers without spaces or special characters), you can use dot notation:

```python
person = {name: "Alice", age: 30}

// Bracket notation:
say(person["name"])

// Dot notation (for simple keys):
say(person.name)
say(person.age)
```

**Note**: Dot notation only works with simple identifier-like keys. For keys with special characters or spaces, use bracket notation:

```python
data = {"user-name": "Bob", "full name": "Alice Smith"}

// Dot notation won't work for these:
say(data["user-name"])  // OK - bracket notation
say(data["full name"])  // OK - bracket notation

// Use bracket notation for special keys
```

---

## Dictionary Methods

UnderstandableCode's standard library provides dictionary helpers under `stdlib.dict_*`:

### `dict_get(dict, key, default)`

Get a value from the dictionary, or return a default if the key doesn't exist.

```python
person = {name: "Alice"}

email = stdlib.dict_get(person, "email", "unknown@example.com")
say(email)  // Outputs: unknown@example.com
```

### `dict_set(dict, key, value)`

Set a key-value pair in the dictionary.

```python
person = {name: "Alice"}
stdlib.dict_set(person, "age", 30)

// Access with quoted string:
say(person["age"])  // Outputs: 30
```

### `dict_has(dict, key)`

Check if a key exists in the dictionary.

```python
person = {name: "Alice", age: 30}

// Use quoted string for the key:
say(stdlib.dict_has(person, "name"))  // Outputs: yeah
say(stdlib.dict_has(person, "email")) // Outputs: nah
```

### `dict_remove(dict, key)`

Remove a key from the dictionary.

```python
person = {name: "Alice", age: 30}
stdlib.dict_remove(person, "age")

// person now only has the name key
```

### `dict_length(dict)`

Get the number of key-value pairs.

```python
person = {name: "Alice", age: 30, city: "NYC"}
say(stdlib.dict_length(person))  // Outputs: 3
```

### `dict_clear(dict)`

Remove all entries from the dictionary.

```python
person = {name: "Alice", age: 30}
stdlib.dict_clear(person)
say(stdlib.dict_length(person))  // Outputs: 0
```

loop key in keys
    say(key)
end

// Outputs:
// name
// age
// city
```

### `dict_values(dict)`

Get all values as a list.

```python
person = {name: "Alice", age: 30}
values = stdlib.dict_values(person)

loop val in values
    say(val)
end

// Outputs:
// Alice
// 30
```

### `dict_items(dict)`

Get all key-value pairs as a list of tuples.

```python
person = {name: "Alice", age: 30}
items = stdlib.dict_items(person)

loop item in items
    // item is a tuple (key, value)
    say(item[0] + ": " + convert_to_txt(item[1]))
end

// Outputs:
// name: Alice
// age: 30
```

### `dict_length(dict)`

Get the number of key-value pairs.

```python
person = {name: "Alice", age: 30, city: "NYC"}
say(stdlib.dict_length(person))  // Outputs: 3
```

### `dict_clear(dict)`

Remove all entries from the dictionary.

```python
person = {name: "Alice", age: 30}
stdlib.dict_clear(person)
say(stdlib.dict_length(person))  // Outputs: 0
```

---

## Examples

### Example 1: User Profile

```python
// Create a user profile
user = {
    username: "john_doe",
    email: "john@example.com",
    score: 100,
    verified: yeah
}

// Access values - use QUOTED strings for bracket notation
say("User: " + user["username"])
say("Email: " + user["email"])

// Update values
user["score"] = user["score"] + 50

// Check if key exists
if stdlib.dict_has(user, "email")
    say("Email is set: " + user["email"])
end
```

### Example 2: Configuration

```python
// Define app configuration
app_config = {
    host: "localhost",
    port: 8080,
    debug: yeah,
    features: ["auth", "logging", "caching"]
}

// Access configuration - use QUOTED strings
say("Host: " + app_config["host"])
say("Port: " + convert_to_txt(app_config["port"]))

// Update configuration
app_config["debug"] = nah

// Check feature
if stdlib.dict_has(app_config, "features")
    features = app_config["features"]
    loop feature in features
        say("Feature: " + feature)
    end
end
```

### Example 3: Nested Dictionaries

```python
// Create nested dictionary structure
company = {
    name: "Tech Corp",
    departments: {
        engineering: {
            manager: "Alice",
            employees: 25,
            budget: 100000
        },
        sales: {
            manager: "Bob",
            employees: 15,
            budget: 75000
        }
    }
}

// Access nested values - use QUOTED strings
engineering_manager = company["departments"]["engineering"]["manager"]
say("Engineering Manager: " + engineering_manager)
```

### Example 4: Counting Words

```python
// Count word occurrences
word_counts = {}

text = ["apple", "banana", "apple", "cherry", "banana", "apple"]

loop word in text
    if stdlib.dict_has(word_counts, word)
        current = word_counts[word]
        word_counts[word] = current + 1
    else
        word_counts[word] = 1
    end
end

// Display counts
loop key in stdlib.dict_keys(word_counts)
    say(key + ": " + convert_to_txt(word_counts[key]))
end

// Outputs:
// apple: 3
// banana: 2
// cherry: 1
```

### Example 5: Contact Book

```python
// Build a simple contact book
contacts = {}

// Add contacts
stdlib.dict_set(contacts, "Alice", {phone: "555-1234", email: "alice@example.com"})
stdlib.dict_set(contacts, "Bob", {phone: "555-5678", email: "bob@example.com"})
stdlib.dict_set(contacts, "Carol", {phone: "555-9012", email: "carol@example.com"})

// Lookup a contact
contact = stdlib.dict_get(contacts, "Alice", {phone: "unknown", email: "unknown"})
say("Alice's phone: " + contact["phone"])

// List all contacts
loop name in stdlib.dict_keys(contacts)
    contact = contacts[name]
    say(name + ": " + contact["phone"])
end
```

---

## Summary

Dictionaries are a powerful data structure for organizing related data. With UnderstandableCode's dictionary support:

- **Easy creation**: Use `{key: value, ...}` syntax
- **Fast access**: Retrieve values with `dict["key"]` (using quoted strings)
- **Built-in helpers**: Use `stdlib.dict_*` functions for get, set, has, remove, keys, values, items, length, clear
- **Flexible keys**: Bare identifiers, strings, or numbers work as keys

### Key Points to Remember

1. **Dictionary keys**: Bare identifiers like `name` are automatically converted to `"name"`
2. **Accessing values**: Use **quoted strings** in brackets: `person["name"]`, NOT `person[name]` (which looks up a variable)
3. **Dot notation**: For simple keys, `person.name` works as shorthand for `person["name"]`
4. **Stdlib helpers**: Use `stdlib.dict_has`, `stdlib.dict_get`, etc. for safe operations

For more examples, check out `examples/dictionary.und` in the UnderstandableCode repository.
