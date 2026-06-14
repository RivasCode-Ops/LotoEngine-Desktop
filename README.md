# LotoEngine Desktop

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-31%2F31-brightgreen)](tests/)
[![PyInstaller](https://img.shields.io/badge/build-.exe-orange)](build.bat)

**LotoEngine Desktop** é uma ferramenta desktop de analise preditiva para a **Lotofacil**, que utiliza o **algoritmo 9/6** para gerar jogos estrategicos com base em sorteios anteriores, frequencia de numeros e ajustes de peso personalizaveis.

![Interface Principal do LotoEngine](screenshot.png)
*(Adicione aqui um print da sua interface para ilustrar)*

## Funcionalidades Principais

- **Entrada de Dados**: Insira o ultimo concurso manualmente ou importe de CSV/Excel.
- **Motor de Geracao 9/6**: Algoritmo que mantem 9 numeros do sorteio anterior e substitui 6 com base em criterios.
- **Painel de Pesos**: Ajuste a importancia de cada criterio de filtragem (salvo em `pesos_config.json`).
- **Auditoria Completa**: Compare o jogo gerado com o resultado oficial e veja o historico de acertos (11 a 15 pontos).
- **Graficos Avancados**:
  - Frequencia dos numeros
  - Grafico de atraso
  - Heatmap 5x5
  - Evolucao de acertos por auditoria
- **Banco de Dados Local (SQLite)**: Persiste concursos, jogos gerados e auditorias em 3 tabelas.
- **Executavel `.exe`**: Gere um arquivo unico com `build.bat` para rodar sem Python instalado.

## Tecnologias Utilizadas

- **Python 3.8+**
- **CustomTkinter** – Interface grafica moderna
- **Pandas & NumPy** – Analise de dados
- **Matplotlib** – Visualizacoes
- **SQLite3** – Banco de dados local
- **PyInstaller** – Criacao do executavel

## Como Executar

### 1. Clonar o repositorio
```bash
git clone https://github.com/RivasCode-Ops/LotoEngine-Desktop.git
cd LotoEngine-Desktop
```

### 2. Criar um ambiente virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicacao
```bash
python main.py
```

### 5. (Opcional) Gerar executavel `.exe`
```bash
build.bat
```
O arquivo `LotoEngine-Desktop.exe` sera gerado na pasta `dist/`.

## Guia Rapido de Uso

1. **Aba "Entrada"**: Informe os 15 numeros do ultimo concurso ou carregue um arquivo CSV/Excel.
2. **Aba "Geracao"**: Escolha a quantidade e clique em "Gerar Jogos".
3. **Aba "Pesos"**: Ajuste a importancia de Soma, Pares/Impares e Primos.
4. **Aba "Auditoria"**: Apos o sorteio oficial, informe o resultado e clique em "Auditar".
5. **Aba "Graficos"**: Visualize analises estatisticas dos sorteios.

## Estrutura do Projeto

```
LotoEngine-Desktop/
├── src/
│   ├── core/          # Motor 9/6, charts, validacoes
│   ├── gui/           # Janelas CustomTkinter (5 abas)
│   ├── database/      # SQLite, migrations e models
│   └── data/          # Loader de dados (CSV/Excel)
├── data/              # Banco SQLite, JSON de pesos
├── tests/             # 31 testes unitarios e de integracao
├── main.py            # Ponto de entrada
├── build.bat          # Script de build do .exe
└── requirements.txt   # Dependencias
```

## Contribuicao

Contribuicoes sao bem-vindas! Sinta-se a vontade para:
- Reportar bugs ou sugerir melhorias via [Issues](https://github.com/RivasCode-Ops/LotoEngine-Desktop/issues)
- Enviar Pull Requests com novas funcionalidades ou correcoes

## Licenca

Este projeto e distribuido sob a licenca **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## Status dos Testes

Todos os **31 testes** estao passando:
- Validacao de entrada (15 numeros unicos)
- Geracao 9/6 com filtros (soma, pares/impares, primos)
- Persistencia em SQLite
- Auditoria e calculo de acertos
- Criacao de graficos

---

**Desenvolvido por [RivasCode-Ops](https://github.com/RivasCode-Ops)** – Versao 1.0
