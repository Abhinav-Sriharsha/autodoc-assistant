import streamlit as st
import os
import ast
import astor
from langchain_community.llms import Ollama

# Streamlit page config
st.set_page_config(page_title="Code Documentation Assistant", layout="wide")
st.title("📘 Code Documentation Assistant")

# Initialize codellama model
llm = Ollama(model="codellama:instruct")

# Extract top-level functions
def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    parsed = ast.parse(content)
    functions = []
    for node in parsed.body:
        if isinstance(node, ast.FunctionDef):
            code = ast.get_source_segment(content, node)
            functions.append({
                "name": node.name,
                "code": code
            })
    return functions

# Generate beginner-friendly explanation
def explain_function(code):
    prompt = f"Explain this Python function to a beginner, in simple language:\n\n{code}"
    return llm.invoke(prompt).strip()

# Generate a Python docstring
def generate_docstring(code):
    prompt = f"Generate a Python docstring for the following function:\n\n{code}"
    return llm.invoke(prompt).strip()

# Insert docstrings using AST
def insert_docstrings(file_path, functions_with_docs):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            match = next((f for f in functions_with_docs if f["name"] == node.name), None)
            if match and not ast.get_docstring(node):
                doc_node = ast.Expr(value=ast.Str(s=match["doc"]))
                node.body.insert(0, doc_node)

    return astor.to_source(tree)

# Upload UI
uploaded_file = st.file_uploader("📂 Upload a Python (.py) file", type=["py"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Save file to local
    os.makedirs("uploaded", exist_ok=True)
    file_path = os.path.join("uploaded", uploaded_file.name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))

    # Extract + display explanations
    with st.spinner("🧠 Analyzing functions and generating explanations..."):
        functions = extract_functions(file_path)
        documented_funcs = []

        for func in functions:
            st.subheader(f"🧩 Function: `{func['name']}`")
            st.code(func["code"], language="python")

            explanation = explain_function(func["code"])
            st.markdown(f"**🧠 Friendly Explanation:**\n\n{explanation}")

            docstring = generate_docstring(func["code"])
            documented_funcs.append({
                "name": func["name"],
                "doc": docstring
            })

    # --- Step 3 Options ---
    st.markdown("### 🛠️ Choose how you want to apply the docstrings:")

    option = st.radio("Choose one:", 
        ("Option A: Overwrite a specific file on your system", 
         "Option B: Download a new file with docstrings"))

    if option == "Option A: Overwrite a specific file on your system":
        overwrite_path = st.text_input("📝 Enter the full path of the file you want to overwrite:")
        if st.button("⚠️ Overwrite File"):
            if overwrite_path and os.path.isfile(overwrite_path):
                updated_code = insert_docstrings(overwrite_path, documented_funcs)
                with open(overwrite_path, "w", encoding="utf-8") as f:
                    f.write(updated_code)
                st.success("✅ File successfully overwritten.")
            else:
                st.error("❌ Please provide a valid file path.")
    
    if option == "Option B: Download a new file with docstrings":
        new_code = insert_docstrings(file_path, documented_funcs)
        st.download_button(
            label="📥 Download Modified File",
            data=new_code,
            file_name=uploaded_file.name.replace(".py", "_documented.py"),
            mime="text/x-python"
        )
