# src/models/data_loader.py

import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any

class DataLoader:
    """
    Classe responsável por abstrair a coleta de dados de mercado (B3)
    e dados fundamentalistas utilizando a API do Yahoo Finance.
    """
    
    def __init__(self):
        pass

    def get_ticker_history(self, ticker: str, interval: str = "1d", period: str = "2y") -> pd.DataFrame:
        """
        Coleta o histórico de preços (OHLCV) de um ativo da B3.
        
        Parâmetros:
            ticker (str): O código do ativo (ex: 'PETR4', 'VALE3').
            interval (str): O tempo gráfico (ex: '1m', '5m', '1d', '1wk').
            period (str): O horizonte de dados retroativos (ex: '30d', '2y', 'max').
            
        Retorna:
            pd.DataFrame: DataFrame contendo Open, High, Low, Close, Volume.
        """
        # Garante o sufixo '.SA' necessário para ativos brasileiros no Yahoo Finance
        if not ticker.endswith(".SA"):
            ticker_yf = f"{ticker.upper()}.SA"
        else:
            ticker_yf = ticker.upper()
            
        try:
            print(f"Baixando dados para {ticker_yf} (Intervalo: {interval}, Período: {period})...")
            ticker_obj = yf.Ticker(ticker_yf)
            df = ticker_obj.history(period=period, interval=interval)
            
            if df.empty:
                raise ValueError(f"Nenhum dado encontrado para o ticker {ticker}.")
                
            return df
            
        except Exception as e:
            print(f"Erro ao carregar dados históricos: {e}")
            return pd.DataFrame()

    def get_financial_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Coleta indicadores fundamentalistas essenciais para análise de Holding.
        
        Parâmetros:
            ticker (str): O código do ativo.
            
        Retorna:
            dict: Dicionário com métricas como P/L, P/VP, DY, Margens, etc.
        """
        if not ticker.endswith(".SA"):
            ticker_yf = f"{ticker.upper()}.SA"
        else:
            ticker_yf = ticker.upper()
            
        metrics = {
            "p_l": None,
            "p_vp": None,
            "dividend_yield": None,
            "roe": None,
            "lucro_liquido": None,
            "volume_medio_20d": None
        }
        
        try:
            ticker_obj = yf.Ticker(ticker_yf)
            info = ticker_obj.info
            
            # Mapeamento seguro dos dados fundamentalistas (evitando KeyError)
            metrics["p_l"] = info.get("trailingPE")
            metrics["p_vp"] = info.get("priceToBook")
            metrics["dividend_yield"] = info.get("dividendYield", 0.0)
            metrics["roe"] = info.get("returnOnEquity")
            metrics["lucro_liquido"] = info.get("netIncomeToCommon")
            metrics["volume_medio_20d"] = info.get("averageVolume10Days") # Proxy de liquidez
            
            return metrics
            
        except Exception as e:
            print(f"Erro ao carregar métricas fundamentalistas: {e}")
            return metrics
