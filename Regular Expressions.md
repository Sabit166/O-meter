# 🧩 Python Regular Expressions Cheat Sheet

## 🔑 Special Characters

| Character        | Meaning                                                                 |
|:----------------|:-----------------------------------------------------------------------|
| `.`             | Matches any character except newline (`\n`).                            |
| `^`             | Matches the start of a string.                                          |
| `$`             | Matches the end of a string.                                            |
| `*`             | Matches 0 or more repetitions of the preceding pattern.                 |
| `+`             | Matches 1 or more repetitions of the preceding pattern.                 |
| `?`             | Matches 0 or 1 repetition (makes it optional).                          |
| `{m}`           | Matches exactly m repetitions.                                          |
| `{m,n}`         | Matches between m and n repetitions.                                    |
| `[]`            | Defines a character class, e.g. `[abc]` matches `a`, `b`, or `c`.      |
| `()`            | Grouping and capturing.                                                 |
| `(?:...)`       | Non-capturing group.                                                    |
| `(?P<name>...)` | Named capturing group.                                                  |
| `\\`           | Escape character (for special sequences or escaping metacharacters).     |

---

## 🔹 Escape Sequences

| Sequence   | Meaning                                 |
|:----------:|:----------------------------------------|
| `\d`       | Digit (`[0-9]`).                        |
| `\D`       | Non-digit.                              |
| `\w`       | Word character (`[a-zA-Z0-9_]`).        |
| `\W`       | Non-word character.                     |
| `\s`       | Whitespace (`[ \t\n\r\f\v]`).           |
| `\S`       | Non-whitespace.                         |
| `\b`       | Word boundary.                          |
| `\B`       | Non-word boundary.                      |
| `\\`       | Matches a literal backslash.            |

---

## 🛠️ Useful Regex Functions in Python

```python
import re

# Search for a pattern
re.search(pattern, string)

# Find all matches
re.findall(pattern, string)

# Replace matches
re.sub(pattern, replacement, string)

# Compile a regex for reuse
regex = re.compile(pattern)
regex.match(string)
```

---

## 💡 Tips

- Use raw strings (`r"pattern"`) to avoid issues with escape sequences.
- Parentheses `()` can be used for grouping and capturing.
- Use `re.IGNORECASE` or `re.I` for case-insensitive matching.
- Use `^` and `$` to anchor your pattern to the start/end of a string.
- Use `|` for alternation (logical OR) in patterns.

---

## 📚 Example

```python
import re
text = "The price is $100."
match = re.search(r"\$\d+", text)
if match:
    print(match.group())  # Output: $100
```

---

## 🔗 More Resources

- [Python re module documentation](https://docs.python.org/3/library/re.html)
- [Regex101 online tester](https://regex101.com/)
