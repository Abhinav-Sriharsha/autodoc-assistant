# 🧠 AutoDoc Assistant

> Automatically generate Python docstrings using a local LLM (CodeLlama via Ollama) with a Streamlit interface.

---

## ✨ Features

- 📂 Upload any `.py` file
- 🔍 Automatically extract all functions using AST
- 🤖 Use Ollama + CodeLlama to generate meaningful Python docstrings
- 📝 Insert the docstring directly into the function in your file
- 🌐 Simple UI using Streamlit — no coding needed to use it!

---

## 🚀 Quickstart

```bash
# Clone and navigate
git clone https://github.com/yourusername/autodoc-assistant.git
cd autodoc-assistant
```

# Create and activate venv
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activat
```

# Install dependencies
```
pip install -r requirements.txt
```

# Make sure you have Ollama + CodeLlama
```
ollama pull codellama
```

# Run the app
```
streamlit run app.py
```

# 🧠 Example
Before:
```
def multiply(x, y):
    return x * y
 ```
After:
```
python
Copy
Edit
def multiply(x, y):
    """
    Multiplies two numbers.

    Args:
        x (int): First number.
        y (int): Second number.

    Returns:
        int: The product of x and y.
    """
    return x * y
```
