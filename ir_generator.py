# ir_generator.py

class IRGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []          # List of TAC instructions
        self.quadruples = []    # List of (op, arg1, arg2, result)
        self.triples = []       # List of (index, op, arg1, arg2)

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast):
        """Generate IR from AST"""
        node_type = ast[0]

        if node_type == "program":
            for stmt in ast[1]:
                self.generate(stmt)

        elif node_type == "assign":
            var_name = ast[1]
            expr_result = self.generate(ast[2])
            self.emit("=", expr_result, None, var_name)

        elif node_type == "num":
            return str(ast[1])

        elif node_type == "id":
            return ast[1]

        elif node_type in {"+", "-", "*", "/"}:
            left = self.generate(ast[1])
            right = self.generate(ast[2])
            temp = self.new_temp()
            self.emit(node_type, left, right, temp)
            return temp

        else:
            raise ValueError(f"Unknown AST node: {node_type}")

    def emit(self, op, arg1, arg2, result):
        """Store TAC, Quadruple, Triple forms"""
        # TAC form
        if arg2 is None:
            tac = f"{result} = {arg1}"
        else:
            tac = f"{result} = {arg1} {op} {arg2}"
        self.code.append(tac)

        # Quadruple form
        self.quadruples.append((op, arg1, arg2, result))

        # Triple form (use index instead of result name)
        self.triples.append((len(self.triples), op, arg1, arg2))

    def print_tac(self):
        print("\nThree-Address Code (TAC):")
        for line in self.code:
            print(line)

    def print_quadruples(self):
        print("\nQuadruples:")
        print("op\targ1\targ2\tresult")
        for q in self.quadruples:
            print(f"{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}")

    def print_triples(self):
        print("\nTriples:")
        print("index\top\targ1\targ2")
        for t in self.triples:
            print(f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}")


# Test Run
if __name__ == "__main__":
    from lexer import lexer
    from parser import Parser

    code = "a = b + c * d;"
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()

    print("AST:", ast)

    ir = IRGenerator()
    ir.generate(ast)

    ir.print_tac()
    ir.print_quadruples()
    ir.print_triples()
