from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseEngine(ABC):
    """
    Abstract base class for all Totality Engines.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """
        Analyze the input data and return a structured dictionary of results.
        
        Args:
            input_data: The input to analyze (e.g., file path, text, object).
            
        Returns:
            Dict[str, Any]: The analysis results.
        """
        pass

    def validate(self, input_data: Any) -> bool:
        """
        Validate the input data before analysis.
        
        Args:
            input_data: The input to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        # Default implementation assumes valid if not overridden
        return True
