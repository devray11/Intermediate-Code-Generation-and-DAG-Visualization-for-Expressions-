# parser.py
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", None)

    def consume(self, token_type=None):
        current = self.peek()
        if token_type and current[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {current}")
        self.pos += 1
        return current

    def parse(self):
        """Program → StmtList"""
        stmts = []
        while self.peek()[0] != "EOF":
            stmts.append(self.stmt())
        return ("program", stmts)

    def stmt(self):
        """Stmt → ID = Expr ;"""
        id_tok = self.consume("ID")
        self.consume("ASSIGN")
        expr = self.expr()
        self.consume("END")
        return ("assign", id_tok[1], expr)

    def expr(self):
        """Expr → Term {(+|-) Term}"""
        node = self.term()
        while self.peek()[0] == "OP" and self.peek()[1] in "+-":
            op = self.consume("OP")
            right = self.term()
            node = (op[1], node, right)
        return node

    def term(self):
        """Term → Factor {(*|/) Factor}"""
        node = self.factor()
        while self.peek()[0] == "OP" and self.peek()[1] in "*/":
            op = self.consume("OP")
            right = self.factor()
            node = (op[1], node, right)
        return node

    def factor(self):
        tok = self.peek()
        if tok[0] == "NUMBER":
            self.consume("NUMBER")
            return ("num", tok[1])
        elif tok[0] == "ID":
            self.consume("ID")
            return ("id", tok[1])
        elif tok[0] == "LPAREN":
            self.consume("LPAREN")
            node = self.expr()
            self.consume("RPAREN")
            return node
        else:
            raise SyntaxError(f"Unexpected token: {tok}")


# Test run
if __name__ == "__main__":
    from lexer import lexer

    code = "a = b + c * d;"
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print("Source Code:", code)
    print("AST:", ast)
