# 📈 B3 Predictive Bot — Inteligência Artificial para Análise de Ativos

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=flat-square)

---

## 🎯 Sobre o Projeto

**B3 Predictive Bot** é uma aplicação inteligente de análise preditiva para ativos da Bolsa de Valores Brasileira (B3). Utiliza machine learning e análise técnica para fornecer recomendações de compra/venda em três horizontes de investimento diferentes.

> **Nota**: Este projeto está em fase **Alpha**. Use com responsabilidade e sempre consulte um profissional de investimentos antes de tomar decisões financeiras.

---

## ✨ Recursos Principais

### 🤖 Três Horizontes de Análise
- **Day Trade (5 min)** - Operações intradiárias de curta duração
- **Swing Trade (Diário)** - Operações de médio prazo (dias/semanas)
- **Holding (Longo Prazo)** - Investimento para períodos estendidos

### 📊 Análise Técnica Avançada
- Indicadores técnicos: SMA, EMA, RSI, MACD, Bollinger Bands
- Gráficos interativos com Plotly
- Análise de tendências e suportes/resistências

### 💰 Métricas Fundamentalistas
- P/L (Preço/Lucro)
- P/VP (Preço/Valor Patrimonial)
- Dividend Yield (DY)
- ROE (Retorno sobre o Patrimônio)

### ⚠️ Sistema de Alertas
- Alerta de liquidez para ativos com baixo volume
- Alerta de risco fundamentalista para empresas com prejuízo

### 🎨 Interface Intuitiva
- Dashboard web com Streamlit
- Cards coloridos com recomendações claras
- Busca rápida de qualquer ticker da B3

---

## 📋 Requisitos

- **Python 3.12+**
- **pip** (gerenciador de pacotes)
- Conexão com a internet (para download de dados)

---

## 🚀 Instalação

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/B3-Predictive-Bot.git
cd "B3 Predictive Bot (Alpha)"
```

### 2️⃣ Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

Principais dependências:
- `streamlit` - Framework web
- `yfinance` - Download de dados financeiros
- `pandas` - Manipulação de dados
- `scikit-learn` - Machine learning
- `plotly` - Gráficos interativos

---

## 💻 Como Usar

### Execução Local

```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac

# Inicie a aplicação
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

### Interface de Uso

1. **Digite o Ticker**: Ex: `PETR4`, `VALE3`, `WEGE3`
2. **Clique em "Executar Análise Preditiva"**
3. **Visualize os Resultados**:
   - Cards com scores de compra por horizonte
   - Gráficos técnicos interativos
   - Métricas fundamentalistas

---

## 📁 Estrutura do Projeto

```
B3 Predictive Bot (Alpha)/
├── app.py                          # Aplicação principal (Streamlit)
├── requirements.txt                # Dependências do projeto
├── README.md                       # Este arquivo
│
├── src/                            # Código-fonte
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── analyzer_controller.py  # Controlador central de análise
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── data_loader.py          # Download e carregamento de dados
│   │   ├── indicators.py           # Cálculo de indicadores técnicos
│   │   └── predictor.py            # Modelos de predição (ML)
│   │
│   └── views/
│       ├── __init__.py
│       ├── charts.py               # Renderização de gráficos
│       └── dashboard.py            # Componentes do dashboard
│
├── streamlit/
│   └── config.toml                 # Configurações do Streamlit
│
└── data/                           # Dados locais (opcional)
```

---

## 🛠️ Arquitetura

### Padrão MVC (Model-View-Controller)

```
Usuário Input
    ↓
[AnalyzerController] - Orquestra o fluxo
    ├→ [DataLoader] - Busca dados no yfinance
    ├→ [Indicators] - Calcula indicadores técnicos
    ├→ [Predictor] - Treina e executa modelos ML
    └→ [Charts] - Renderiza visualizações
        ↓
    Streamlit UI (app.py)
        ↓
    Usuário recebe análise
```

---

## 📊 Exemplos de Output

### Cards de Recomendação
- 🟢 **Compra Forte** (≥ 80%)
- 🟡 **Compra Moderada** (60-80%)
- ⚪ **Aguardar / Neutro** (40-60%)
- 🔴 **Evitar / Venda** (< 40%)

### Alertas
- ⚠️ Alerta de Liquidez: Volume médio < R$ 1M
- ❌ Risco Fundamentalista: Empresa com prejuízo recente

---

## 🔧 Configuração Avançada

### Modificar Período de Análise
Edite em [src/models/data_loader.py](src/models/data_loader.py):
```python
period = "6mo"  # Altere para "1y", "5y", etc.
```

### Ajustar Indicadores Técnicos
Edite em [src/models/indicators.py](src/models/indicators.py):
```python
sma_period = 20  # Período da Média Móvel Simples
```

### Customizar Streamlit
Edite [streamlit/config.toml](streamlit/config.toml) para mudar tema, cores, etc.

---

## 🧪 Testes

Para executar testes (quando implementados):
```bash
pytest tests/
```

---

## 📈 Roadmap

- [ ] Backtesting de estratégias
- [ ] Suporte a mais indicadores técnicos
- [ ] Análise de correlação entre ativos
- [ ] Sistema de alertas por email/SMS
- [ ] API REST para integração
- [ ] Suporte a cripto e mercado internacional
- [ ] Dashboard com histórico de análises

---

## ⚖️ Disclaimer Importante

⚠️ **Este projeto é fornecido "como está" para fins educacionais e de pesquisa.**

- Não é aconselhamento financeiro profissional
- Resultados passados não garantem resultados futuros
- Use por sua conta e risco
- Sempre consulte um profissional antes de investir

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Carlos Henrique**
- 🐙 [GitHub](https://github.com/carlospereira4-arch)
- 📧 Email: carlos.pereira4@estudante.ufla.br

---

## 🙏 Agradecimentos

- [yfinance](https://github.com/ranaroussi/yfinance) - Dados financeiros
- [Streamlit](https://streamlit.io/) - Framework web
- [Plotly](https://plotly.com/) - Gráficos interativos
- [scikit-learn](https://scikit-learn.org/) - Machine Learning

---

## 📞 Suporte

Encontrou um problema? Abra uma [Issue](https://github.com/scarlospereira4-arch/B3-Predictive-Bot/issues) no GitHub.

---

**⭐ Se este projeto foi útil, considere deixar uma estrela!**

