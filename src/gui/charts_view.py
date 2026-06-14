import customtkinter as ctk
from PIL import Image, ImageTk
import os

from src.core.charts import (
    gerar_frequencia,
    gerar_atraso,
    gerar_heatmap,
    gerar_evolucao_acertos,
)
from src.core.analyzer import Analisador


class ChartsView:
    def __init__(self, parent, analyzer: Analisador):
        self.analyzer = analyzer
        self._imagens = {}

        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.grid(row=0, column=0, pady=(10, 5), sticky="ew")
        header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(header, text="Visualizacao Grafica",
                      font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=5, pady=5)

        ctk.CTkButton(header, text="Frequencia", command=lambda: self._render("frequencia")).grid(row=1, column=0, padx=3, pady=5)
        ctk.CTkButton(header, text="Atraso", command=lambda: self._render("atraso")).grid(row=1, column=1, padx=3, pady=5)
        ctk.CTkButton(header, text="Heatmap", command=lambda: self._render("heatmap")).grid(row=1, column=2, padx=3, pady=5)
        ctk.CTkButton(header, text="Evolucao", command=lambda: self._render("evolucao")).grid(row=1, column=3, padx=3, pady=5)
        ctk.CTkButton(header, text="Atualizar Dados", command=self._atualizar_dados).grid(row=1, column=4, padx=3, pady=5)

        self.image_label = ctk.CTkLabel(self.frame, text="Clique em um grafico acima", font=ctk.CTkFont(size=14))
        self.image_label.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self._grafico_atual = None
        self._dados_atualizados = False

    def _atualizar_dados(self):
        self._dados_atualizados = True
        if self._grafico_atual:
            self._render(self._grafico_atual)

    def _render(self, tipo):
        self._grafico_atual = tipo
        freq = self.analyzer.frequencia_numeros()
        freq_dict = freq.to_dict() if not freq.empty else {}

        if tipo == "frequencia":
            path = gerar_frequencia(freq_dict)
        elif tipo == "atraso":
            atrasos = self.analyzer.atraso_numeros()
            atrasos_dict = atrasos.to_dict() if not atrasos.empty else {}
            path = gerar_atraso(atrasos_dict)
        elif tipo == "heatmap":
            path = gerar_heatmap(freq_dict)
        elif tipo == "evolucao":
            path = None
        else:
            return

        if path and os.path.exists(path):
            self._exibir_imagem(path)
        else:
            self.image_label.configure(text="Sem dados disponiveis para este grafico")

    def _exibir_imagem(self, path):
        try:
            pil_image = Image.open(path)
            label_w = self.image_label.winfo_width() or 800
            label_h = self.image_label.winfo_height() or 400
            pil_image.thumbnail((label_w, label_h), Image.LANCZOS)

            tk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
            self.image_label.configure(image=tk_img, text="")
            self._imagens["atual"] = tk_img
        except Exception as e:
            self.image_label.configure(text=f"Erro ao renderizar: {e}")
