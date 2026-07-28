# ============================================
# src/ia.py - Lógica da IA da Luna (versão atualizada)
# ============================================
"""
Módulo de lógica da IA para a assistente Luna.

Gerencia a conexão com o Ollama, o histórico de conversas
e as interações com o modelo de linguagem.
"""

# Importações padrão
import subprocess
from typing import List, Optional

# Importações de terceiros - VERSÃO ATUALIZADA
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Importações do projeto
from src.config import (
    MODELO_PADRAO, 
    TEMPERATURA, 
    NOME_ASSISTENTE,
    MAX_TOKENS
)


class AssistenteProgramacao:
    """
    Classe principal da assistente de programação.
    
    Gerencia a interação com o modelo de linguagem, mantém
    o histórico da conversa e fornece métodos para perguntar,
    limpar memória e trocar modelos.
    """
    
    def __init__(self, modelo: str = MODELO_PADRAO):
        """
        Inicializa a assistente com um modelo específico.
        """
        self.nome = NOME_ASSISTENTE
        self.modelo = modelo
        self.llm: Optional[OllamaLLM] = None
        self.memory: Optional[ChatMessageHistory] = None
        self.chain: Optional[RunnableWithMessageHistory] = None
        self.session_id = "luna_session"
        
        # Tenta inicializar o modelo
        self.inicializar()
    
    def inicializar(self) -> bool:
        """
        Inicializa ou reinicializa o modelo e a memória.
        """
        try:
            # Cria a instância do modelo com configurações
            self.llm = OllamaLLM(
                model=self.modelo,
                temperature=TEMPERATURA,
                num_predict=MAX_TOKENS,
            )
            
            # Cria a memória para armazenar o histórico
            self.memory = ChatMessageHistory()
            
            # Adiciona uma mensagem de sistema com a personalidade da Luna
            self.memory.add_message(SystemMessage(
                content="""Você é a Luna, uma assistente de programação amigável, paciente e offline.

CARACTERÍSTICAS:
- Você é acolhedora e encorajadora
- Explica conceitos de forma clara e didática
- Adora ajudar com código e programação
- Seu tom é sempre positivo e motivador
- Você é especialista em Python, mas também conhece JavaScript, Java, C++, etc.
- Quando não sabe algo, você admite e sugere onde pesquisar

REGRAS:
- Sempre responda em português
- Seja detalhada nas explicações
- Ofereça exemplos de código quando relevante
- Pergunte se a pessoa precisa de mais esclarecimentos"""
            ))
            
            # Cria o template do prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é a Luna, uma assistente de programação amigável, paciente e offline.

CARACTERÍSTICAS:
- Você é acolhedora e encorajadora
- Explica conceitos de forma clara e didática
- Adora ajudar com código e programação
- Seu tom é sempre positivo e motivador
- Você é especialista em Python, mas também conhece JavaScript, Java, C++, etc.
- Quando não sabe algo, você admite e sugere onde pesquisar

REGRAS:
- Sempre responda em português
- Seja detalhada nas explicações
- Ofereça exemplos de código quando relevante"""),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
            
            # Cria a cadeia de conversação com histórico
            from langchain_core.runnables import RunnablePassthrough
            from langchain_core.output_parsers import StrOutputParser
            
            # Cria a cadeia básica
            chain = prompt | self.llm | StrOutputParser()
            
            # Adiciona histórico à cadeia
            self.chain = RunnableWithMessageHistory(
                chain,
                lambda session_id: self.memory,
                input_messages_key="input",
                history_messages_key="history",
            )
            
            print(f"✅ {self.nome} inicializada com sucesso! Modelo: {self.modelo}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar {self.nome}: {e}")
            return False
    
    def perguntar(self, pergunta: str) -> str:
        """
        Envia uma pergunta para a assistente e retorna a resposta.
        """
        if not self.chain:
            return "❌ Desculpe, a Luna não está inicializada corretamente."
        
        try:
            # Envia a pergunta com o session_id fixo
            resposta = self.chain.invoke(
                {"input": pergunta},
                config={"configurable": {"session_id": self.session_id}}
            )
            return resposta.strip()
            
        except Exception as e:
            return f"❌ Desculpe, tive um erro ao processar sua pergunta: {e}"
    
    def limpar_memoria(self) -> None:
        """
        Limpa o histórico da conversa.
        """
        if self.memory:
            self.memory.clear()
            # Re-adiciona a mensagem de sistema
            self.memory.add_message(SystemMessage(
                content="""Você é a Luna, uma assistente de programação amigável, paciente e offline.
                
CARACTERÍSTICAS:
- Você é acolhedora e encorajadora
- Explica conceitos de forma clara e didática
- Adora ajudar com código e programação
- Seu tom é sempre positivo e motivador
- Você é especialista em Python, mas também conhece JavaScript, Java, C++, etc.
- Quando não sabe algo, você admite e sugere onde pesquisar"""
            ))
            print("🧹 Memória da Luna limpa!")
    
    def trocar_modelo(self, novo_modelo: str) -> bool:
        """
        Troca o modelo de IA em uso.
        """
        if novo_modelo == self.modelo:
            return True
        
        self.modelo = novo_modelo
        return self.inicializar()
    
    def listar_modelos_disponiveis(self) -> List[str]:
        """
        Lista todos os modelos disponíveis no Ollama.
        """
        try:
            # Usa o caminho completo do Ollama
            ollama_path = r"C:\Users\Misa\AppData\Local\Programs\Ollama\ollama.exe"
            
            resultado = subprocess.run(
                [ollama_path, "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado.returncode == 0:
                linhas = resultado.stdout.strip().split('\n')
                if len(linhas) <= 1:
                    return []
                
                modelos = []
                for linha in linhas[1:]:
                    if linha.strip():
                        nome_modelo = linha.split()[0]
                        modelos.append(nome_modelo)
                return modelos
            
            return []
            
        except subprocess.TimeoutExpired:
            print("⏰ Timeout ao listar modelos")
            return []
        except FileNotFoundError:
            print("❌ Ollama não encontrado.")
            return []
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            return []
    
    def verificar_modelo_instalado(self, nome_modelo: str) -> bool:
        """
        Verifica se um modelo específico está instalado.
        """
        modelos = self.listar_modelos_disponiveis()
        return nome_modelo in modelos
    
    def get_status(self) -> dict:
        """
        Retorna o status atual da assistente.
        """
        return {
            "nome": self.nome,
            "modelo": self.modelo,
            "modelo_instalado": self.verificar_modelo_instalado(self.modelo),
            "conversation_active": self.chain is not None,
            "temperatura": TEMPERATURA,
            "max_tokens": MAX_TOKENS
        }