# Music Engines MVP (The Totality Engine)

> A systems-theoretical optimization engine for music analysis and "Hit Science".
> Also known as the **Totality Engine**.

## Component Overview

This repository contains the **Minimum Viable Product (MVP)** implementation of the Totality Engine:

1.  **Totality Engine (Backend)**: 22 specialized Python modules covering Creative, Market, Industry, and Audience analysis.
2.  **Unified API**: A Flask server orchestrating the `HitSciencePipeline`.
3.  **Web Interface (Frontend)**: A modern drag-and-drop UI for real-time analysis visualization.
4.  **Result Persistence**: Automatic storage of analysis results to a local SQLite database (`totality.db`).

## verified Modules

The engine consists of 22 independently verifiable modules across:
*   **Creative**: `album_architect`, `audioscape`, `composition`, `context`, `lyrical`
*   **Hit Science**: `audience` (neuro, growth), `creative` (audio, nlp), `culture` (distance), `industry` (centrality), `market` (risk), `platform` (virality)

## Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies including Flask and Librosa
pip install -r requirements.txt
```

### 2. Verify System Health

Run the included verification script to check all 22 modules:

```bash
python3 verify_modules.py
# Expected Output: Summary: 23/23 modules passed.
```

### 3. Run the Application

Start the API and Web Server:

```bash
# Standard Launch
python3 server.py

# Alternative Launch (if Port 5000 is busy)
PORT=5001 python3 server.py
```

The server runs on **http://localhost:5000** (or configured port).

### 4. Usage

1.  Open **http://localhost:5000** in your browser.
2.  Drag and drop an audio file (MP3, WAV, FLAC).
3.  Click **INITIALIZE ANALYSIS**.
4.  View detailed metrics for Creative, Platform, Market, Audience, and Industry dimensions.
5.  View past analyses at `/history`.

## Architecture

*   **Server**: `server.py` (Flask) - Handles uploads, pipeline orchestration, and database persistence.
*   **Pipeline**: `totality_engine/engines/hit_science/pipeline.py` - Connects all analysis modules.
*   **Frontend**: `frontend/` - Vanilla JS + CSS for a lightweight, responsive UI.
*   **Database**: `totality.db` (SQLite) - Stores analysis results (`AnalysisResult` model).
