# app.py

import streamlit as st
from src.controllers.analyzer_controller import AnalyzerController
from src.views.charts import render_stock_chart

# Configuração da página Web do Streamlit
st.set_page_config(page_title="B3 Predictive Bot", page_icon="📈", layout="wide")

# Inicializa o controlador central na memória da aplicação
if "controller" not in st.session_state:
    st.session_state.controller = AnalyzerController()

st.title("📈 B3 Predictive Bot — Inteligência Artificial")
st.markdown("Analise qualquer ativo da B3 sob as óticas de Day Trade, Swing Trade e Holding em tempo real.")

# Barra de pesquisa do ativo
ticker_input = st.text_input("Digite o Ticker do Ativo (ex: PETR4, VALE3, WEGE3):", value="PETR4").upper().strip()

if st.button("Executar Análise Preditiva", type="primary"):
    if ticker_input:
        with st.spinner(f"Processando {ticker_input}... Baixando histórico e treinando modelos de IA..."):
            
            # Executa a esteira completa através do controlador
            res = st.session_state.controller.run_full_analysis(ticker_input)
            
            # --- SEÇÃO DE ALERTAS DE SEGURANÇA ---
            if res["liquidity_alert"]:
                st.warning(f"⚠️ **Alerta de Liquidez**: O ativo {ticker_input} possui volume financeiro médio diário abaixo de R$ 1 Milhão. Os sinais técnicos podem sofrer distorções.")
            if res["fundamental_alert"]:
                st.error(f"❌ **Risco Fundamentalista**: {ticker_input} registrou prejuízo líquido recente. A nota de Holding sofreu um downgrade automático de risco.")

            # --- SEÇÃO 1: CARDS DE SCORE DA IA ---
            st.subheader("Veredito de Atratividade de Compra")
            col1, col2, col3 = st.columns(3)

            horizontes = [
                ("Day Trade (5 Minutos)", res["day_trade"], col1),
                ("Swing Trade (Diário)", res["swing_trade"], col2),
                ("Holding (Longo Prazo)", res["holding"], col3)
            ]

            for nome, operacao, coluna in horizontes:
                with coluna:
                    prob = operacao["prob"]
                    status = operacao["status"]
                    
                    # Define a cor do card com base na probabilidade
                    if prob >= 80: color, emoji = "#1E4620", "🟢 Compra Forte"
                    elif prob >= 60: color, emoji = "#2E5A1C", "🟡 Compra Moderada"
                    elif prob >= 40: color, emoji = "#4A4A4A", "⚪ Aguardar / Neutro"
                    else: color, emoji = "#5C1E1E", "🔴 Evitar / Venda"
                    
                    # Renderiza o Card customizado em HTML/CSS para ter personalidade
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center; border: 1px solid rgba(255,255,255,0.1)">
                            <h4 style="margin:0; color:white;">{nome}</h4>
                            <h1 style="margin:10px 0; color:white;">{prob:.1f}%</h1>
                            <p style="margin:0; font-weight:bold; color:white;">{emoji} ({status})</p>
                        </div>
                    """, unsafe_allow_html=True)

            # --- SEÇÃO 2: GRÁFICOS INTERATIVOS ---
            st.write("")
            st.subheader("Análise Gráfica")
            
            # Re-baixa o diário rapidamente apenas para plotar o gráfico interativo
            df_chart = st.session_state.controller.loader.get_ticker_history(ticker_input, interval="1d", period="6mo")
            if not df_chart.empty:
                df_chart = st.session_state.controller.calculator.apply_technical_indicators(df_chart)
                fig = render_stock_chart(df_chart, ticker_input)
                st.plotly_chart(fig, use_container_width=True)
                
            # --- SEÇÃO 3: TABELA DE FUNDAMENTOS ---
            st.subheader("Métricas de Saúde Financeira")
            m = res["holding"]["metrics"]
            
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            col_f1.metric("Preço / Lucro (P/L)", f"{m['p_l']:.2f}" if m['p_l'] else "N/A")
            col_f2.metric("Preço / Val. Patr. (P/VP)", f"{m['p_vp']:.2f}" if m['p_vp'] else "N/A")
            col_f3.metric("Dividend Yield (DY)", f"{m['dividend_yield']*100:.2f}%" if m['dividend_yield'] else "0.00%")
            col_f4.metric("Retorno s/ Patrimônio (ROE)", f"{m['roe']*100:.2f}%" if m['roe'] else "N/A")

    else:
        st.error("Por favor, insira um ticker válido.")