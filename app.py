# app.py
import streamlit as st
from lexer import lexer
from parser import Parser
from ir_generator import IRGenerator
#from dag_generator import DAGGenerator
#import graphviz

st.set_page_config(page_title="Compiler Design Mini Project", layout="wide")

st.title("Compiler Design Project")
st.subheader("Intermediate Code Representations: TAC, Quadruples, Triples, DAG")

# Text area for code input
code_input = st.text_area("Enter your code:", "a = b + c * d;")

if st.button("Run Compiler"):
    try:
        # Step 1: Lexical Analysis
        tokens = lexer(code_input)
        st.markdown("### 🔹 Tokens")
        st.json(tokens)

        # Step 2: Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        st.markdown("### 🔹 Abstract Syntax Tree (AST)")
        st.json(ast)

        # Step 3: Intermediate Code Generation
        ir = IRGenerator()
        ir.generate(ast)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🔹 Three-Address Code (TAC)")
            st.code("\n".join(ir.code), language="c")

        with col2:
            st.markdown("### 🔹 Quadruples")
            st.table(
                {
                    "op": [q[0] for q in ir.quadruples],
                    "arg1": [q[1] for q in ir.quadruples],
                    "arg2": [q[2] for q in ir.quadruples],
                    "result": [q[3] for q in ir.quadruples],
                }
            )

        with col3:
            st.markdown("### 🔹 Triples")
            st.table(
                {
                    "index": [t[0] for t in ir.triples],
                    "op": [t[1] for t in ir.triples],
                    "arg1": [t[2] for t in ir.triples],
                    "arg2": [t[3] for t in ir.triples],
                }
            )

        # Step 4: DAG Generation
        st.markdown("### 🔹 DAG Representation (Textual)")
        dag = DAGGenerator()
        dag.build(ast)
        nodes, edges = dag.get_nodes_and_edges()

        st.text("Nodes:\n" + "\n".join(nodes))
        st.text("Edges:\n" + "\n".join(edges))

        # Step 5: DAG Visualization using Graphviz
        st.markdown("### 🔹 DAG Diagram (Graphviz)")

        dot = graphviz.Digraph(comment='DAG')

        # Add nodes
        for idx, node in enumerate(dag.nodes):
            if node.op:
                label = f"{node.op}\n{','.join(node.labels)}"
            else:
                label = f"{node.value}\n{','.join(node.labels)}"
            dot.node(str(idx), label)

        # Add edges
        for idx, node in enumerate(dag.nodes):
            if node.op:
                if node.left:
                    left_idx = dag.nodes.index(node.left)
                    dot.edge(str(idx), str(left_idx))
                if node.right:
                    right_idx = dag.nodes.index(node.right)
                    dot.edge(str(idx), str(right_idx))

        st.graphviz_chart(dot)

    except Exception as e:
        st.error(f"Compilation Error: {str(e)}")
