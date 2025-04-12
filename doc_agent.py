import ast
from pathlib import Path
from langchain_community.llms import Ollama

# Initialize codellama via Ollama
llm = Ollama(model="codellama:instruct")

def generate_docstring(code_block):
    """Generate a proper Python docstring using codellama."""
    prompt = f"Generate a Python docstring for the following function:\n\n{code_block}"
    response = llm.invoke(prompt)
    return response.strip()

def explain_function(code_block):
    """Generate a friendly explanation for beginners using codellama."""
    prompt = f"Explain in a clear, beginner-friendly way what this Python function does. Use simple language and examples if needed:\n\n{code_block}"
    response = llm.invoke(prompt)
    return response.strip()

def extract_functions_from_file(file_path):
    """Extract top-level functions from a Python file using AST."""
    with open(file_path, "r") as f:
        file_content = f.read()

    parsed = ast.parse(file_content)
    functions = []

    for node in parsed.body:
        if isinstance(node, ast.FunctionDef):
            func_code = ast.get_source_segment(file_content, node)
            functions.append({
                "name": node.name,
                "code": func_code
            })

    return functions

if __name__ == "__main__":
    functions = extract_functions_from_file("test_code.py")

    for func in functions:
        print(f"\n🧠 Function: {func['name']}")
        print(func['code'])

        # Generate plain English explanation
        explanation = explain_function(func['code'])
        print(f"\n📘 Friendly Explanation:\n{explanation}")

        # Generate professional docstring
        docstring = generate_docstring(func['code'])
        print(f"\n📄 Suggested Docstring:\n{docstring}")
