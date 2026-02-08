import re
import os
from typing import Dict, Any, List, Tuple
from totality_engine.core.engine import BaseEngine

class LyricalEngine(BaseEngine):
    """
    Engine for text-based analysis of lyrics.
    """
    
    CONCRETE_NOUNS = {
        "water", "blood", "light", "neon", "skin", "bone", "glass", "metal", "stone", 
        "fire", "rain", "car", "street", "ocean", "tide", "floor", "door", "window",
        "knife", "gun", "breath", "smoke", "ash", "dust", "gold", "silver", "chrome",
        "wire", "body", "face", "eye", "hand", "lip", "mouth", "tooth", "teeth",
        "sun", "moon", "star", "sky", "cloud", "storm", "wave", "shore", "sand",
        "ice", "snow", "wind", "shadow", "mirror", "screen", "pixel", "static",
        "saltwater", "flash", "pulse", "abyss", "undertow", "pressure", "void"
    }

    ABSTRACT_CONCEPTS = {
        "love", "hate", "soul", "mind", "dream", "hope", "fear", "faith", "truth",
        "lie", "time", "memory", "thought", "feeling", "heart", "spirit", "life",
        "death", "eternity", "forever", "nothing", "everything", "reason", "doubt",
        "pain", "joy", "sorrow", "regret", "threat", "permission", "warning"
    }

    SENTIMENT_KEYWORDS = {
        "dark": {"black", "dark", "night", "shadow", "void", "abyss", "grave", "death", "kill", "blood"},
        "euphoric": {"light", "sun", "sky", "high", "fly", "dream", "star", "gold", "shine", "alive"},
        "aggressive": {"fight", "burn", "fire", "break", "cut", "scream", "hate", "enemy", "war"},
        "melancholic": {"cry", "tear", "rain", "blue", "cold", "alone", "miss", "lost", "gone"}
    }
    
    def validate(self, input_data: Any) -> bool:
        return isinstance(input_data, str)

    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Analyzes lyrics text or file path.
        """
        text = input_data
        # If input looks like a file path and exists, read it
        if len(text) < 1024 and os.path.exists(text):
            try:
                with open(text, 'r', encoding='utf-8') as f:
                    text = f.read()
            except:
                pass # Treat as raw text

        return self._analyze_text(text)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'[^\w\s]', '', text)
        return text.lower()

    def _analyze_text(self, text: str) -> Dict[str, Any]:
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        total_lines = len(lines)
        if total_lines == 0:
            return {"error": "Empty text"}

        words = self._clean_text(text).split()
        total_words = len(words)
        
        # 1. Visual Density
        concrete_count = sum(1 for w in words if w in self.CONCRETE_NOUNS)
        abstract_count = sum(1 for w in words if w in self.ABSTRACT_CONCEPTS)
        
        visual_score = 0
        if total_words > 0:
            visual_score = (concrete_count / total_words) * 100

        # 2. Rhyme Density
        rhymes = self._count_rhymes(lines)
        rhyme_density = (rhymes / total_lines) * 10 if total_lines > 0 else 0

        # 3. Sentiment Tagging
        detected_moods = self._detect_moods(words)
        top_moods = [m[0] for m in detected_moods[:2]]

        return {
            "visual_density_score": round(visual_score, 2),
            "concrete_noun_count": concrete_count,
            "abstract_concept_count": abstract_count,
            "rhyme_density_score": round(rhyme_density, 2),
            "dominant_moods": top_moods,
            "stats": {
                "lines": total_lines,
                "words": total_words
            },
            "verdict": self._get_verdict(visual_score)
        }

    def _count_rhymes(self, lines: List[str]) -> int:
        rhymes = 0
        last_words = []
        for line in lines:
            cleaned = self._clean_text(line)
            if cleaned:
                last_words.append(cleaned.split()[-1])
                
        for i in range(len(last_words) - 1):
            w1 = last_words[i]
            w2 = last_words[i+1]
            if len(w1) > 2 and len(w2) > 2:
                if w1[-3:] == w2[-3:]: 
                    rhymes += 1
                elif w1[-2:] == w2[-2:] and len(w1)<4: 
                    rhymes += 1
        return rhymes

    def _detect_moods(self, words: List[str]) -> List[Tuple[str, int]]:
        detected_moods = []
        for mood, keywords in self.SENTIMENT_KEYWORDS.items():
            count = sum(1 for w in words if w in keywords)
            if count > 0:
                detected_moods.append((mood, count))
        
        detected_moods.sort(key=lambda x: x[1], reverse=True)
        return detected_moods

    def _get_verdict(self, visual_score: float) -> str:
        if visual_score > 5.0:
            return "[PASS] High Visual Potential for Video Generation."
        return "[WARN] Low Visual Density. AI prompts may need manual enrichment."
