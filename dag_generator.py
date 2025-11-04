# dag_generator.py

from graphviz import Digraph

class DAGNode:
    def __init__(self, op=None, left=None, right=None, value=None):
        self.op = op
        self.left = left
        self.right = right
        self.value = value
        self.labels = []  

    def get_label(self):
        """Return label for Graphviz and textual output"""
        if self.op:
            return f"{self.op}\n{','.join(self.labels)}" if self.labels else self.op
        else:
            return f"{self.value}\n{','.join(self.labels)}" if self.labels else str(self.value)


class DAGGenerator:
    def __init__(self):
        self.nodes = []

    def get_or_create_node(self, op=None, left=None, right=None, value=None):
        for node in self.nodes:
            if node.op == op and node.left == left and node.right == right and node.value == value:
                return node
        new_node = DAGNode(op, left, right, value)
        self.nodes.append(new_node)
        return new_node

    def build(self, ast):
        node_type = ast[0]

        if node_type == "program":
            dag_nodes = []
            for stmt in ast[1]:
                dag_nodes.append(self.build(stmt))
            return ("program", dag_nodes)

        elif node_type == "assign":
            var_name = ast[1]
            expr_node = self.build(ast[2])
            if var_name not in expr_node.labels:
                expr_node.labels.append(var_name)
            return expr_node

        elif node_type == "num":
            return self.get_or_create_node(value=ast[1])

        elif node_type == "id":
            return self.get_or_create_node(value=ast[1])

        elif node_type in {"+", "-", "*", "/"}:
            left = self.build(ast[1])
            right = self.build(ast[2])
            return self.get_or_create_node(op=node_type, left=left, right=right)

        else:
            raise ValueError(f"Unknown AST node type: {node_type}")

    def get_nodes_and_edges(self):
        """Return textual DAG representation"""
        nodes_list = []
        edges_list = []

        for idx, node in enumerate(self.nodes):
            nodes_list.append(f"{idx}: {node.get_label()}")
            if node.left:
                left_idx = self.nodes.index(node.left)
                edges_list.append(f"{idx} → {left_idx}")
            if node.right:
                right_idx = self.nodes.index(node.right)
                edges_list.append(f"{idx} → {right_idx}")

        return nodes_list, edges_list

    def visualize(self, filename="dag"):
        """Generate DAG using Graphviz"""
        dot = Digraph(comment="DAG")
        dot.attr("node", shape="ellipse")

        for idx, node in enumerate(self.nodes):
            dot.node(str(idx), node.get_label())

        for idx, node in enumerate(self.nodes):
            if node.left:
                dot.edge(str(idx), str(self.nodes.index(node.left)))
            if node.right:
                dot.edge(str(idx), str(self.nodes.index(node.right)))

        dot.render(filename, format="png", cleanup=True)
        print(f"DAG saved as {filename}.png")


# Test run
if __name__ == "__main__":
    from lexer import lexer
    from parser import Parser

    code = "a = b + c * d;"
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()

    dag_gen = DAGGenerator()
    dag_gen.build(ast)

    # Textual DAG
    nodes, edges = dag_gen.get_nodes_and_edges()
    print("Nodes:")
    print("\n".join(nodes))
    print("\nEdges:")
    print("\n".join(edges))

    # Graphviz diagram
    dag_gen.visualize("dag_output")
