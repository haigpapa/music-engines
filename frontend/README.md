# Music Engines Frontend
> **A modern React SPA for visualizing deep audio analysis.**
> *React • Vite • Tailwind CSS • Brutalist Neumorphism*

This frontend provides the interface for the Totality Engine. It is built as a Single Page Application (SPA) and served by the Flask backend in production.

## Design Philosophy: "Minimal Brutalist Neumorphism"
The UI combines two distinct styles:
1.  **Brutalism**: Bold typography, high contrast, stark layout.
2.  **Neumorphism**: Soft, extruded shadows for interactive elements (`box-shadow`), creating a tactile feel.

## Architecture

### Connectivity
-   **Upload**: `POST /analyze` -> Returns `job_id`.
-   **Polling**: `GET /jobs/<job_id>` -> Polls every 2s until `completed`.
-   **State**: Managed via `useAnalysis.js` hook.

### Key Components
-   `src/components/UploadZone.jsx`: Handles file drag-and-drop with neumorphic press states.
-   `src/components/AnalysisDashboard.jsx`: Visualizes complex nested JSON data (Resonance, Hit Science).
-   `src/index.css`: Contains the custom Tailwind utility classes for the design system.

## Development

### Setup
```bash
npm install
```

### Dev Server (Standalone)
Runs on port 5173. Note: API calls will fail unless you configure a proxy to Flask (5001).
```bash
npm run dev
```

### Production Build
Builds to `dist/`, which is then served by `server.py`.
```bash
npm run build
```
