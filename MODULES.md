# Music Engines: Module Manifest

This document details the status, capabilities, and limitations of the 22 modules within the Totality Engine.

## Status Key
-   🟢 **Production**: Fully implemented using industry-standard libraries (Librosa, Torch, Transformers).
-   🟡 **MVP / Beta**: Functional logic present, but relies on heuristics or simplified models.
-   🔴 **Stub / Simulation**: Returns mock data or hardcoded values; needs implementation.
-   🟠 **Disconnected**: Logic exists but is not currently fed by the main data pipeline.

---

## 1. Creative Engine (The "Ears")
*Focus: Audio Signal & Lyrical Content*

| Module | File | Status | What Works Well | Needs Work |
| :--- | :--- | :--- | :--- | :--- |
| **Deep Listening** | `deep_listening.py` | 🟢 | Uses `AST` (Audio Spectrogram Transformer) to generate 768-dim embeddings. Real ML inference. | Model is heavy (500MB+). Could be optimized with quantization. |
| **Resonance** | `resonance.py` | 🟡 | Cross-modal analysis (Lyrics vs Audio). Uses `DistilBERT` for lyrics. | Audio valence is a heuristic derived from energy, needs a trained regression model. |
| **Audioscape** | `audioscape.py` | 🟢 | Extracts technical features (Spectral Centroid, Rolloff, ZCR) using `librosa`. | Analysis is purely signal-based, lacks "perceptual" mapping. |
| **Lyrical** | `lyrical.py` | 🟢 | Uses NLP for sentiment, rhyme density, and complexity. | "Theme detection" is basic keyword matching. |
| **Composition** | `composition.py` | 🟡 | Detects sections (Verse/Chorus) using similarity matrices. | Segment labeling is generic (A/B/C) rather than semantic (Verse/Chorus). |
| **Context** | `context.py` | 🔴 | Placeholder for benchmarking against artist catalog. | Currently returns mock comparison data. |
| **Album Architect** | `album_architect.py` | 🔴 | Placeholder for playlist/album cohesion. | Not integrated into main pipeline. |

---

## 2. Hit Science Engine (The "Brain")
*Focus: Predicting Success & Risk*

### Creative System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Audio Analyzer** | 🟢 | Wrapper around Creative Engine. | Redundant with Creative Engine. |
| **NLP Engine** | 🟢 | Wrapper around Lyrical Engine. | Redundant. |
| **Explicitness** | 🟡 | Keyword-based detection (Profanity check). | Needs context awareness (e.g., reclaimed slurs). |
| **Code Switching** | 🔴 | Intended to detect multi-language usage. | Currently a stub returning `False`. |
| **Harmonic** | 🟡 | Key/Mode detection via `librosa.chroma`. | Often confuses relative majors/minors. |

### Audience System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Neuro** | 🟢 | Calculates "Spectral Burstiness" (Hook Efficacy) using onset strength peaks. | "Hook Prediction" is a header-heuristic, not trained on actual brain data. |
| **Growth** | 🔴 | Simulates fan retention rates. | No integration with actual streaming data (Spotify for Artists). |
| **Lift** | 🔴 | Simulates playlist addition probability. | Purely random/mock logic. |

### Industry System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Centrality** | 🟠 | Logic for Graph Centrality exists (using NetworkX). | **Disconnected**. The engine analyzes an empty in-memory graph, while the worker populates the real Neo4j graph. Needs bridging. |
| **Graph Model** | 🟢 | Neo4j integration for Artist/Track relationship. | Only tracks basic `PERFORMED` and `HAS_VIBE` relationships. |

### Market System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Risk Map** | 🔴 | Checks Geopolitical risk for specific countries (CN, RU). | logic is hardcoded lists. Needs real-time API. |
| **Economics** | 🔴 | Placeholder for monetization modeling. | Not implemented. |

### Platform System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Virality** | 🔴 | "Viral Elasticity" score. | Returns random float. Needs TikTok trend ingestion. |
| **Optimization** | 🔴 | metadata optimization suggestions. | Returns static string suggestions. |

### Culture System
| Module | Status | Capabilities | Limitations |
| :--- | :--- | :--- | :--- |
| **Distance** | 🔴 | Cultural distance metrics. | Stub. |
| **Identity** | 🔴 | Subculture mapping. | Stub. |

---

## Summary
*   **Audio/Lyrics Analysis**: Production Ready (Green).
*   **Infrastructure (Async/Graph)**: Production Ready (Green).
*   **Market/Business Logic**: Prototype/Stub (Red).

**Next Technical Step**: Connect the **Industry System** (`centrality.py`) to the **Neo4j Graph** to fix the "Disconnected" status.
