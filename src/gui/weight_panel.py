import customtkinter as ctk


class WeightPanel:
    def __init__(self, parent, on_change_callback=None):
        self.on_change = on_change_callback
        self.pesos = {"soma": 1.0, "par_impar": 1.0, "primos": 1.0}

        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame, text="Criterio", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(self.frame, text="Peso", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(self.frame, text="Valor", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.sliders = {}
        self.labels = {}

        for i, (key, label) in enumerate([
            ("soma", "Soma (180-220)"),
            ("par_impar", "Pares / Impares (8/7)"),
            ("primos", "Numeros Primos (5-6)"),
        ], start=1):
            ctk.CTkLabel(self.frame, text=label).grid(row=i, column=0, padx=10, pady=8, sticky="w")

            slider = ctk.CTkSlider(self.frame, from_=0, to=3, number_of_steps=30)
            slider.set(self.pesos[key])
            slider.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
            slider.configure(command=lambda v, k=key: self._atualizar(k, v))
            self.sliders[key] = slider

            lbl = ctk.CTkLabel(self.frame, text=f"{self.pesos[key]:.1f}", width=40)
            lbl.grid(row=i, column=2, padx=10, pady=8, sticky="e")
            self.labels[key] = lbl

        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=3, pady=15)

        ctk.CTkButton(btn_frame, text="Resetar", command=self._resetar, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Salvar Pesos", command=self._salvar, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Carregar Pesos", command=self._carregar, width=110).pack(side="left", padx=5)

    def _atualizar(self, key, valor):
        v = round(valor, 1)
        self.pesos[key] = v
        self.labels[key].configure(text=f"{v:.1f}")
        if self.on_change:
            self.on_change(self.pesos)

    def _resetar(self):
        for key in self.pesos:
            self.pesos[key] = 1.0
            self.sliders[key].set(1.0)
            self.labels[key].configure(text="1.0")
        if self.on_change:
            self.on_change(self.pesos)

    def _salvar(self):
        try:
            from src.data.loader import CarregadorDados
            CarregadorDados.salvar_pesos("data/pesos_config.json", self.pesos)
        except Exception:
            pass

    def _carregar(self):
        try:
            from src.data.loader import CarregadorDados
            import os
            if os.path.exists("data/pesos_config.json"):
                self.pesos = CarregadorDados.carregar_pesos("data/pesos_config.json")
                for key, v in self.pesos.items():
                    self.sliders[key].set(v)
                    self.labels[key].configure(text=f"{v:.1f}")
                if self.on_change:
                    self.on_change(self.pesos)
        except Exception:
            pass

    def obter_pesos(self):
        return dict(self.pesos)
