# src/views/charts.py

import plotly.graph_objects as go
import pandas as pd

def render_stock_chart(df: pd.DataFrame, ticker: str):
    """
    Gera um gráfico interativo de Candlestick usando Plotly.
    """
    # Filtra as últimas 60 linhas para o gráfico não ficar poluído na tela
    df_plot = df.tail(60)
    
    fig = go.Figure()

    # 1. Desenha os Candles (Velas)
    fig.add_trace(go.Candlestick(
        x=df_plot.index,
        open=df_plot['Open'],
        high=df_plot['High'],
        low=df_plot['Low'],
        close=df_plot['Close'],
        name="Preço"
    ))

    # 2. Injeta as Médias Móveis se existirem no DataFrame
    if 'ema_9' in df_plot.columns:
        fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['ema_9'], name='EMA 9', line=dict(color='cyan', width=1.5)))
    if 'ema_21' in df_plot.columns:
        fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['ema_21'], name='EMA 21', line=dict(color='magenta', width=1.5)))
    if 'sma_200' in df_plot.columns:
        fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['sma_200'], name='SMA 200', line=dict(color='white', width=2)))

    # Customização do Layout para combinar com o Tema Dark
    fig.update_layout(
        title=f"Histórico Recente de Preços - {ticker}",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=400
    )
    
    return fig