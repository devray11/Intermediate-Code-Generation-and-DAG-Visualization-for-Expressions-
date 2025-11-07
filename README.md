# Intermediate Code Generator and DAG Visualizer

## A Compiler Design Project

This repository contains a mini-compiler project that demonstrates the core phases of compilation, focusing on the generation of intermediate representations (IR) and optimization for arithmetic expressions.

The system takes a simple arithmetic expression (e.g., `a=b+c*d;`) as input and processes it through various compiler phases. It is designed to practically illustrate how high-level source code is transformed into optimized, low-level forms, bridging the gap between the compiler's front-end and back-end.

The project features an interactive web interface built with Streamlit, which visualizes each stage of the compilation process, including token generation, the Abstract Syntax Tree (AST), all intermediate code forms, and the final optimized Directed Acyclic Graph (DAG).

## Features

* **Lexical Analysis:** Tokenizes the input source code to identify identifiers, operators, and punctuation.
* **Syntax Analysis:** Implements a recursive descent parser to build an Abstract Syntax Tree (AST) that represents the grammatical structure of the expression.
* **Intermediate Code Generation:** Generates three distinct intermediate representations from the AST:
    * Three-Address Code (TAC)
    * Quadruples
    * Triples
* **Optimization:** Constructs a Directed Acyclic Graph (DAG) from the intermediate code to identify and eliminate common subexpressions.
* **Interactive Visualization:** A web interface that clearly displays the output of every phase:
    * List of Tokens
    * Abstract Syntax Tree (AST)
    * Three-Address Code (TAC)
    * Quadruples Table
    * Triples Table
    * Rendered DAG using Graphviz

## Technologies Used

* **Core Logic:** Python
* **Web Interface:** Streamlit
* **Parsing:** Recursive Descent
* **Visualization:** Graphviz (for rendering the AST and DAG)

![Output Image](https://github.com/devray11/Intermediate-Code-Generation-and-DAG-Visualization-for-Expressions-/blob/0db350d8f799b843fc2f6143ebff4f311634c869/Output-Image.png)
