# src/controllers/analyzer_controller.py

import pandas as pd
from src.models.data_loader import DataLoader
from src.models.indicators import IndicatorCalculator
from src.models.predictor import MarketPredictor
from typing import Dict, Any

class AnalyzerController:
    """
    Classe Controladora que orquestra o fluxo de dados entre os Models
    e formata os resultados consolidados para a View (Interface).
    """
    
    def __init__(self):
        self.loader = DataLoader()
        self.calculator = IndicatorCalculator()
        self.predictor = MarketPredictor()

    def run_full_analysis(self, ticker: str) -> Dict[str, Any]:
        """
        Executa a esteira completa de análise para Day Trade, Swing Trade e Holding.
        """
        ticker = ticker.upper().strip()
        
        # 1. Busca Métricas Fundamentalistas e de Liquidez
        fundamental_metrics = self.loader.get_financial_metrics(ticker)
        
        results = {
            "ticker": ticker,
            "liquidity_alert": False,
            "fundamental_alert": False,
            "day_trade": {"prob": 0.0, "status": "Erro"},
            "swing_trade": {"prob": 0.0, "status": "Erro"},
            "holding": {"prob": 0.0, "status": "Erro", "metrics": fundamental_metrics}
        }
        
        # Alerta de Liquidez (Volume médio menor que R$ 1 Milhão)
        vol_medio = fundamental_metrics.get("volume_medio_20d")
        if vol_medio is not None and vol_medio < 1000000:
            results["liquidity_alert"] = True

        # Alerta Fundamentalista (Empresa com prejuízo ou dívida excessiva)
        lucro = fundamental_metrics.get("lucro_liquido")
        if lucro is not None and lucro <= 0:
            results["fundamental_alert"] = True

        # ==========================================
        # EXECUÇÃO DA IA PARA CADA HORIZONTE
        # ==========================================
        try:
            # --- PERSPECTIVA 1: DAY TRADE ---
            # dados de 5 minutos ('5m') dos últimos 30 dias ('30d')
            df_dt = self.loader.get_ticker_history(ticker, interval="5m", period="30d")
            if not df_dt.empty:
                df_dt_feats = self.calculator.apply_technical_indicators(df_dt)
                df_dt_feats = self.calculator.apply_quantitative_metrics(df_dt_feats)
                df_dt_feats = self.calculator.detect_candlestick_patterns(df_dt_feats)
                # Alvo Day Trade: Janela 12 candles (~1h) | Gain 1.2% | Loss 0.6%
                prob_dt = self.predictor.train_and_predict(df_dt_feats, horizon=12, gain_pct=1.2, loss_pct=0.6)
                results["day_trade"] = {"prob": prob_dt, "status": self._classify_score(prob_dt)}
        except Exception as e:
            results["day_trade"]["status"] = f"Indisponível: {str(e)}"

        try:
            # --- PERSPECTIVA 2: SWING TRADE ---
            # dados diários ('1d') dos últimos 2 anos ('2y')
            df_st = self.loader.get_ticker_history(ticker, interval="1d", period="2y")
            if not df_st.empty:
                df_st_feats = self.calculator.apply_technical_indicators(df_st)
                df_st_feats = self.calculator.apply_quantitative_metrics(df_st_feats)
                df_st_feats = self.calculator.detect_candlestick_patterns(df_st_feats)
                # Alvo Swing Trade: Janela 10 dias | Gain 4.2% | Loss 2.1%
                prob_st = self.predictor.train_and_predict(df_st_feats, horizon=10, gain_pct=4.2, loss_pct=2.1)
                results["swing_trade"] = {"prob": prob_st, "status": self._classify_score(prob_st)}
        except Exception as e:
            results["swing_trade"]["status"] = f"Indisponível: {str(e)}"

        try:
            # --- PERSPECTIVA 3: HOLDING TRADE ---
            # dados semanais ('1wk') de longo prazo ('5y')
            df_hd = self.loader.get_ticker_history(ticker, interval="1wk", period="5y")
            if not df_hd.empty:
                df_hd_feats = self.calculator.apply_technical_indicators(df_hd)
                df_hd_feats = self.calculator.apply_quantitative_metrics(df_hd_feats)
                df_hd_feats = self.calculator.detect_candlestick_patterns(df_hd_feats)
                # Alvo Holding Gráfico: Janela 24 semanas (~6 meses) | Gain 15% | Loss 7.5%
                prob_hd = self.predictor.train_and_predict(df_hd_feats, horizon=24, gain_pct=15.0, loss_pct=7.5)
                
                # Se houver alerta fundamentalista, aplica o Downgrade de 40% na nota gráfica que combinamos no PRD
                if results["fundamental_alert"]:
                    prob_hd = prob_hd * 0.60
                    
                results["holding"]["prob"] = prob_hd
                results["holding"]["status"] = self._classify_score(prob_hd)
        except Exception as e:
            results["holding"]["status"] = f"Indisponível: {str(e)}"

        return results

    def _classify_score(self, score: float) -> str:
        """Método auxiliar interno para classificar os scores percentuais."""
        if score >= 80: return "Muito Boa"
        if score >= 60: return "Boa"
        if score >= 40: return "Ruim"
        return "Muito Ruim"