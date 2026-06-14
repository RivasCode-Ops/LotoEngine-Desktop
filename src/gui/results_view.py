import customtkinter as ctk


class ResultsView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self.frame, state="disabled", wrap="none", font=ctk.CTkFont(family="Consolas", size=13))
        self.textbox.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ctk.CTkScrollbar(self.frame, orientation="vertical", command=self.textbox.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.textbox.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ctk.CTkScrollbar(self.frame, orientation="horizontal", command=self.textbox.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.textbox.configure(xscrollcommand=scrollbar_x.set)

    def exibir(self, jogos):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        cabecalho = (
            f"{'Jogo':<6} {'Numeros':<48} {'Repete':<24} {'Novos':<24} "
            f"{'Soma':<6} {'P/I':<6} {'Primos':<6} {'Status':<8}\n"
        )
        cabecalho += "-" * 130 + "\n"
        self.textbox.insert("end", cabecalho)

        for i, r in enumerate(jogos, 1):
            if "erro" in r:
                self.textbox.insert("end", f"{i:<6} ERRO: {r['erro']}\n")
                continue

            jogo = r["jogo"]
            repete = r["repete_do_ultimo"]
            novos = r["novos"]
            a = r["analise"]

            jogo_str = " ".join(f"{n:02d}" for n in jogo)
            repete_str = " ".join(f"{n:02d}" for n in repete)
            novos_str = " ".join(f"{n:02d}" for n in novos)
            status = "OK" if a["valido"] else "FAIL"

            self.textbox.insert("end",
                f"{i:<6} {jogo_str:<48} {repete_str:<24} {novos_str:<24} "
                f"{a['soma']:<6} {a['impares']}/{a['pares']:<4} {a['primos']:<6} {status:<8}\n"
            )

        self.textbox.configure(state="disabled")
