# ============================================
# app.py - Luna Web (Streamlit)
# ============================================
"""
Interface web da Luna usando Streamlit.
"""
import time

import streamlit as st

from src.config import COR_PRIMARIA, EMOJI, NOME_ASSISTENTE
from src.ia import AssistenteProgramacao

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="🌙 Luna - Assistente de Programação",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    /* Estilo geral */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Título principal */
    .luna-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #6C63FF, #FF6B9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
    }
    
    /* Subtítulo */
    .luna-subtitle {
        text-align: center;
        color: #a0a0c0;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Container do chat */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Mensagem do usuário */
    .user-message {
        background: linear-gradient(135deg, #6C63FF, #7B6FFF);
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px 0;
        color: white;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }
    
    /* Mensagem da Luna */
    .luna-message {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px 0;
        color: #e0e0e0;
        max-width: 80%;
        float: left;
        clear: both;
        border-left: 4px solid #6C63FF;
    }
    
    /* Avatar Luna */
    .luna-avatar {
        font-size: 2rem;
        margin-right: 10px;
    }
    
    /* Input personalizado */
    .stTextInput > div > div > input {
        border-radius: 30px !important;
        border: 2px solid #6C63FF !important;
        padding: 15px 20px !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B9D !important;
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.2) !important;
    }
    
    /* Botão */
    .stButton > button {
        border-radius: 30px !important;
        background: linear-gradient(135deg, #6C63FF, #FF6B9D) !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px 30px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.4) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95) !important;
    }
    
    /* Badge de status */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        background: rgba(108, 99, 255, 0.2);
        color: #6C63FF;
        border: 1px solid #6C63FF;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INICIALIZA A LUNA
# ============================================
@st.cache_resource
def inicializar_luna():
    """Inicializa a assistente Luna (cacheada para não recarregar)."""
    return AssistenteProgramacao()

luna = inicializar_luna()

# ============================================
# GERENCIAMENTO DE ESTADO
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"🌙 Olá! Sou a Luna, sua assistente de programação offline.\n\nComo posso ajudar você hoje?"}
    ]

if "modelo_atual" not in st.session_state:
    st.session_state.modelo_atual = luna.modelo

# ============================================
# SIDEBAR - CONFIGURAÇÕES
# ============================================
with st.sidebar:
    st.markdown("## 🌙 Configurações")
    
    # Status
    st.markdown(f"**Status:** 🟢 Online")
    st.markdown(f"**Modelo:** `{st.session_state.modelo_atual}`")
    
    # Selecionar modelo
    st.markdown("---")
    st.markdown("### 🔄 Trocar Modelo")
    
    modelos_disponiveis = luna.listar_modelos_disponiveis()
    if not modelos_disponiveis:
        modelos_disponiveis = ["phi3", "llama3.2", "mistral"]
    
    novo_modelo = st.selectbox(
        "Escolha um modelo:",
        modelos_disponiveis,
        index=modelos_disponiveis.index(st.session_state.modelo_atual) if st.session_state.modelo_atual in modelos_disponiveis else 0
    )
    
    if novo_modelo != st.session_state.modelo_atual:
        if st.button("✅ Trocar Modelo"):
            with st.spinner(f"🔄 Trocando para {novo_modelo}..."):
                if luna.trocar_modelo(novo_modelo):
                    st.session_state.modelo_atual = novo_modelo
                    st.session_state.messages.append({"role": "assistant", "content": f"🔄 Troquei para o modelo **{novo_modelo}**!"})
                    st.rerun()
    
    st.markdown("---")
    
    # Botão Limpar Histórico
    if st.button("🧹 Limpar Histórico", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "🧹 Histórico limpo! Como posso ajudar?"}
        ]
        luna.limpar_memoria()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    st.markdown(f"**Mensagens:** {len(st.session_state.messages)}")
    st.markdown(f"**Modelo:** {st.session_state.modelo_atual}")
    
    st.markdown("---")
    st.markdown("### 💡 Dicas")
    st.markdown("""
    - Pergunte sobre código Python
    - Peça explicações de algoritmos
    - Solicite exemplos de código
    - Tire dúvidas de programação
    """)
    
    st.markdown("---")
    st.markdown(f"**{EMOJI} Luna v1.0**")

# ============================================
# ÁREA PRINCIPAL - CHAT
# ============================================
# Título
st.markdown('<div class="luna-title">🌙 Luna</div>', unsafe_allow_html=True)
st.markdown('<div class="luna-subtitle">Sua assistente de programação offline 🤫</div>', unsafe_allow_html=True)

# Container do chat
chat_container = st.container()

# Exibe as mensagens
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="luna-message">🌙 {msg["content"]}</div>', unsafe_allow_html=True)

# Espaço para o input
st.markdown("---")

# ============================================
# INPUT DO USUÁRIO
# ============================================
with st.container():
    col1, col2 = st.columns([5, 1])
    
    with col1:
        prompt = st.text_input(
            "Mensagem",
            placeholder="Digite sua pergunta para a Luna...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("📤 Enviar", use_container_width=True):
            if prompt and prompt.strip():
                # Adiciona a mensagem do usuário
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Mostra "pensando..."
                with st.spinner("🌙 Luna está pensando..."):
                    # Obtém a resposta
                    resposta = luna.perguntar(prompt)
                
                # Adiciona a resposta
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                
                # Atualiza a página
                st.rerun()

# ============================================
# RODAPÉ
# ============================================
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 30px;">
    🌙 Luna - 100% Offline • Seus dados ficam só com você • Feito com 💜
</div>
""", unsafe_allow_html=True)