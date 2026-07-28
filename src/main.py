# ============================================
# src/main.py - Interface Gráfica da Luna
# ============================================
"""
Módulo da interface gráfica da assistente Luna.

Utiliza CustomTkinter para uma interface moderna e responsiva.
Inclui área de chat, entrada de texto e controles para
gerenciar a conversa e os modelos.
"""

# Importações padrão
import threading
from typing import Optional

# Importações de terceiros
import customtkinter as ctk

# Importações do projeto
from src.ia import AssistenteProgramacao
from src.config import (
    NOME_ASSISTENTE,
    EMOJI,
    SAUDACAO,
    COR_PRIMARIA,
    COR_SECUNDARIA,
    COR_FUNDO,
    TEMA,
    JANELA_LARGURA,
    JANELA_ALTURA,
    FRASES,
)


class AppLuna:
    """
    Classe principal da aplicação Luna.
    
    Gerencia a janela principal, todos os widgets da interface,
    a comunicação com a assistente e a atualização da tela.
    """
    
    def __init__(self):
        """
        Inicializa a aplicação, a assistente e a interface gráfica.
        """
        # ============================================
        # INICIALIZA A ASSISTENTE
        # ============================================
        self.assistente = AssistenteProgramacao()
        self.nome = NOME_ASSISTENTE
        self.emoji = EMOJI
        
        # ============================================
        # CONFIGURA A JANELA PRINCIPAL
        # ============================================
        # Aplica o tema configurado
        ctk.set_appearance_mode(TEMA)
        ctk.set_default_color_theme("dark-blue")
        
        # Cria a janela
        self.janela = ctk.CTk()
        self.janela.title(f"{EMOJI} Luna - Assistente de Programação Offline")
        self.janela.geometry(f"{JANELA_LARGURA}x{JANELA_ALTURA}")
        self.janela.minsize(800, 600)
        
        # Tenta carregar o ícone (se existir)
        try:
            self.janela.iconbitmap("assets/luna.ico")
        except Exception:
            pass  # Ícone não encontrado, continua sem
        
        # Configura o grid principal
        self.janela.grid_rowconfigure(0, weight=0)  # Header
        self.janela.grid_rowconfigure(1, weight=1)  # Chat
        self.janela.grid_rowconfigure(2, weight=0)  # Input
        self.janela.grid_columnconfigure(0, weight=1)
        
        # ============================================
        # CRIA OS WIDGETS DA INTERFACE
        # ============================================
        self.criar_widgets()
        
        # Exibe a mensagem de boas-vindas
        self.mostrar_boas_vindas()
    
    def criar_widgets(self):
        """
        Cria e organiza todos os widgets da interface.
        """
        # ============================================
        # HEADER (Barra Superior)
        # ============================================
        header = ctk.CTkFrame(
            self.janela,
            height=70,
            fg_color=COR_PRIMARIA
        )
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header.grid_columnconfigure(0, weight=0)  # Logo
        header.grid_columnconfigure(1, weight=1)  # Título
        header.grid_columnconfigure(2, weight=0)  # Status
        header.grid_columnconfigure(3, weight=0)  # Botões
        
        # ----- LOGO DA LUNA -----
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=15, pady=10)
        
        # Emoji grande
        logo_label = ctk.CTkLabel(
            logo_frame,
            text=EMOJI,
            font=ctk.CTkFont(size=32)
        )
        logo_label.pack(side="left")
        
        # Nome "Luna" em destaque
        nome_label = ctk.CTkLabel(
            logo_frame,
            text=self.nome,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        nome_label.pack(side="left", padx=(5, 0))
        
        # ----- TÍTULO E SUBTÍTULO -----
        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.grid(row=0, column=1, sticky="w", padx=10)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="Assistente de Programação Offline",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        titulo.pack(anchor="w")
        
        subtitulo = ctk.CTkLabel(
            titulo_frame,
            text="100% local - seus dados ficam com você 🤫",
            font=ctk.CTkFont(size=11),
            text_color="white"
        )
        subtitulo.pack(anchor="w")
        
        # ----- STATUS E MODELO ATUAL -----
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=2, padx=15, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text=f"🧠 {self.assistente.modelo}",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        self.status_label.pack()
        
        # ----- BOTÕES DE AÇÃO -----
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.grid(row=0, column=3, padx=10, pady=10)
        
        # Botão Limpar
        btn_limpar = ctk.CTkButton(
            btn_frame,
            text="🧹 Limpar",
            width=80,
            height=32,
            fg_color="white",
            text_color=COR_PRIMARIA,
            hover_color="#E0E0E0",
            command=self.limpar_historico
        )
        btn_limpar.pack(side="left", padx=3)
        
        # Botão Trocar Modelo
        btn_modelos = ctk.CTkButton(
            btn_frame,
            text="🔄 Trocar",
            width=80,
            height=32,
            fg_color="white",
            text_color=COR_PRIMARIA,
            hover_color="#E0E0E0",
            command=self.abrir_trocar_modelo
        )
        btn_modelos.pack(side="left", padx=3)
        
        # ============================================
        # ÁREA DO CHAT
        # ============================================
        self.chat_frame = ctk.CTkScrollableFrame(self.janela)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # ============================================
        # ÁREA DE INPUT (Campo de texto + Botão)
        # ============================================
        input_frame = ctk.CTkFrame(self.janela)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=0)
        
        # Campo de texto
        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=60,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=COR_PRIMARIA
        )
        self.input_text.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Adiciona texto de placeholder manualmente
        self.input_text.insert("1.0", "Digite sua pergunta para a Luna...")
        self.input_text.configure(fg_color="#2D2D44")
        
        # Evento para limpar o placeholder quando clicar
        def on_click(event):
            if self.input_text.get("1.0", "end-1c") == "Digite sua pergunta para a Luna...":
                self.input_text.delete("1.0", "end")
                self.input_text.configure(fg_color="white")
        
        self.input_text.bind("<Button-1>", on_click)
        
        # Eventos de tecla
        self.input_text.bind("<Shift-Return>", self.enviar_mensagem_event)
        self.input_text.bind("<Return>", self.enviar_mensagem_event)
        
        # Botão Enviar
        self.btn_enviar = ctk.CTkButton(
            input_frame,
            text="📤 Enviar",
            width=100,
            height=60,
            fg_color=COR_PRIMARIA,
            hover_color=COR_SECUNDARIA,
            command=self.enviar_mensagem
        )
        self.btn_enviar.grid(row=0, column=1, sticky="e")
    
    def mostrar_boas_vindas(self):
        """
        Exibe a mensagem de boas-vindas com a saudação da Luna.
        """
        saudacao = SAUDACAO.format(modelo=self.assistente.modelo)
        self.adicionar_mensagem("🌙 Luna", saudacao, is_luna=True)
    
    def enviar_mensagem_event(self, event=None):
        """
        Callback para eventos de tecla no campo de texto.
        """
        if event and event.keysym == "Return":
            if event.state & 0x1:  # Shift pressionado
                return
            self.enviar_mensagem()
            return "break"
    
    def enviar_mensagem(self):
        """
        Envia a mensagem do usuário para a assistente Luna.
        """
        # Coleta e valida o texto
        texto = self.input_text.get("1.0", "end-1c").strip()
        if not texto or texto == "Digite sua pergunta para a Luna...":
            return
        
        # Adiciona a mensagem do usuário ao chat
        self.adicionar_mensagem("👤 Você", texto)
        
        # Limpa o campo de texto
        self.input_text.delete("1.0", "end")
        
        # Desabilita o botão durante o processamento
        self.btn_enviar.configure(
            state="disabled",
            text="⏳ Pensando..."
        )
        
        # Processa em uma thread separada
        thread = threading.Thread(target=self.processar_resposta, args=(texto,))
        thread.daemon = True
        thread.start()
    
    def processar_resposta(self, pergunta: str):
        """
        Processa a resposta da Luna em background.
        """
        try:
            resposta = self.assistente.perguntar(pergunta)
            self.janela.after(0, lambda: self.adicionar_mensagem("🌙 Luna", resposta, True))
        except Exception as e:
            msg_erro = f"❌ Desculpe, tive um problema: {e}"
            self.janela.after(0, lambda: self.adicionar_mensagem("🌙 Luna", msg_erro, True))
        finally:
            # Reabilita o botão - usando lambda para evitar problemas
            self.janela.after(0, lambda: self.btn_enviar.configure(state="normal", text="📤 Enviar"))
    
    def adicionar_mensagem(self, remetente: str, texto: str, is_luna: bool = False):
        """
        Adiciona uma nova mensagem ao chat com estilização.
        """
        # Cria o frame da mensagem
        frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COR_PRIMARIA if is_luna else "#2D2D44"
        )
        frame.pack(fill="x", padx=5, pady=3)
        
        # Label do remetente
        cor_remetente = "white" if is_luna else "#64B5F6"
        nome = ctk.CTkLabel(
            frame,
            text=remetente,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=cor_remetente
        )
        nome.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Texto da mensagem
        texto_widget = ctk.CTkTextbox(
            frame,
            height=50,
            font=ctk.CTkFont(size=13),
            wrap="word",
            fg_color="transparent",
            border_width=0,
            text_color="white" if is_luna else "#E0E0E0"
        )
        texto_widget.insert("1.0", texto)
        texto_widget.configure(state="disabled")
        
        # Ajusta a altura
        linhas = texto.count('\n') + 1
        if linhas > 10:
            linhas = 10
        texto_widget.configure(height=linhas * 20 + 20)
        texto_widget.pack(fill="x", padx=10, pady=(0, 5))
        
        # Rola para o final
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def limpar_historico(self):
        """
        Limpa o histórico da conversa e o chat.
        """
        self.assistente.limpar_memoria()
        
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        self.adicionar_mensagem(
            "🌙 Luna",
            FRASES["limpeza"],
            is_luna=True
        )
    
    def abrir_trocar_modelo(self):
        """
        Abre uma janela modal para trocar o modelo de IA.
        """
        dialog = ctk.CTkToplevel(self.janela)
        dialog.title(f"{EMOJI} Luna - Trocar Modelo")
        dialog.geometry("400x350")
        dialog.transient(self.janela)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.janela.winfo_x() + (self.janela.winfo_width() - 400) // 2
        y = self.janela.winfo_y() + (self.janela.winfo_height() - 350) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Título
        titulo = ctk.CTkLabel(
            dialog,
            text="🌙 Escolha o modelo para a Luna:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=(20, 5))
        
        subtitulo = ctk.CTkLabel(
            dialog,
            text="Modelos disponíveis no Ollama",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 15))
        
        modelos = self.assistente.listar_modelos_disponiveis()
        if not modelos:
            modelos = ["phi3", "llama3.2", "mistral", "codellama", "deepseek-coder"]
        
        modelo_atual = self.assistente.modelo
        if modelo_atual in modelos:
            indice_atual = modelos.index(modelo_atual)
        else:
            indice_atual = 0
        
        combo = ctk.CTkOptionMenu(
            dialog,
            values=modelos,
            dropdown_font=ctk.CTkFont(size=13),
            fg_color=COR_PRIMARIA,
            button_color=COR_PRIMARIA,
            button_hover_color=COR_SECUNDARIA
        )
        combo.pack(pady=10)
        combo.set(modelo_atual)
        
        info_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        info_frame.pack(pady=10)
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Dicas de modelos:\n"
                 "• phi3  - Leve e rápido (recomendado)\n"
                 "• llama3.2 - Mais inteligente (mais pesado)\n"
                 "• mistral - Bom custo-benefício\n"
                 "• deepseek-coder - Especializado em código",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        info_text.pack()
        
        def confirmar():
            novo_modelo = combo.get()
            if novo_modelo and novo_modelo != self.assistente.modelo:
                sucesso = self.assistente.trocar_modelo(novo_modelo)
                if sucesso:
                    self.status_label.configure(text=f"🧠 {novo_modelo}")
                    self.adicionar_mensagem(
                        "🌙 Luna",
                        FRASES["troca_modelo"].format(modelo=novo_modelo),
                        is_luna=True
                    )
                else:
                    self.adicionar_mensagem(
                        "🌙 Luna",
                        f"❌ Não foi possível trocar para {novo_modelo}.",
                        is_luna=True
                    )
            dialog.destroy()
        
        btn_confirmar = ctk.CTkButton(
            dialog,
            text="✅ Confirmar Troca",
            fg_color=COR_PRIMARIA,
            hover_color=COR_SECUNDARIA,
            command=confirmar,
            height=40
        )
        btn_confirmar.pack(pady=20)
        
        btn_cancelar = ctk.CTkButton(
            dialog,
            text="❌ Cancelar",
            fg_color="transparent",
            text_color="gray",
            hover_color="#333333",
            command=dialog.destroy,
            height=30
        )
        btn_cancelar.pack(pady=(0, 10))
    
    def run(self):
        """
        Inicia o loop principal da aplicação.
        """
        self.janela.mainloop()


if __name__ == "__main__":
    app = AppLuna()
    app.run()