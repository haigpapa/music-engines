from .systems.creative.audio_analyzer import AudioAnalyzer
from .systems.creative.harmonic import HarmonicAnalyzer
from .systems.creative.nlp_engine import NLPEngine
from .systems.creative.explicitness import ExplicitnessDetector
from .systems.creative.code_switching import CodeSwitchingDetector
from totality_engine.engines.creative.deep_listening import DeepListeningEngine
from totality_engine.engines.creative.resonance import ResonanceEngine

from .systems.industry.graph_model import IndustryGraph
from .systems.industry.centrality import NetworkAnalyst

from .systems.platform.virality import ViralityEngine
from .systems.platform.optimization import PlatformOptimizer

from .systems.market.risk_map import MarketRiskEngine
from .systems.market.economics import EconomicsEngine

from .systems.culture.distance import CulturalDistanceEngine
from .systems.culture.identity import IdentityEngine

from .systems.audience.neuro import NeuroAesthetics
from .systems.audience.growth import GrowthAIEngine
from .systems.audience.lift import LiftAnalyzer

class HitSciencePipeline:
    def __init__(self):
        print("Initializing Hit Science Pipeline...")
        # System I
        self.audio_analyzer = AudioAnalyzer()
        self.harmonic_analyzer = HarmonicAnalyzer()
        self.nlp_engine = NLPEngine()
        self.explicitness_detector = ExplicitnessDetector()
        self.code_switcher = CodeSwitchingDetector()
        
        # System I - Deep Learning Enhancement
        self.deep_listening = DeepListeningEngine()
        
        # System I - Resonance (Cross-Modal)
        self.resonance_engine = ResonanceEngine()
        
        # System II
        self.industry_graph = IndustryGraph()
        self.network_analyst = NetworkAnalyst()
        
        # System III
        self.virality_engine = ViralityEngine()
        self.platform_optimizer = PlatformOptimizer()
        
        # System IV
        self.market_risk = MarketRiskEngine()
        self.economics = EconomicsEngine()
        
        # System V
        self.culture_distance = CulturalDistanceEngine()
        self.identity_engine = IdentityEngine()
        
        # System VI
        self.neuro_aesthetics = NeuroAesthetics()
        self.growth_engine = GrowthAIEngine()
        self.lift_analyzer = LiftAnalyzer()

    def analyze_track(self, audio_path: str, metadata: dict):
        """
        Main entry point for analyzing a track.
        metadata: {
            "lyrics": str, 
            "artist_id": str, 
            "artist_brand_keywords": list,
            "target_markets": list,
            "platform": str
        }
        """
        print(f"Analyzing track: {audio_path}")
        results = {}
        
        # --- System I: Creative ---
        print("Running System I Analysis...")
        results["creative"] = {}
        # Deep Listening (AI)
        results["creative"].update(self.deep_listening.analyze(audio_path))
        # Basic Signal Processing
        results["creative"].update(self.audio_analyzer.analyze(audio_path))
        results["creative"].update(self.harmonic_analyzer.analyze_harmony(audio_path))
        
        # --- System I: Resonance (Cross-Modal) ---
        print("Running Cross-Modal Resonance...")
        lyrics = metadata.get("lyrics", "")
        # Pass the creative results as 'audio_features' to access embeddings
        resonance_results = self.resonance_engine.analyze(lyrics, results["creative"])
        results["resonance"] = resonance_results
        
        if "lyrics" in metadata:
            results["creative"].update(self.nlp_engine.analyze_lyrics(metadata["lyrics"]))
            results["creative"].update(self.explicitness_detector.check_explicitness(metadata["lyrics"]))
            results["creative"].update(self.code_switcher.detect_languages(metadata["lyrics"]))
            
        # --- System II: Industry ---
        print("Running System II Analysis...")
        # (Assuming graph is populated or we look up existing nodes)
        if "artist_id" in metadata:
            centrality = self.network_analyst.get_artist_centrality(metadata["artist_id"])
            results["industry"] = {"artist_centrality": centrality}
            
        # --- System III: Platform ---
        print("Running System III Analysis...")
        # Mocking time series for prototype call
        import pandas as pd
        mock_tiktok = pd.Series([100, 500, 2000, 10000])
        mock_spotify = pd.Series([50, 100, 300, 1200])
        elasticity = self.virality_engine.calculate_elasticity(mock_tiktok, mock_spotify)
        results["platform"] = {"viral_elasticity": elasticity}
        
        optimizations = self.platform_optimizer.get_optimizations(results["creative"], metadata.get("platform", "Spotify"))
        results["platform"]["optimizations"] = optimizations
        
        # --- System IV: Market ---
        print("Running System IV Analysis...")
        if "target_markets" in metadata:
            risks = self.market_risk.assess_risk(metadata["target_markets"], results["creative"])
            results["market"] = {"geopolitical_risks": risks}
            
        # --- System V: Culture ---
        print("Running System V Analysis...")
        # Mocking track features as vector for distance
        track_vector = [0.5, 0.5, 0.5] # Placeholder
        if "target_markets" in metadata:
            dist_results = {}
            for mkt in metadata["target_markets"]:
                d = self.culture_distance.calculate_distance(track_vector, mkt)
                dist_results[mkt] = {"score": d, "interpretation": self.culture_distance.interpret_distance(d)}
            results["culture"] = {"distances": dist_results}
            
        if "artist_brand_keywords" in metadata:
            dissonance = self.identity_engine.check_brand_dissonance(
                metadata["artist_brand_keywords"], 
                results["creative"].get("sentiment", "Neutral"),
                results["creative"].get("explicitness_score", 0.0)
            )
            results["culture"]["brand_dissonance"] = dissonance

        # --- System VI: Audience ---
        print("Running System VI Analysis...")
        results["audience"] = self.neuro_aesthetics.analyze_hook_efficacy(audio_path)
        
        return results
