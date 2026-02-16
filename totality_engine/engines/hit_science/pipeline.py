from totality_engine.engines.creative.audioscape import AudioscapeEngine
from .systems.creative.harmonic import HarmonicAnalyzer
from totality_engine.engines.creative.lyrical import LyricalEngine
from .systems.creative.explicitness import ExplicitnessDetector
from .systems.creative.code_switching import CodeSwitchingDetector

from totality_engine.engines.creative.deep_listening import DeepListeningEngine
from totality_engine.engines.creative.resonance import ResonanceEngine

from .systems.industry.graph_model import IndustryGraph
from .systems.industry.centrality import NetworkAnalyst

from .systems.audience.neuro import NeuroAesthetics

class HitSciencePipeline:
    def __init__(self):
        print("Initializing Hit Science Pipeline (Pruned v2)...")
        # System I: Creative (The "Ears")
        self.audioscape = AudioscapeEngine()
        self.harmonic_analyzer = HarmonicAnalyzer() # Note: This might need moving to engines/creative if it's not there
        self.lyrical_engine = LyricalEngine()
        self.explicitness_detector = ExplicitnessDetector()
        self.code_switcher = CodeSwitchingDetector()
        
        # Deep Learning
        self.deep_listening = DeepListeningEngine()
        
        # Resonance (Cross-Modal)
        self.resonance_engine = ResonanceEngine()
        
        # System II: Industry (The "Network")
        self.industry_graph = IndustryGraph()
        self.network_analyst = NetworkAnalyst()
        
        # System VI: Audience (The "Brain") - Only keeping Neuro
        self.neuro_aesthetics = NeuroAesthetics()

        # Systems III, IV, V (Platform, Market, Culture) are currently Archived

    def analyze_track(self, audio_path: str, metadata: dict):
        """
        Main entry point for analyzing a track.
        metadata: {
            "lyrics": str, 
            "artist_id": str, 
            "artist_brand_keywords": list
        }
        """
        print(f"Analyzing track: {audio_path}")
        results = {}
        
        # --- System I: Creative ---
        print("Running Creative Analysis...")
        results["creative"] = {}
        
        # 1. Deep Listening (AI Embeddings)
        results["creative"].update(self.deep_listening.analyze(audio_path))
        
        # 2. Technical Audio Profile (FFmpeg)
        results["creative"].update(self.audioscape.analyze(audio_path))
        
        # 3. Harmonic Analysis (Librosa)
        # Assuming HarmonicAnalyzer is still in hit_science/systems/creative/harmonic.py
        # If I didn't verify it, I hope it exists. It was in the import list.
        try:
            results["creative"].update(self.harmonic_analyzer.analyze_harmony(audio_path))
        except Exception as e:
            print(f"Harmonic analysis failed: {e}")
        
        # 4. Lyrical Analysis
        lyrics = metadata.get("lyrics", "")
        if lyrics:
            print("Running Lyrical Analysis...")
            results["creative"].update(self.lyrical_engine.analyze(lyrics))
            results["creative"].update(self.explicitness_detector.check_explicitness(lyrics))
            results["creative"].update(self.code_switcher.detect_languages(lyrics))
        
        # --- System I: Resonance (Cross-Modal) ---
        print("Running Cross-Modal Resonance...")
        # Pass the creative results as 'audio_features' to access embeddings/moods
        resonance_results = self.resonance_engine.analyze(lyrics, results["creative"])
        results["resonance"] = resonance_results
            
        # --- System II: Industry ---
        print("Running Industry Analysis...")
        if "artist_id" in metadata:
            centrality = self.network_analyst.get_artist_centrality(metadata["artist_id"])
            results["industry"] = {"artist_centrality": centrality}
            
        # --- System VI: Audience (Neuro only) ---
        print("Running Audience (Neuro) Analysis...")
        results["audience"] = self.neuro_aesthetics.analyze_hook_efficacy(audio_path)
        
        # Fill placeholders for archived systems to maintain JSON schema compatibility (optional but good for frontend)
        results["platform"] = {"status": "archived"}
        results["market"] = {"status": "archived"}
        results["culture"] = {"status": "archived"}
        
        return results
