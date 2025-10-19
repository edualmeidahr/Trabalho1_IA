# Comparador de Algoritmos de Busca em Labirintos
[![SO][Ubuntu-badge]][Ubuntu-url]
[![IDE][vscode-badge]][vscode-url]
[![Language][python-badge]][python-url]

Este repositório contém o código-fonte do **Trabalho 1 da disciplina de Inteligência Artificial**, ministrada pelo docente Tiago Alves de Oliveira, no CEFET-MG, campus V. O objetivo do projeto é implementar e comparar o desempenho de diferentes algoritmos de busca (DFS, BFS, Greedy e A*) na resolução de labirintos.

O script principal (`run_search.py`) é capaz de ler múltiplos labirintos de arquivos de texto, executar os quatro algoritmos em cada um e, ao final, gerar um relatório comparativo detalhado em `.txt` e gráficos comparativos em `.png`.

---


## 📥 Clone do Projeto

Para começar, clone este repositório para a sua máquina local usando o seguinte comando no seu terminal:

```bash
#usando HTTPS
git clone https://github.com/edualmeidahr/Trabalho1_IA.git

#usando SSH
git clone git@github.com:edualmeidahr/Trabalho1_IA.git
```
## 🚀 Requisitos

* **Python 3.10** (ou superior)
* **Matplotlib** (única dependência externa, usada para gerar os gráficos)




## ⚙️ Instalação das Dependências

Para facilitar, você pode usar os scripts de instalação fornecidos ou rodar o comando manualmente. Para isso, é preciso que esteja dentro da pasta do projeto.

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

Seus arquivos de labirinto devem estar dentro de uma pasta chamada `data/`. O script principal `run_search.py` foi programado para procurar automaticamente por qualquer arquivo que comece com `labirinto` (ex: `labirinto.txt`, `labirinto_grande.txt`, etc.) dentro dessa pasta.

``` Markdown
SEU_PROJETO/
├── data/
│   ├── labirinto1.txt
│   └── labirinto_grande.txt
│
├── src/
│   ├── maze.py
│   ├── search.py
│   └── heuristics.py
│
├── .gitignore
├── EC_IA_Trabalho_01_2025.pdf
├── install_deps.bat
├── install_deps.sh
├── README.md
├── requirements.txt
└── run_search.py


```

### Formato do labirinto

Os arquivos `.txt` devem seguir este formato: 

- `#`: Parede
- `.`: Caminho livre
- `S`: Ponto de partida (Start)
- `G`: Ponto de chegada (Goal)

## 🏃‍♂️ Executando o Projeto

Com as dependências instaladas e os labirintos na pasta `data/`, basta executar o script principal a partir da pasta raiz do projeto:

```Bash

# Em Linux/macOS
python3 run_search.py

# Em Windows
python run_search.py
# ou
py run_search.py

```

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



