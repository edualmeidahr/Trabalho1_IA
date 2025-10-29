# Problema das 8 Rainhas com Hill Climbing
[![SO][Ubuntu-badge]][Ubuntu-url]
[![IDE][vscode-badge]][vscode-url]
[![Language][python-badge]][python-url]

Este repositório contém o código-fonte do **Trabalho 2 da disciplina de Inteligência Artificial**, ministrada pelo docente Tiago Alves de Oliveira, no CEFET-MG, campus V. O objetivo do projeto é implementar e comparar o desempenho do algoritmo **Hill Climbing (Subida de Encosta)** na resolução do problema das 8 Rainhas.

O script principal (`run_search.py`) executa os algoritmos N vezes (padrão: 100) para comparar duas variações principais:
1.  **Hill Climbing com movimentos laterais** limitados.
2.  **Hill Climbing com reinícios aleatórios (Random-Restart)**.

Ao final da execução, ele gera relatórios detalhados (`.txt`) na pasta `Relatorios/` com as métricas de cada execução (tabuleiro inicial, final, tempo, passos, etc.) e imprime um sumário estatístico no console.

---

## 📥 Clone do Projeto

Para começar, clone este repositório para a sua máquina local usando o seguinte comando no seu terminal:

```bash
#usando HTTPS
git clone [https://github.com/edualmeidahr/Trabalho2_IA.git](https://github.com/edualmeidahr/Trabalho2_IA.git)

#usando SSH
git clone git@github.com:edualmeidahr/Trabalho2_IA.git
```

## 🚀 Requisitos

- **Python 3.10** (ou superior)
* **Matplotlib** (única dependência externa, usada para gerar os gráficos)




## ⚙️ Instalação das Dependências

Para facilitar, você pode usar os scripts de instalação fornecidos ou rodar o comando manualmente. Para isso, é preciso que esteja dentro da pasta do projeto (`Trabalho2`).

### Opção 1: Usando os Scripts de Instalação

#### 🐧 Em Linux / macOS

1.  Primeiro, dê permissão de execução ao script:
    ```bash
    chmod +x install_deps.sh
    ```
2.  Depois, execute o script:
    ```bash
    ./install_deps.sh
    ```

#### 🪟 Em Windows

1.  Apenas execute o script `install_deps.bat` clicando duas vezes nele.
2.  (Alternativa) Se preferir, execute-o pelo seu terminal (CMD ou PowerShell):
    ```bash
    .\install_deps.bat
    ```

### Opção 2: Instalação Manual (via Pip)

Se preferir, você pode instalar a biblioteca manualmente usando o `pip` (gerenciador de pacotes do Python):

```bash
pip install -r requirements.txt
```



## 📂 Detalhes do Projeto

### Estrutura de Pastas

O projeto segue a seguinte estrutura de diretórios: 


``` Markdown
Trabalho2_IA/
├── Relatorios/
│   ├── relatorio_lateral_moves.txt
│   └── relatorio_random_start.txt
│
├── src/
│   ├── eight_queens.py
│   └── hill_climbing.py
│
├── .gitignore
├── install_deps.bat
├── install_deps.sh
├── README.md
├── requirements.txt
└── run_search.py
```

### Representação do Problema

O estado do tabuleiro (tipo `Board`) é representado por um vetor (lista) de 8 posições, onde: 

- O **índice** `c` (0..7) representa a **coluna**.
- O **valor** `r` (0..7) na posição `Board[c]` representa a linha onde a rainha daquela coluna está. 

*Exemplo*: O vetor `[1, 5, 0 6, 3, 7, 2, 4]` significa que a rainha da coluna 0 eta'na linha 1, a rainha da coluna 1 está na linha 5, e assim por diante. 

*A função de avalição (custo)* do algoritmo é o número total de pares de rainhas em conflito (horizontal e diagonal). O objetivo é encontrar um estado com `custo 0`. 


## 🏃‍♂️ Executando o Projeto

Com o Python 3.10+ instalado, basta executar o script principal a partir da pasta raiz do projeto (`\Trabalho2`). O script `run_search.py` foi programado para rodar os dois experimentos e salvar os relatórios automaticamente.


``` BASH

# Em Linux/macOS
python3 run_search.py

# Em Windows
python run_search.py
# ou
py run_search.py
```

# Máquinas de Teste

Para testagem do projeto, foram utilizadas 2 máquinas que rodaram o cógido em sistema operacional Linux (Ubuntu).

| Máquina | Processador            | Memória RAM | Sistema Operacional |
|------------------|------------------------|-------------|---------------------|
| Intel inspiron 15 5000 |Intel(R) Core(TM) i7-11390H    | 16 GB       | Ubunto 22.04     |
| Lenovo ideaPad 3i    | AMD Ryzen 7 5700U       | 12 GB        | Ubuntu 22.04       |



## 📨 Autores

<div align="center">
<i>Eduardo Henrique Queiroz Almeida - Computer Engineering Student @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor1]
[![Linkedin][linkedin-badge]][linkedin-autor1]
[![Telegram][telegram-badge]][telegram-autor1]

<br><br>


<i>Joaquim Cézar Santana da Cruz - Computer Engineering Student @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor4]
[![Linkedin][linkedin-badge]][linkedin-autor4]
[![Telegram][telegram-badge]][telegram-autor4]


</div>

[linkedin-badge]: https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white
[telegram-badge]: https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[gmail-badge]: https://img.shields.io/badge/-Gmail-D14836?style=for-the-badge&logo=Gmail&logoColor=white

[linkedin-autor1]: https://www.linkedin.com/in/eduardo-henrique-queiroz-almeida-61378a124/
[telegram-autor1]: https://t.me
[gmail-autor1]: mailto:eduardohenriquecruzeiro123@gmail.com

[linkedin-autor4]: https://www.linkedin.com/in/joaquim-cruz-b760bb350/
[telegram-autor4]: https://t.me/
[gmail-autor4]: mailto:joaquimcezar930@gmail.com

[ubuntu-badge]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white
[Ubuntu-url]: https://ubuntu.com/
[vscode-badge]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[vscode-url]: https://code.visualstudio.com/docs/?dv=linux64_deb
[make-badge]: https://img.shields.io/badge/_-MAKEFILE-427819.svg?style=for-the-badge
[make-url]: https://www.gnu.org/software/make/manual/make.html
[python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
