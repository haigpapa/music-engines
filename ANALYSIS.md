# Music Engines Analysis

## Overview
The "Music Engines" (Totality Engine) project is a sophisticated system for analyzing music audio and metadata to derive insights about quality, hit potential, and structural composition.

## Core Component: Totality Engine
Located in `totality_engine`, this backend powers the analysis.

### 1. Creative Engine (`totality_engine/engines/creative`)
Focused on the artistic and diverse technical aspects of a track.
- **Audioscape (`audioscape.py`)**: Technical analysis of audio signals (waveform, spectrogram, frequency response).
- **Lyrical Intelligence (`lyrical.py`)**: Natural Language Processing (NLP) on lyrics to determine sentiment, themes, and complexity.
- **Composition (`composition.py`)**: Structural analysis (intro, verse, chorus, bridge) and arrangement.
- **Album Architect (`album_architect.py`)**: Analyzes collections of tracks to determine cohesion and flow.
- **Context (`context.py`)**: Benchmarks the track against market standards or an artist's previous work.

### 2. Hit Science Engine (`totality_engine/engines/hit_science`)
A systems-theoretical approach to predicting "hit" potential. It appears to be based on a pipeline that aggregates data from 6 key systems:
1.  **Creative System**: The song itself (quality, hooks).
2.  **Industry System**: Label support, team, resources.
3.  **Platform System**: DSP algorithms, playlisting.
4.  **Market System**: Trends, competition, timing.
5.  **Culture System**: Zeitgeist, memes, virality.
6.  **Audience System**: Demographics, psychographics, retention.

### 3. Comparison Engine (`totality_engine/engines/comparison.py`)
Allows for side-by-side comparison of two tracks (e.g., "Demo vs. Final Master" or "Song A vs. Hit Song B").

## Current Frontend State
Located in `frontend`.
- **Stack**: React (Vite), Tailwind CSS.
- **Design System**: "Pro Audio" aesthetic. Dark mode by default (`pro-black`, `pro-gray`) with high-contrast accents (`electric-cyan`, `volt-green`, `warning-orange`).
- **Functionality**: Basic upload and result visualization is scaffolded but not fully integrated with all engines.
