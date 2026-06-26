# src/models/predictor.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import Tuple, Dict, Any

class MarketPredictor:
    """
    Classe responsável pelo ciclo de vida do modelo de Machine Learning:
    Criação de targets, treinamento sob demanda e inferência de probabilidades.
    """
    
    def __init__(self):
        # Usamos o Random Forest por ser estável e excelente para dados tabulares financeiros
        self.model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        # Lista das variáveis que o modelo vai usar para tomar a decisão
        self.feature_cols = [
            'feat_mme_dist', 
            'feat_rsi_14', 
            'feat_bb_position', 
            'feat_vol_ratio', 
            'feat_zscore_20', 
            'feat_volatility', 
            'feat_pattern_bull'
        ]

    def prepare_dataset(self, df: pd.DataFrame, horizon: int, gain_pct: float, loss_pct: float) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Cria a lógica do Target (1 para Sucesso, 0 para Falha) baseado no gerenciamento de risco.
        """
        df = df.copy()
        
        # Remove linhas iniciais que possuem valores nulos por conta do cálculo das médias/IFR
        df = df.dropna(subset=self.feature_cols)
        
        targets = []
        indices_validos = []
        
        # Loop para olhar o futuro de cada candle e rotular se deu Gain ou Loss
        for i in range(len(df) - horizon):
            preco_entrada = df['Close'].iloc[i]
            alvo_gain = preco_entrada * (1 + (gain_pct / 100))
            alvo_loss = preco_entrada * (1 - (loss_pct / 100))
            
            sucesso = 0
            # Varre o horizonte futuro
            for j in range(1, horizon + 1):
                preco_futuro = df['Close'].iloc[i + j]
                
                if preco_futuro >= alvo_gain:
                    sucesso = 1
                    break
                if preco_futuro <= alvo_loss:
                    sucesso = 0
                    break
                    
            targets.append(sucesso)
            indices_validos.append(df.index[i])
            
        # Retorna as Features (X) e o Target (y) alinhados temporalmente
        X = df.loc[indices_validos, self.feature_cols]
        y = pd.Series(targets, index=indices_validos)
        
        return X, y

    def train_and_predict(self, df: pd.DataFrame, horizon: int, gain_pct: float, loss_pct: float) -> float:
        """
        Orquestra o treinamento do modelo com o histórico e faz a predição para o momento atual.
        """
        # 1. Prepara a matriz de dados
        X, y = self.prepare_dataset(df, horizon, gain_pct, loss_pct)
        
        if len(X) < 30:
            raise ValueError("Histórico de dados insuficiente para treinar a Inteligência Artificial.")
            
        # 2. Treina o modelo com o passado (On-the-fly training)
        self.model.fit(X, y)
        
        # 3. Captura o estado atual do mercado (o último candle fechado)
        df_limpo = df.dropna(subset=self.feature_cols)
        X_atual = df_limpo[self.feature_cols].tail(1)
        
        # 4. Calcula a probabilidade de acerto (Retorna a % para a classe 1 - Sucesso)
        probabilidade_sucesso = self.model.predict_proba(X_atual)[0][1]
        
        return float(probabilidade_sucesso * 100)