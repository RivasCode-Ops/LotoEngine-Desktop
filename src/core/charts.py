import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

from .validator import TOTAL_NUMEROS


plt.style.use("dark_background")

CHART_DIR = os.path.join(tempfile.gettempdir(), "lotoengine_charts")
os.makedirs(CHART_DIR, exist_ok=True)


def _limpar():
    for f in os.listdir(CHART_DIR):
        try:
            os.remove(os.path.join(CHART_DIR, f))
        except Exception:
            pass


def gerar_frequencia(frequencias, top_n=10):
    _limpar()
    fig, ax = plt.subplots(figsize=(10, 5))

    todos = list(range(1, TOTAL_NUMEROS + 1))
    valores = [frequencias.get(n, 0) for n in todos]

    cores = ["#2ecc71" if v > 0 else "#555555" for v in valores]
    ax.bar(todos, valores, color=cores, edgecolor="white", linewidth=0.5)

    destaques = sorted(
        [(n, frequencias.get(n, 0)) for n in todos],
        key=lambda x: x[1],
        reverse=True,
    )[:top_n]

    for n, v in destaques:
        ax.annotate(str(v), (n, v), ha="center", va="bottom", fontsize=8, color="#f1c40f")

    ax.set_xlabel("Numero", fontsize=11)
    ax.set_ylabel("Frequencia", fontsize=11)
    ax.set_title("Frequencia dos Numeros (1-25)", fontsize=14, fontweight="bold")
    ax.set_xticks(todos)
    ax.set_xticklabels(todos, fontsize=8)
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")
    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("#333")
    ax.spines["left"].set_color("#333")

    path = os.path.join(CHART_DIR, "frequencia.png")
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close(fig)
    return path


def gerar_atraso(atrasos):
    _limpar()
    fig, ax = plt.subplots(figsize=(10, 5))

    todos = list(range(1, TOTAL_NUMEROS + 1))
    valores = [atrasos.get(n, 0) for n in todos]

    max_atraso = max(valores) if valores else 1
    cores = []
    for v in valores:
        if v == 0:
            cores.append("#2ecc71")
        elif v < max_atraso * 0.3:
            cores.append("#f1c40f")
        elif v < max_atraso * 0.6:
            cores.append("#e67e22")
        else:
            cores.append("#e74c3c")

    ax.bar(todos, valores, color=cores, edgecolor="white", linewidth=0.5)

    for n, v in zip(todos, valores):
        if v > 0:
            ax.annotate(str(v), (n, v), ha="center", va="bottom", fontsize=7, color="#ccc")

    ax.set_xlabel("Numero", fontsize=11)
    ax.set_ylabel("Atraso (concursos)", fontsize=11)
    ax.set_title("Atraso dos Numeros", fontsize=14, fontweight="bold")
    ax.set_xticks(todos)
    ax.set_xticklabels(todos, fontsize=8)
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")
    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("#333")
    ax.spines["left"].set_color("#333")

    path = os.path.join(CHART_DIR, "atraso.png")
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close(fig)
    return path


def gerar_heatmap(frequencias):
    _limpar()
    fig, ax = plt.subplots(figsize=(8, 6))

    grid = np.zeros((5, 5))
    for n in range(1, 26):
        r, c = (n - 1) // 5, (n - 1) % 5
        grid[r, c] = frequencias.get(n, 0)

    max_val = grid.max() if grid.max() > 0 else 1
    norm_grid = grid / max_val

    cmap = plt.cm.Greens
    ax.matshow(norm_grid, cmap=cmap, aspect="auto")

    for i in range(5):
        for j in range(5):
            num = i * 5 + j + 1
            val = int(grid[i, j])
            ax.text(j, i, f"{num}\n({val})", ha="center", va="center", fontsize=9,
                    color="white" if norm_grid[i, j] > 0.5 else "#ccc", fontweight="bold")

    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(["1-5", "6-10", "11-15", "16-20", "21-25"])
    ax.set_yticklabels(["1-5", "6-10", "11-15", "16-20", "21-25"])
    ax.set_title("Heatmap de Frequencia (5x5)", fontsize=14, fontweight="bold", color="white")
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    path = os.path.join(CHART_DIR, "heatmap.png")
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close(fig)
    return path


def gerar_evolucao_acertos(resultados_auditoria):
    _limpar()
    if not resultados_auditoria:
        return None

    fig, ax = plt.subplots(figsize=(10, 4))

    acertos = [r["quantidade"] for r in resultados_auditoria]
    labels = [f"Jogo #{i+1}" for i in range(len(acertos))]

    cores = ["#2ecc71" if a >= 11 else "#e74c3c" for a in acertos]
    ax.bar(range(len(acertos)), acertos, color=cores, edgecolor="white", linewidth=0.5)

    ax.axhline(y=11, color="#f1c40f", linestyle="--", linewidth=1, label="Min. premiacao (11)")
    ax.axhline(y=15, color="#9b59b6", linestyle="--", linewidth=1, label="Maximo (15)")

    for i, v in enumerate(acertos):
        ax.annotate(str(v), (i, v), ha="center", va="bottom" if v >= 0 else "top", fontsize=9, fontweight="bold")

    ax.set_xlabel("Jogos", fontsize=11)
    ax.set_ylabel("Acertos", fontsize=11)
    ax.set_title("Evolucao de Acertos", fontsize=14, fontweight="bold")
    ax.set_xticks(range(len(acertos)))
    ax.set_xticklabels(labels, fontsize=7, rotation=45)
    ax.legend(fontsize=9)
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")
    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("#333")
    ax.spines["left"].set_color("#333")

    path = os.path.join(CHART_DIR, "evolucao_acertos.png")
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close(fig)
    return path
