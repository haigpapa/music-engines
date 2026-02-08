# Frontend Design Proposal: Totality Engine

## Design Philosophy
**"The mixing console for your career."**
The interface should feel like a professional DAW (Digital Audio Workstation)—dense, data-rich, dark-mode first, and highly responsive. It acts as a "Head-Up Display" (HUD) for the music industry.

## Color Palette & Typography
-   **Backgrounds**: `pro-black` (#121212) for the canvas, `pro-gray` (#1E1E1E) for panels.
-   **Accents**:
    -   `electric-cyan` (#00FFFF): Primary actions, active states.
    -   `volt-green` (#C0FF00): Positive metrics, "Hit" indicators.
    -   `warning-orange` (#FF5722): Alerts, low scores, "Miss" indicators.
    -   `hot-pink` (#FF00FF): Creative/Lyrical highlights.
-   **Fonts**: `JetBrains Mono` for data/code, `Inter` for UI text.

## Core Navigation Structure
The app will be divided into three main Views, selectable via a global navigation bar.

### 1. The Workbench (Upload & Quick Analysis)
*Default View*
-   **Drop Zone**: Large, central area for drag-and-drop audio (WAV/MP3) and metadata (JSON/Text).
-   **Quick Stats**: Instant technical readout (BPM, Key, Loudness - LUFS) upon upload.
-   **Engine Router**: Toggle switches to send the track to specific engines (Creative, Hit Science, or both).

### 2. Creative Intelligence View (The "Art" View)
Focuses on the track's internal qualities.
-   **Audioscape Panel**: Spectrogram visualization, frequency balance graph.
-   **Lyrical Panel**: Scrolling lyrics with sentiment highlighting and keyword extraction.
-   **Composition Panel**: Timeline view showing song structure (Intro -> Verse -> Chorus) with energy levels.
-   **Context Panel**: Radar chart comparing the track to genre averages.

### 3. Hit Science View (The "Business" View)
Focuses on the track's external potential.
-   **The Hexagon**: A central hexagonal radar chart representing the 6 foundational systems (Creative, Industry, Platform, Market, Culture, Audience).
-   **Total Hit Score**: A large, central gauge (0-100) predicting probability of success.
-   **Recommendations**: Bulleted list of actionable steps to improve the score (e.g., "Increase social ad spend", "Shorten intro").

### 4. Comparison View
-   **Split Screen**: Select two tracks (loaded from history or upload).
-   **Diff View**: Highlights differences in key metrics (e.g., "Track B is +2dB louder", "Track A has 15% more lyrical complexity").

## Component Architecture
```
App
├── Header (Logo, System Status)
├── Navigation (Workbench | Creative | Hit Science | Compare)
├── MainContent
│   ├── WorkbenchView
│   │   ├── UploadZone
│   │   └── ProcessingStatus
│   ├── CreativeView
│   │   ├── AudioscapeWidget
│   │   ├── LyricalWidget
│   │   └── CompositionWidget
│   ├── HitScienceView
│   │   ├── HexagonChart
│   │   └── ScoreGauge
│   └── CompareView
│       ├── TrackSelector
│       └── DiffTable
└── Footer (Job Queue, server latency)
```
