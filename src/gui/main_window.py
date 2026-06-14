import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.core.generator import Gerador9_6
from src.core.analyzer import Analisador
from src.core.auditor import Auditor
from src.data.loader import CarregadorDados
from src.gui.weight_panel import WeightPanel
from src.gui.results_view import ResultsView
from src.gui.charts_view import ChartsView
from src.database.migrations import rodar_migracoes
from src.database.models import ConcursoDB, JogoDB, AuditoriaDB


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LotoEngine Desktop - Algoritmo 9/6")
        self.geometry("1100x750")
        self.minsize(900, 600)

        rodar_migracoes()

        self.concurso_db = ConcursoDB()
        self.jogo_db = JogoDB()
        self.auditoria_db = AuditoriaDB()
        self.generator = Gerador9_6()
        self.analyzer = Analisador()
        self.auditor = Auditor()
        self.loader = CarregadorDados()
        self.df_historico = None
        self.ultimo_concurso = None
        self.jogos_gerados = []

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, corner_radius=0, height=50)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="LotoEngine Desktop", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(side="left", padx=20, pady=10)

        self.mode_switch = ctk.CTkSwitch(
            header, text="Dark Mode", command=self._toggle_mode, onvalue=True, offvalue=False
        )
        self.mode_switch.select()
        self.mode_switch.pack(side="right", padx=20, pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.tab_entrada = self.tabview.add("Entrada")
        self.tab_geracao = self.tabview.add("Geracao")
        self.tab_pesos = self.tabview.add("Pesos")
        self.tab_auditoria = self.tabview.add("Auditoria")
        self.tab_graficos = self.tabview.add("Graficos")

        self._build_entrada_tab()
        self._build_geracao_tab()
        self._build_pesos_tab()
        self._build_auditoria_tab()
        self._build_graficos_tab()

        self.status_bar = ctk.CTkLabel(self, text="Pronto", anchor="w", height=24)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))

    def _toggle_mode(self):
        novo = "dark" if self.mode_switch.get() else "light"
        ctk.set_appearance_mode(novo)

    def _build_entrada_tab(self):
        self.tab_entrada.grid_columnconfigure(0, weight=1)
        self.tab_entrada.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self.tab_entrada, text="Entrada de Dados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")

        frame_import = ctk.CTkFrame(self.tab_entrada)
        frame_import.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        frame_import.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(frame_import, text="Carregar CSV", command=self._carregar_csv).grid(row=0, column=0, padx=5, pady=10)
        ctk.CTkButton(frame_import, text="Carregar Excel", command=self._carregar_excel).grid(row=0, column=1, padx=5, pady=10)
        ctk.CTkButton(frame_import, text="Gerar Exemplo (100 concursos)", command=self._gerar_exemplo).grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkButton(frame_import, text="Salvar no Banco", command=self._salvar_concursos_db).grid(row=0, column=3, padx=5, pady=10)

        frame_manual = ctk.CTkFrame(self.tab_entrada)
        frame_manual.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        frame_manual.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_manual, text="Ultimo concurso (15 nums):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_ultimo = ctk.CTkEntry(frame_manual, placeholder_text="Ex: 1 2 5 7 8 9 11 13 14 17 19 20 22 24 25")
        self.entry_ultimo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_manual, text="Usar", command=self._usar_manual, width=60).grid(row=0, column=2, padx=10, pady=10)

        self.info_entrada = ctk.CTkTextbox(self.tab_entrada, height=150, state="disabled", wrap="word")
        self.info_entrada.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")

    def _build_geracao_tab(self):
        self.tab_geracao.grid_columnconfigure(0, weight=1)
        self.tab_geracao.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.tab_geracao, text="Motor de Geracao 9/6",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")

        frame_controls = ctk.CTkFrame(self.tab_geracao)
        frame_controls.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        frame_controls.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(frame_controls, text="Quantidade:").grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.spin_qtd = ctk.CTkEntry(frame_controls, width=60)
        self.spin_qtd.insert(0, "5")
        self.spin_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.var_forcado = ctk.CTkCheckBox(frame_controls, text="Busca exaustiva", onvalue=True, offvalue=False)
        self.var_forcado.grid(row=0, column=2, padx=5, pady=10)

        ctk.CTkButton(frame_controls, text="Gerar Jogos", command=self._gerar_jogos, width=120).grid(row=0, column=3, padx=10, pady=10)

        self.results_view = ResultsView(self.tab_geracao)
        self.results_view.frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

    def _build_pesos_tab(self):
        self.tab_pesos.grid_columnconfigure(0, weight=1)
        self.tab_pesos.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.tab_pesos, text="Painel de Pesos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")

        ctk.CTkLabel(
            self.tab_pesos,
            text="Ajuste a importancia de cada criterio de filtragem (0.0 a 3.0)",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=20, sticky="w")

        self.weight_panel = WeightPanel(self.tab_pesos, self._on_pesos_change)
        self.weight_panel.frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

    def _build_auditoria_tab(self):
        self.tab_auditoria.grid_columnconfigure(0, weight=1)
        self.tab_auditoria.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self.tab_auditoria, text="Auditoria e Comparativo",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")

        frame_audit = ctk.CTkFrame(self.tab_auditoria)
        frame_audit.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        frame_audit.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_audit, text="Resultado oficial (15 nums):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_oficial = ctk.CTkEntry(frame_audit, placeholder_text="Ex: 1 3 5 7 9 11 13 15 17 19 21 22 23 24 25")
        self.entry_oficial.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_audit, text="Auditar", command=self._auditar, width=80).grid(row=0, column=2, padx=10, pady=10)

        self.info_auditoria = ctk.CTkTextbox(self.tab_auditoria, height=200, state="disabled", wrap="word")
        self.info_auditoria.grid(row=2, column=0, pady=5, padx=20, sticky="ew")

        frame_hist = ctk.CTkFrame(self.tab_auditoria)
        frame_hist.grid(row=3, column=0, pady=5, padx=20, sticky="nsew")
        frame_hist.grid_columnconfigure(0, weight=1)
        frame_hist.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame_hist, text="Historico de Auditoria",
                      font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=5, sticky="w")

        self.hist_auditoria = ctk.CTkTextbox(frame_hist, height=150, state="disabled", wrap="word")
        self.hist_auditoria.grid(row=1, column=0, pady=5, sticky="nsew")

    def _build_graficos_tab(self):
        self.tab_graficos.grid_columnconfigure(0, weight=1)
        self.tab_graficos.grid_rowconfigure(0, weight=1)

        self.charts_view = ChartsView(self.tab_graficos, self.analyzer)
        self.charts_view.frame.grid(row=0, column=0, sticky="nsew")

    def _log(self, widget, texto):
        widget.configure(state="normal")
        widget.insert("end", texto + "\n")
        widget.see("end")
        widget.configure(state="disabled")

    def _set_status(self, texto):
        self.status_bar.configure(text=texto)

    def _carregar_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        df = self.loader.carregar_csv(path)
        if df is not None:
            self.df_historico = df
            self.analyzer.carregar_historico(df)
            self.ultimo_concurso = self.loader.extrair_ultimo_concurso(df)
            self._log(self.info_entrada, f"CSV carregado: {len(df)} concursos")
            if self.ultimo_concurso:
                self._log(self.info_entrada, f"Ultimo concurso: {self.ultimo_concurso}")
                self._exibir_estatisticas()
            self._set_status(f"Carregado: {len(df)} concursos")
        else:
            messagebox.showerror("Erro", "Formato CSV invalido. Necessario colunas Bola1..Bola15")

    def _carregar_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not path:
            return
        df = self.loader.carregar_excel(path)
        if df is not None:
            self.df_historico = df
            self.analyzer.carregar_historico(df)
            self.ultimo_concurso = self.loader.extrair_ultimo_concurso(df)
            self._log(self.info_entrada, f"Excel carregado: {len(df)} concursos")
            if self.ultimo_concurso:
                self._log(self.info_entrada, f"Ultimo concurso: {self.ultimo_concurso}")
                self._exibir_estatisticas()
            self._set_status(f"Carregado: {len(df)} concursos")
        else:
            messagebox.showerror("Erro", "Formato Excel invalido. Necessario colunas Bola1..Bola15")

    def _gerar_exemplo(self):
        self.df_historico = self.loader.gerar_resultados_exemplo()
        self.analyzer.carregar_historico(self.df_historico)
        self.ultimo_concurso = self.loader.extrair_ultimo_concurso(self.df_historico)
        self._log(self.info_entrada, "Dados de exemplo gerados: 100 concursos")
        if self.ultimo_concurso:
            self._log(self.info_entrada, f"Ultimo concurso: {self.ultimo_concurso}")
            self._exibir_estatisticas()
        self._set_status("Exemplo carregado: 100 concursos")

    def _salvar_concursos_db(self):
        if self.df_historico is None or self.df_historico.empty:
            messagebox.showwarning("Aviso", "Carregue dados primeiro")
            return
        colunas_bola = sorted([c for c in self.df_historico.columns if "bola" in c.lower()])[:15]
        if len(colunas_bola) < 15:
            messagebox.showerror("Erro", "Colunas das bolas nao encontradas")
            return
        importados = 0
        for _, row in self.df_historico.iterrows():
            nums = sorted([int(row[c]) for c in colunas_bola])
            concurso_num = int(row.get("Concurso", importados + 1))
            data = str(row.get("Data", ""))
            self.concurso_db.inserir(concurso_num, data, nums)
            importados += 1
        total = self.concurso_db.contar()
        self._log(self.info_entrada, f"Salvo no banco: {total} concursos")
        self._set_status(f"Banco: {total} concursos")

    def _exibir_estatisticas(self):
        resumo = self.analyzer.resumo_historico()
        if "erro" not in resumo:
            self._log(self.info_entrada, f"Total: {resumo['total_concursos']} | "
                      f"Media soma: {resumo['media_soma']:.1f} | "
                      f"Mais frequente: #{resumo['numero_mais_frequente']} ({resumo['frequencia_max']}x) | "
                      f"Menos frequente: #{resumo['numero_menos_frequente']} ({resumo['frequencia_min']}x)")

    def _usar_manual(self):
        raw = self.entry_ultimo.get().strip()
        try:
            nums = sorted([int(x) for x in raw.split()])
            if len(nums) != 15 or len(set(nums)) != 15 or any(n < 1 or n > 25 for n in nums):
                messagebox.showerror("Erro", "Digite 15 numeros unicos entre 1 e 25")
                return
            self.ultimo_concurso = nums
            self._log(self.info_entrada, f"Ultimo concurso (manual): {nums}")
            self._set_status("Ultimo concurso definido manualmente")
        except ValueError:
            messagebox.showerror("Erro", "Entrada invalida")

    def _gerar_jogos(self):
        if self.ultimo_concurso is None:
            messagebox.showwarning("Aviso", "Defina o ultimo concurso primeiro (aba Entrada)")
            return

        try:
            qtd = int(self.spin_qtd.get())
        except ValueError:
            qtd = 5

        forcado = bool(self.var_forcado.get())
        self.generator.pesos = self.weight_panel.obter_pesos() if hasattr(self, "weight_panel") else self.generator.pesos

        self.jogos_gerados = self.generator.gerar_multiplos(self.ultimo_concurso, quantidade=qtd, forcado=forcado)

        ultimo_db = self.concurso_db.ultimo()
        concurso_base_id = ultimo_db["id"] if ultimo_db else None

        for r in self.jogos_gerados:
            if "erro" not in r:
                self.jogo_db.inserir(
                    r["jogo"], r["repete_do_ultimo"], r["novos"],
                    r["analise"], self.generator.pesos,
                    concurso_base_id=concurso_base_id,
                )

        self.results_view.exibir(self.jogos_gerados)
        self._set_status(f"{qtd} jogos gerados e salvos no banco")

    def _on_pesos_change(self, pesos):
        self.generator.pesos = pesos
        self._set_status(f"Pesos atualizados: soma={pesos['soma']:.1f}, par_impar={pesos['par_impar']:.1f}, primos={pesos['primos']:.1f}")

    def _auditar(self):
        if not self.jogos_gerados:
            messagebox.showwarning("Aviso", "Gere jogos primeiro (aba Geracao)")
            return

        raw = self.entry_oficial.get().strip()
        try:
            oficial = sorted([int(x) for x in raw.split()])
            if len(oficial) != 15 or len(set(oficial)) != 15 or any(n < 1 or n > 25 for n in oficial):
                messagebox.showerror("Erro", "Digite 15 numeros unicos entre 1 e 25")
                return
        except ValueError:
            messagebox.showerror("Erro", "Entrada invalida")
            return

        jogos = [r["jogo"] for r in self.jogos_gerados if "erro" not in r]
        resultado = self.auditor.auditar_lote(jogos, oficial)

        self.info_auditoria.configure(state="normal")
        self.info_auditoria.delete("1.0", "end")
        self.info_auditoria.insert("end", f"Resultado Oficial: {oficial}\n")
        self.info_auditoria.insert("end", f"Total de jogos: {resultado['total_jogos']}\n")
        self.info_auditoria.insert("end", f"Premiados (11+): {resultado['total_premiados']}\n")
        self.info_auditoria.insert("end", f"Aproveitamento: {resultado['aproveitamento']}%\n\n")
        for r in resultado["resultados"]:
            self.info_auditoria.insert("end", f"Jogo: {r['jogo']} -> {r['quantidade']} acertos ({r['classificacao']})\n")

        ultimo_db = self.concurso_db.ultimo()
        concurso_id = ultimo_db["id"] if ultimo_db else None
        jogos_db = self.jogo_db.listar_ultimos(len(jogos))
        for i, r in enumerate(resultado["resultados"]):
            jogo_id = jogos_db[i]["id"] if i < len(jogos_db) else None
            if jogo_id:
                self.auditoria_db.inserir(jogo_id, oficial, r["quantidade"], r["classificacao"], r["premiado"], concurso_id)

        self.info_auditoria.configure(state="disabled")
        self._exibir_historico_auditoria()
        self._set_status(f"Auditoria: {resultado['total_premiados']}/{resultado['total_jogos']} premiados")

    def _exibir_historico_auditoria(self):
        stats = self.auditoria_db.estatisticas()
        self.hist_auditoria.configure(state="normal")
        self.hist_auditoria.delete("1.0", "end")
        self.hist_auditoria.insert("end", f"Total auditorias: {stats['total']}\n")
        self.hist_auditoria.insert("end", f"Total premiados: {stats['total_premiados']}\n")
        self.hist_auditoria.insert("end", f"Media de acertos: {stats['media_acertos']}\n")
        self.hist_auditoria.insert("end", f"Maximo acertos: {stats['max_acertos']}\n\n")

        ultimas = self.auditoria_db.ultimas_auditorias(10)
        if ultimas:
            self.hist_auditoria.insert("end", "Ultimas auditorias:\n")
            for a in ultimas:
                self.hist_auditoria.insert("end",
                    f"  {a['acertos']} acertos ({a['classificacao']}) - "
                    f"{'Premiado' if a['premiado'] else 'Nao premiado'}\n")
        self.hist_auditoria.configure(state="disabled")
