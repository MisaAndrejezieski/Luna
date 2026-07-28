# ============================================
# src/ia.py - Lógica da IA da Luna
# ============================================
"""
Módulo de lógica da IA para a assistente Luna.

Gerencia a conexão com o Ollama, o histórico de conversas
e as interações com o modelo de linguagem.
"""

# Importações padrão
import subprocess
from typing import List, Optional

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
# Importações de terceiros
from langchain_ollama import OllamaLLM

# Importações do projeto
from src.config import MAX_TOKENS, MODELO_PADRAO, NOME_ASSISTENTE, TEMPERATURA


class AssistenteProgramacao:
    """
    Classe principal da assistente de programação.
    
    Gerencia a interação com o modelo de linguagem, mantém
    o histórico da conversa e fornece métodos para perguntar,
    limpar memória e trocar modelos.
    
    Atributos:
        nome (str): Nome da assistente
        modelo (str): Nome do modelo atual
        llm (OllamaLLM): Instância do modelo
        memory (ConversationBufferMemory): Memória da conversa
        conversation (ConversationChain): Cadeia de conversação
    """
    
    def __init__(self, modelo: str = MODELO_PADRAO):
        """
        Inicializa a assistente com um modelo específico.
        
        Args:
            modelo (str): Nome do modelo no Ollama (ex: "phi3", "llama3.2")
        """
        self.nome = NOME_ASSISTENTE
        self.modelo = modelo
        self.llm: Optional[OllamaLLM] = None
        self.memory: Optional[ConversationBufferMemory] = None
        self.conversation: Optional[ConversationChain] = None
        
        # Tenta inicializar o modelo
        self.inicializar()
    
    def inicializar(self) -> bool:
        """
        Inicializa ou reinicializa o modelo e a memória.
        
        Este método é chamado no construtor e também quando
        o usuário troca de modelo.
        
        Returns:
            bool: True se inicializou com sucesso, False caso contrário
        """
        try:
            # Cria a instância do modelo com configurações
            self.llm = OllamaLLM(
                model=self.modelo,
                temperature=TEMPERATURA,
                max_tokens=MAX_TOKENS,
                # verbose=True  # Descomente para debug
            )
            
            # Cria a memória para armazenar o histórico
            self.memory = ConversationBufferMemory()
            
            # Cria a cadeia de conversação
            self.conversation = ConversationChain(
                llm=self.llm,
                memory=self.memory,
                verbose=False  # Mude para True para ver os "pensamentos" da IA
            )
            
            print(f"✅ {self.nome} inicializada com sucesso! Modelo: {self.modelo}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar {self.nome}: {e}")
            return False
    
    def perguntar(self, pergunta: str) -> str:
        """
        Envia uma pergunta para a assistente e retorna a resposta.
        
        Args:
            pergunta (str): Pergunta do usuário
            
        Returns:
            str: Resposta da assistente ou mensagem de erro
        """
        if not self.conversation:
            return "❌ Desculpe, a Luna não está inicializada corretamente."
        
        try:
            # Cria um prompt com a personalidade da Luna
            prompt = f"""
            Você é a Luna, uma assistente de programação amigável, paciente e offline.
            
            CARACTERÍSTICAS:
            - Você é acolhedora e encorajadora
            - Explica conceitos de forma clara e didática
            - Adora ajudar com código e programação
            - Seu tom é sempre positivo e motivador
            - Você é especialista em Python, mas também conhece JavaScript, Java, C++, etc.
            - Quando não sabe algo, você admite e sugere onde pesquisar
            
            PERGUNTA DO USUÁRIO:
            {pergunta}
            
            Sua resposta (seja amigável e útil):
            """
            
            # Envia o prompt para o modelo
            resposta = self.conversation.predict(input=prompt)
            return resposta.strip()
            
        except Exception as e:
            return f"❌ Desculpe, tive um erro ao processar sua pergunta: {e}"
    
    def limpar_memoria(self) -> None:
        """
        Limpa o histórico da conversa.
        
        Útil para começar uma nova conversa sem o contexto anterior.
        """
        if self.memory:
            self.memory.clear()
            print("🧹 Memória da Luna limpa!")
    
    def trocar_modelo(self, novo_modelo: str) -> bool:
        """
        Troca o modelo de IA em uso.
        
        Args:
            novo_modelo (str): Nome do novo modelo
            
        Returns:
            bool: True se a troca foi bem-sucedida
        """
        if novo_modelo == self.modelo:
            return True
        
        self.modelo = novo_modelo
        return self.inicializar()
    
    def listar_modelos_disponiveis(self) -> List[str]:
        """
        Lista todos os modelos disponíveis no Ollama.
        
        Returns:
            List[str]: Lista de nomes dos modelos instalados
        """
        try:
            # Executa o comando 'ollama list'
            resultado = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10  # Timeout para não travar
            )
            
            if resultado.returncode == 0:
                # Processa a saída do comando
                linhas = resultado.stdout.strip().split('\n')
                if len(linhas) <= 1:
                    return []  # Nenhum modelo encontrado
                
                # Pula o cabeçalho e extrai os nomes dos modelos
                modelos = []
                for linha in linhas[1:]:
                    if linha.strip():
                        # O nome é a primeira coluna
                        nome_modelo = linha.split()[0]
                        modelos.append(nome_modelo)
                return modelos
            
            return []
            
        except subprocess.TimeoutExpired:
            print("⏰ Timeout ao listar modelos")
            return []
        except FileNotFoundError:
            print("❌ Ollama não encontrado. Certifique-se de que está instalado.")
            return []
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            return []
    
    def verificar_modelo_instalado(self, nome_modelo: str) -> bool:
        """
        Verifica se um modelo específico está instalado.
        
        Args:
            nome_modelo (str): Nome do modelo a verificar
            
        Returns:
            bool: True se o modelo estiver instalado
        """
        modelos = self.listar_modelos_disponiveis()
        return nome_modelo in modelos
    
    def get_status(self) -> dict:
        """
        Retorna o status atual da assistente.
        
        Returns:
            dict: Dicionário com informações de status
        """
        return {
            "nome": self.nome,
            "modelo": self.modelo,
            "modelo_instalado": self.verificar_modelo_instalado(self.modelo),
            "conversation_active": self.conversation is not None,
            "temperatura": TEMPERATURA,
            "max_tokens": MAX_TOKENS
        }