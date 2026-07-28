# ============================================
# src/__init__.py - Pacote Principal da Luna
# ============================================
"""
Pacote principal da assistente Luna.

Este pacote contém toda a lógica da assistente de programação
offline, incluindo a interface gráfica, integração com IA
e configurações.

Módulos:
    - config: Configurações e identidade da Luna
    - ia: Lógica de integração com o Ollama
    - main: Interface gráfica principal
"""

from src.config import EMOJI, NOME_ASSISTENTE
from src.ia import AssistenteProgramacao

__version__ = "1.0.0"
__author__ = "Seu Nome"
__all__ = ["NOME_ASSISTENTE", "EMOJI", "AssistenteProgramacao"]