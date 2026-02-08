import numpy as np
import pandas as pd

class LiftAnalyzer:
    def __init__(self):
        pass
        
    def calculate_lift(self, actual_series: pd.Series, control_markets: pd.DataFrame) -> float:
        """
        Compares actual performance vs synthetic control.
        Uses a simple weighted average of control markets as the counterfactual.
        """
        if actual_series.empty or control_markets.empty:
            return 0.0
            
        # Simplified Synthetic Control: Average of control markets
        synthetic_baseline = control_markets.mean(axis=1)
        
        # Calculate Lift (Difference)
        lift = actual_series - synthetic_baseline
        total_lift_percentage = (lift.sum() / synthetic_baseline.sum()) * 100
        
        return float(total_lift_percentage)
