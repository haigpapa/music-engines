import React from 'react';

const AnalysisDashboard = ({ result }) => {
    // Parsing result data
    const resonance = result?.resonance || {};
    const creative = result?.creative || {};

    // Safety checks
    const vibe = resonance.vibe || "Undetected";
    const dissonance = resonance.dissonance_score || 0;
    const lySentiment = resonance.lyrical_sentiment || "Unknown";

    // Creative metrics
    const tempo = creative.tempo ? Math.round(creative.tempo) : "---";
    const model = creative.model ? creative.model.split('/')[1] : "Standard"; // AST

    // Determine bar color based on Dissonance (High Dissonance = Red/Orange, Low = Green/Blue)
    // Actually, distinct colors for Neumorphism
    const items = [
        { label: "LYRICAL SENTIMENT", value: lySentiment },
        { label: "AUDIO MODEL", value: model },
        { label: "BPM", value: tempo }
    ];

    return (
        <div className="h-full animate-in fade-in duration-700 flex flex-col space-y-6">

            {/* 1. Main Vibe Card (Neumorphic) */}
            <div className="neu-card">
                <div className="flex justify-between items-start mb-4">
                    <h2 className="text-neu-accent text-sm font-bold uppercase tracking-widest">Resonance Vibe</h2>
                    <div className="px-2 py-1 rounded bg-neu-bg shadow-neu-pressed font-mono text-[10px] text-gray-500">
                        CONFIDENCE: HIGH
                    </div>
                </div>
                <div className="text-3xl md:text-5xl font-black text-neu-text tracking-tighter uppercase leading-none">
                    {vibe}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-grow">

                {/* 2. Dissonance Meter */}
                <div className="neu-card flex flex-col justify-center">
                    <h3 className="text-gray-500 text-xs uppercase tracking-widest mb-6">Lyrical / Sonic Friction</h3>

                    <div className="relative pt-2">
                        <div className="flex justify-between text-xs font-mono text-gray-400 mb-2">
                            <span>ALIGNED (0.0)</span>
                            <span>{dissonance.toFixed(2)}</span>
                            <span>CLASHING (1.0)</span>
                        </div>
                        <div className="neu-progress-container h-6">
                            <div
                                className="h-full bg-neu-accent shadow-none transition-all duration-1000 ease-out"
                                style={{ width: `${dissonance * 100}%` }}
                            ></div>
                        </div>
                    </div>

                    <p className="mt-6 text-xs text-gray-400 font-mono leading-relaxed">
                        "Friction" measures the emotional distance between the lyrics ({lySentiment}) and the audio track's mood.
                        {dissonance > 0.5 ? " High tension detected." : " Elements are emotionally aligned."}
                    </p>
                </div>

                {/* 3. System Telemetry */}
                <div className="neu-card space-y-4">
                    <h3 className="text-gray-500 text-xs uppercase tracking-widest mb-4">System Telemetry</h3>

                    <div className="space-y-3">
                        {items.map((item, idx) => (
                            <div key={idx} className="flex justify-between items-center p-3 rounded-lg shadow-neu-pressed">
                                <span className="text-xs text-gray-500 font-bold">{item.label}</span>
                                <span className="text-sm font-mono text-neu-text">{item.value}</span>
                            </div>
                        ))}
                    </div>

                    <div className="mt-4 pt-4 border-t border-[#222]">
                        <p className="text-[10px] text-gray-600 font-mono">
                            AI MODEL: MIT/AST-FINETUNED<br />
                            NLP MODEL: DISTILBERT-SST-2
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AnalysisDashboard;
