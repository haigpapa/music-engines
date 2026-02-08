from datetime import date
from typing import List, Optional
from pydantic import BaseModel

# Mocking the legacy TotalitySong models referenced in main.py

class AcousticFeatures(BaseModel):
    bpm: float
    key: str
    lufs: float
    duration_ms: int
    danceability: float
    energy: float

class LyricalContent(BaseModel):
    themes: List[str]
    sentiment_valence: float

class CulturalContext(BaseModel):
    origin_city: str
    origin_country: str
    language: str

class NeuroResponse(BaseModel):
    predicted_emotions: List[str]
    stimulation_score: float

class EconomicStats(BaseModel):
    label_type: str

class SocialContext(BaseModel):
    identity_markers: List[str]

class HistoricalContext(BaseModel):
    era: str

class TotalitySong(BaseModel):
    id: str
    title: str
    artist: str
    release_date: date
    acoustic: AcousticFeatures
    lyrical: LyricalContent
    cultural: CulturalContext
    neuro: NeuroResponse
    economic: EconomicStats
    social: SocialContext
    historical: HistoricalContext
