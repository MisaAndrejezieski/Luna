# 🌙 Luna - Assistente de Programação Offline

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-0.3+-orange.svg)](https://ollama.com)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-purple.svg)](https://customtkinter.tomschimansky.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Luna** é sua assistente de programação que funciona 100% offline. 
> Segura, privada e sempre disponível, mesmo sem internet.

---

## ✨ Funcionalidades

- 🤖 **Chat com IA** - Use modelos locais do Ollama (phi3, llama3.2, mistral)
- 🧠 **Memória de conversa** - Luna lembra do contexto da sua conversa
- 🔄 **Troca de modelos** - Mude o modelo de IA a qualquer momento
- 💻 **Foco em programação** - Ajuda com Python, JavaScript, debug, etc.
- 🔒 **100% offline** - Seus dados ficam apenas no seu computador
- 🎨 **Interface moderna** - Tema escuro com CustomTkinter

---

## 📸 Screenshot

![Luna Interface](assets/screenshot.png)

---

## 🚀 Como Instalar

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Ollama** instalado ([baixe aqui](https://ollama.com/download))

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/Luna.git
cd Luna

# 2. Crie o ambiente virtual
python -m venv .venv

# 3. Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Baixe um modelo no Ollama
ollama pull phi3

# 6. Execute a Luna
python -m src.main