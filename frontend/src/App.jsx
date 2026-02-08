import { useState } from 'react';
import { useAnalysis } from './hooks/useAnalysis';
import UploadZone from './components/UploadZone.jsx';
import AnalysisDashboard from './components/AnalysisDashboard.jsx';

function App() {
  const { startAnalysis, status, result, error, jobId } = useAnalysis();
  const [lyrics, setLyrics] = useState('');

  const handleFileSelected = (file) => {
    startAnalysis(file, lyrics);
  };

  return (
    <div className="min-h-screen bg-neu-bg text-neu-text font-mono p-4 md:p-8 selection:bg-neu-accent selection:text-black">

      {/* Brutalist Header */}
      <header className="mb-12 flex justify-between items-end border-b-4 border-neu-text pb-4">
        <div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter uppercase leading-none">
            TOTALITY<br />
            <span className="text-neu-accent">ENGINE</span>
          </h1>
          <p className="mt-2 text-xs font-bold tracking-widest text-gray-500">
            V.4.0 // DEEP LISTENING // RESONANCE
          </p>
        </div>
        <div className="text-right">
          <div className={`text-xs font-bold uppercase tracking-widest ${status === 'processing' ? 'text-neu-accent animate-pulse' : 'text-gray-600'}`}>
            SYSTEM STATUS: {status === 'idle' ? 'STANDBY' : status.toUpperCase()}
          </div>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">

        {/* Left Column: Input Vector */}
        <div className="lg:col-span-4 space-y-8">

          {/* Lyrics Input (Neumorphic) */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-500 uppercase tracking-widest pl-1">
              Lyrical Context (Optional)
            </label>
            <textarea
              className="neu-input h-32 resize-none text-xs font-mono"
              placeholder="PASTE LYRICS HERE TO ACTIVATE RESONANCE ENGINE..."
              value={lyrics}
              onChange={(e) => setLyrics(e.target.value)}
              disabled={status === 'processing' || status === 'uploading'}
            ></textarea>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-500 uppercase tracking-widest pl-1">
              Audio Vector
            </label>
            <UploadZone
              onFileSelected={handleFileSelected}
              isProcessing={status === 'uploading' || status === 'processing'}
            />
          </div>

          {error && (
            <div className="p-4 bg-neu-bg shadow-neu-pressed border-l-4 border-red-500 text-red-500 text-xs font-bold">
              ERROR: {error}
            </div>
          )}

          {jobId && (
            <div className="p-4 bg-neu-bg shadow-neu-pressed text-xs text-gray-600 font-mono flex justify-between">
              <span>JOB ID:</span>
              <span>{jobId}</span>
            </div>
          )}
        </div>

        {/* Right Column: Intelligence Output */}
        <div className="lg:col-span-8">
          {result ? (
            <AnalysisDashboard result={result} />
          ) : (
            <div className="h-96 md:h-full rounded-xl shadow-neu-pressed flex items-center justify-center border border-transparent">
              <div className="text-center opacity-30">
                <div className="text-6xl mb-4 font-black text-gray-800">∅</div>
                <span className="text-sm font-bold tracking-widest text-gray-600">
                  AWAITING INPUT DATA
                </span>
              </div>
            </div>
          )}
        </div>

      </main>
    </div>
  )
}

export default App;
