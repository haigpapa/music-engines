from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Dict, Any
from sqlalchemy import Column, JSON

# --- Relationship / Join Tables ---

class Credit(SQLModel, table=True):
    """Link table between SongVersion and Contributor."""
    version_id: Optional[int] = Field(default=None, foreign_key="songversion.id", primary_key=True)
    contributor_id: Optional[int] = Field(default=None, foreign_key="contributor.id", primary_key=True)
    role: str  # e.g., "producer", "songwriter"
    role_detail: Optional[str] = None

class SongVersionGenre(SQLModel, table=True):
    """Link table between SongVersion and GenreTag (omitted for brevity, essentially a tag)."""
    version_id: Optional[int] = Field(default=None, foreign_key="songversion.id", primary_key=True)
    genre: str = Field(primary_key=True) # Storing genre as string for now for simplicity

# --- Core Entities ---

class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    primary_market_id: Optional[int] = Field(default=None, foreign_key="market.id")
    
    # Relationships
    songs: List["Song"] = Relationship(back_populates="primary_artist")

class Contributor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role_type: str # e.g. "writer", "producer"

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str # Label, Distributor, Publisher

class Market(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str # country, region

class Song(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    canonical_title: str
    primary_artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    
    # Relationships
    primary_artist: Optional[Artist] = Relationship(back_populates="songs")
    versions: List["SongVersion"] = Relationship(back_populates="song")

class SongVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    song_id: Optional[int] = Field(default=None, foreign_key="song.id")
    version_type: str = Field(default="original")
    isrc: Optional[str] = None
    release_date: Optional[datetime] = None
    duration_ms: Optional[int] = None
    
    # Relationships
    song: Optional[Song] = Relationship(back_populates="versions")
    audio_features: Optional["AudioFeatures"] = Relationship(back_populates="version")
    lyric_features: Optional["LyricFeatures"] = Relationship(back_populates="version")
    platform_metrics: List["PlatformMetric"] = Relationship(back_populates="version")

# --- Feature Tables ---

class AudioFeatures(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version_id: int = Field(foreign_key="songversion.id")
    
    # Basic
    tempo_bpm: float
    time_signature: int
    key_estimated: int
    mode_estimated: int # 1 major, 0 minor
    
    # Advanced
    loudness_lufs: float
    dynamic_range_db: float
    spectral_centroid_avg: float
    harmonic_surprise_index: Optional[float] = None
    
    # Relationship
    version: Optional[SongVersion] = Relationship(back_populates="audio_features")

class LyricFeatures(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version_id: int = Field(foreign_key="songversion.id")
    
    language_id: str
    word_count: int
    sentiment_valence: float
    sentiment_arousal: Optional[float] = None
    rhyme_density: Optional[float] = None
    explicit_content: bool = False
    
    # Relationship
    version: Optional[SongVersion] = Relationship(back_populates="lyric_features")

class MarketContext(SQLModel, table=True):
    """Context for a specific market (e.g., US, BR)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    market_id: int = Field(foreign_key="market.id")
    gdp_per_capita: Optional[float] = None
    streaming_penetration: Optional[float] = None
    censorship_score: float = 0.0

# --- Event / Metric Tables ---

class PlatformMetric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version_id: int = Field(foreign_key="songversion.id")
    platform_name: str # Spotify, TikTok
    date: datetime
    
    streams: int = 0
    saves: int = 0
    skips: int = 0
    
    version: Optional[SongVersion] = Relationship(back_populates="platform_metrics")

class PlaylistEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version_id: int = Field(foreign_key="songversion.id")
    playlist_name: str
    date_added: datetime
    position: Optional[int] = None
    is_editorial: bool = False

class SocialTrendEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version_id: int = Field(foreign_key="songversion.id")
    platform: str
    event_start_date: datetime
    ugc_count: int
class AnalysisResult(SQLModel, table=True):
    """Raw storage for analysis results."""
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str
    raw_json: str # Storing as stringified JSON for SQLite compatibility and simplicity
    
    # AI Embeddings (for Similarity Search)
    embedding_json: Optional[str] = None # JSON list of floats
    
    # Resonance Metrics
    dissonance_score: Optional[float] = None
    vibe_descriptor: Optional[str] = None
    lyrical_sentiment: Optional[str] = None
    
    # Metadata for searching
    artist_id: Optional[str] = None
    markets: Optional[str] = None
