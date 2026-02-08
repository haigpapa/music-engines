import yaml
import os
from typing import Dict, Any

class ConfigLoader:
    """
    Loads configuration for the engines.
    """
    
    DEFAULT_CONFIG = {
        "audioscape": {
            "streaming": {"target_lufs": -14, "tolerance": 2, "true_peak_max": -1.0},
            "club": {"target_lufs": -9, "tolerance": 2, "true_peak_max": -1.0},
            "lra": {"min": 3, "max": 15}
        }
    }

    def __init__(self, config_path: str = "engines_config.yaml"):
        self.config_path = config_path
        self._config = self.DEFAULT_CONFIG.copy()

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration from file, falling back to defaults.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        # Deep merge could be better, but simple update for now
                        self._config.update(user_config)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
        
        return self._config

    def get_engine_config(self, engine_name: str) -> Dict[str, Any]:
        return self._config.get(engine_name, {})
