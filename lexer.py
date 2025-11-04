# lexer.py
import re

# Define token specification
token_specification = [
    ("NUMBER",   r'\d+'),                 # Integer
    ("ID",       r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
    ("ASSIGN",   r'='),                   # Assignment operator
    ("OP",       r'[\+\-\*/]'),           # Arithmetic operators + - * /
    ("LPAREN",   r'\('),                  # (
    ("RPAREN",   r'\)'),                  # )
    ("END",      r';'),                   # ;
    ("SKIP",     r'[ \t]+'),              # Skip spaces and tabs
    ("MISMATCH", r'.'),                   # Any other character
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

def lexer(code):
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            tokens.append(("NUMBER", int(value)))
        elif kind == "ID":
            tokens.append(("ID", value))
        elif kind in ("ASSIGN", "OP", "LPAREN", "RPAREN", "END"):
            tokens.append((kind, value))
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character: {value}")
    tokens.append(("EOF", None))  # End of file marker
    return tokens

# Test run
if __name__ == "__main__":
    code = "a = b + c * d;"
    print("Source Code:", code)
    print("Tokens:", lexer(code))
