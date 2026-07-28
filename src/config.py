# ============================================
# src/config.py - Configurações da Luna
# ============================================
"""
Módulo de configurações da assistente Luna.

Contém todas as constantes, cores e configurações
que definem a identidade e comportamento da Luna.
"""

# ============================================
# IDENTIDADE DA LUNA
# ============================================

NOME_ASSISTENTE = "Luna"      # Nome da assistente
EMOJI = "🌙"                  # Emoji principal
TAG = f"{EMOJI} Luna"         # Tag para exibição

# Mensagem de saudação exibida ao iniciar
SAUDACAO = f"""
🌙 Olá! Sou a Luna, sua assistente de programação offline.

✨ Posso ajudar com:
- Código em Python, JavaScript, etc.
- Debug e correção de erros
- Explicações e documentação
- Sugestões de melhoria
- Algoritmos e estruturas de dados

💡 Dica: sou 100% offline, seus dados ficam só com você!
🔧 Atualmente usando o modelo: {{modelo}}
"""

# ============================================
# CORES E TEMA VISUAL
# ============================================

# Cores principais (tema noturno - combina com "Luna")
COR_PRIMARIA = "#6C63FF"      # Roxo principal - noturno
COR_SECUNDARIA = "#FF6B9D"    # Rosa - destaque
COR_TERCIARIA = "#00D4FF"     # Azul claro - detalhes
COR_FUNDO = "#1A1A2E"         # Fundo escuro como a noite
COR_TEXTO = "#FFFFFF"         # Texto branco

# Cores para mensagens
COR_USUARIO = "#64B5F6"       # Azul para mensagens do usuário
COR_LUNA = "#FFFFFF"          # Branco para mensagens da Luna

# Cores dos botões
COR_BOTAO_PRIMARIO = COR_PRIMARIA
COR_BOTAO_HOVER = COR_SECUNDARIA

# ============================================
# CONFIGURAÇÕES DA IA
# ============================================

MODELO_PADRAO = "phi3"        # Modelo inicial (leve e rápido)
TEMPERATURA = 0.7             # Criatividade (0.0 = conservador, 1.0 = criativo)
MAX_TOKENS = 2048             # Tamanho máximo da resposta
HISTORICO_MAXIMO = 50         # Número de mensagens no histórico

# ============================================
# CONFIGURAÇÕES DE INTERFACE
# ============================================

TEMA = "dark"                 # "dark" ou "light"
JANELA_LARGURA = 900          # Largura da janela principal
JANELA_ALTURA = 700           # Altura da janela principal
FONTE_PADRAO = "Segoe UI"     # Fonte principal
TAMANHO_FONTE = 14            # Tamanho da fonte

# ============================================
# FRASES CARACTERÍSTICAS DA LUNA
# ============================================

FRASES = {
    "pensando": "🌙 Deixa eu pensar um pouquinho...",
    "erro": "🌙 Ops! Tive um pequeno erro. Vamos tentar de novo?",
    "encorajamento": [
        "✨ Boa pergunta! Vou te ajudar com isso.",
        "🌟 Você está indo muito bem!",
        "💪 Que ótima dúvida! Vamos resolver juntos.",
        "🧠 Essa é uma questão interessante!"
    ],
    "despedida": "🌙 Até logo! Continue programando com a Luna!",
    "limpeza": "🧹 Histórico limpo! Pronta para mais perguntas.",
    "troca_modelo": "🔄 Modelo trocado para {modelo}! Pronta para ajudar.",
}