## 📊 Dashboard de Análise e Simulação de Ações com Streamlit

Bem-vindo(a) ao **Dashboard Financeiro**, um projeto interativo desenvolvido em Python com a biblioteca **Streamlit**. Este painel visa fornecer ferramentas de análise e visualização para investidores e entusiastas do mercado de ações, focando em análise de séries temporais de ativos individuais e simulação de carteiras com ações do Ibovespa.

### ✨ Funcionalidades

O dashboard é organizado em **3 abas principais** para facilitar a navegação e o uso das ferramentas:

#### **1. 📈 Análise de Série Temporal Individual**

Esta aba é dedicada à inspeção detalhada de uma única ação (ticker). Você pode:
* **Visualizar Séries Temporais:** Plotagem do histórico de preços do ativo selecionado.
* **Estatísticas Descritivas:** Informações rápidas sobre a distribuição dos dados de retorno e preço (média, desvio padrão, mínimo, máximo, etc.).
* **Médias Móveis:** Adicione médias móveis (simples ou exponencial) ao gráfico para identificar tendências e pontos de suporte/resistência.

#### **2. 💰 Simulação de Carteira (Ibovespa)**

Nesta seção, você pode montar e analisar uma carteira de investimentos composta por ações do Ibovespa. Os recursos incluem:
* **Seleção de Ativos:** Escolha múltiplas ações para compor sua carteira.
* **Plotagem Conjunta:** Visualize a evolução das séries temporais de todas as ações selecionadas no mesmo gráfico para comparação.
* **Retorno Buy & Hold:** Calcule e visualize o retorno acumulado se você tivesse comprado e mantido (Buy & Hold) os ativos durante o período de análise.

#### **3. 💡 Guia Rápido**

Um manual de bolso dentro do próprio dashboard! Esta aba contém um **guia rápido e texto explicativo** sobre:
* Como interpretar os gráficos de séries temporais.
* O significado e a utilidade das estatísticas descritivas (por exemplo, o que o desvio padrão representa).
* Como as médias móveis podem ser usadas na análise técnica.
* A leitura dos resultados da simulação de carteira e o retorno Buy & Hold.

### 🛠️ Tecnologias Utilizadas

| Tecnologia | Função Principal |
| :--- | :--- |
| **Python** | Linguagem de programação principal. |
| **Streamlit** | Framework para criação rápida e elegante do dashboard. |
| **Pandas** | Manipulação e análise de dados. |
| **yfinance / Outras Bibliotecas de Dados** | Obtenção dos dados históricos de ações. |
| **Plotly / Matplotlib (ou similar)** | Visualização e plotagem interativa dos gráficos. |

### 🚀 Como Rodar o Projeto Localmente

1.  **Clone este repositório:**
    ```bash
    git clone [LINK_DO_SEU_REPOSITORIO]
    cd [NOME_DO_DIRETORIO]
    ```
2.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    # Exemplo com venv:
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    .\venv\Scripts\activate   # No Windows
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *Certifique-se de ter um arquivo `requirements.txt` com todas as bibliotecas usadas (streamlit, pandas, yfinance, etc.).*
4.  **Execute o dashboard:**
    ```bash
    streamlit run [NOME_DO_SEU_ARQUIVO_PRINCIPAL].py
    ```
    O painel será aberto automaticamente no seu navegador padrão.

---

### 🖼️ Prévia do Dashboard

*Adicione aqui uma imagem de alta qualidade do seu dashboard em funcionamento.*