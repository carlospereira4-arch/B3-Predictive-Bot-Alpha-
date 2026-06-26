# src/models/indicators.py

import pandas as pd
import numpy as np
import pandas_ta as ta

class IndicatorCalculator:
    """
    Classe responsável por transformar dados brutos de preço em 
    indicadores técnicos, estatísticos e padrões de price action.
    """
    
    def __init__(self):
        pass
        
    def apply_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Injeta Médias Móveis, IFR/RSI, MACD e Bandas de Bollinger.
        """
        df = df.copy()
        
        # 1. Médias Móveis (Exponenciais e Simples)
        df['ema_9'] = ta.ema(df['Close'], length=9)
        df['ema_21'] = ta.ema(df['Close'], length=21)
        df['sma_200'] = ta.sma(df['Close'], length=200)
        
        # Distância percentual entre as médias (Feature crucial para o ML)
        df['feat_mme_dist'] = ((df['ema_9'] - df['ema_21']) / df['ema_21']) * 100
        
        # 2. Índice de Força Relativa (IFR / RSI)
        df['feat_rsi_14'] = ta.rsi(df['Close'], length=14)
        
        # 3. Bandas de Bollinger (Retorna as bandas superior, média e inferior)
        bbands = ta.bbands(df['Close'], length=20, std=2)
        if bbands is not None:
            df['bb_upper'] = bbands.iloc[:, 2]
            df['bb_lower'] = bbands.iloc[:, 0]
            # Mapeia quão perto o preço está das bandas (0 = banda inferior, 1 = banda superior)
            df['feat_bb_position'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
            
        # 4. Volume Financeiro Relativo
        df['volume_sma20'] = ta.sma(df['Volume'], length=20)
        df['feat_vol_ratio'] = df['Volume'] / df['volume_sma20']
        
        return df

    def apply_quantitative_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Injeta métricas de volatilidade e desvio padrão (Z-Score).
        """
        df = df.copy()
        
        # Média e desvio padrão móvel para o Z-Score
        sma_20 = ta.sma(df['Close'], length=20)
        std_20 = df['Close'].rolling(window=20).std()
        
        # Z-Score: Mede quantos desvios padrões o preço atual está longe da média
        df['feat_zscore_20'] = (df['Close'] - sma_20) / std_20
        
        # Volatilidade Histórica (anualizada com base em 252 dias úteis)
        log_ret = np.log(df['Close'] / df['Close'].shift(1))
        df['feat_volatility'] = log_ret.rolling(window=20).std() * np.sqrt(252) * 100
        
        return df

    def detect_candlestick_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta padrões clássicos de Price Action (Martelo e Engolfo).
        Retorna 1 para alta, -1 para baixa e 0 para neutro.
        """
        df = df.copy()
        
        # Inicializa as colunas de padrões
        df['feat_pattern_bull'] = 0
        
        # Loop seguro para ler os candles e identificar padrões básicos de Price Action
        for i in range(2, len(df)):
            open_curr, close_curr = df['Open'].iloc[i], df['Close'].iloc[i]
            high_curr, low_curr = df['High'].iloc[i], df['Drop'].iloc[i] if 'Drop' in df.columns else df['Low'].iloc[i]
            
            open_prev, close_prev = df['Open'].iloc[i-1], df['Close'].iloc[i-1]
            
            body = abs(close_curr - open_curr)
            total_range = high_curr - low_curr
            
            if total_range == 0: continue
            
            # 1. Identificação de Martelo (Sombra inferior longa, corpo pequeno no topo)
            lower_shadow = min(open_curr, close_curr) - low_curr
            upper_shadow = high_curr - max(open_curr, close_curr)
            
            if (lower_shadow > (2 * body)) and (upper_shadow < (0.5 * body)):
                df.iloc[i, df.columns.get_loc('feat_pattern_bull')] = 1
                
            # 2. Identificação de Engolfo de Alta
            if (close_prev < open_prev) and (close_curr > open_curr) and (open_curr <= close_prev) and (close_curr >= open_prev):
                df.iloc[i, df.columns.get_loc('feat_pattern_bull')] = 1
                
        return df
