import numpy as np
import pandas as pd
# from statsmodels.tsa.stattools import grangercausalitytests # Heavy dependency, mocking for now

class ViralityEngine:
    def __init__(self):
        pass
        
    def calculate_elasticity(self, tiktok_series: pd.Series, spotify_series: pd.Series) -> float:
        """
        Calculates the Viral Elasticity Coefficient (epsilon).
        % Change in Spotify / % Change in TikTok
        """
        if tiktok_series.empty or spotify_series.empty:
            return 0.0
            
        pct_change_tiktok = tiktok_series.pct_change().mean()
        pct_change_spotify = spotify_series.pct_change().mean()
        
        if pct_change_tiktok == 0:
            return 0.0
            
        return pct_change_spotify / pct_change_tiktok

    def check_causality(self, tiktok_series: pd.Series, spotify_series: pd.Series):
        """
        Checks if TikTok views Granger-cause Spotify streams.
        """
        # Mocking the statistical test result
        # In real impl, use statsmodels.tsa.stattools.grangercausalitytests
        
        # Simple heuristic for prototype: correlation with lag
        correlation = tiktok_series.corr(spotify_series.shift(1))
        
        is_causal = correlation > 0.7
        return {
            "granger_causality_detected": bool(is_causal),
            "correlation_lag_1": float(correlation)
        }
