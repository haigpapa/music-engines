import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

const VibeRadar = ({ data }) => {
    // Transform AnalysisResult into chart data
    // Assuming data structure from pipeline.py
    const chartData = [
        { subject: 'Creative', A: (data.creative?.harmonic_entropy || 0.5) * 100, fullMark: 100 },
        { subject: 'Audience', A: (data.audience?.spectral_burstiness || 0) > 100 ? 100 : (data.audience?.spectral_burstiness || 0), fullMark: 100 },
        { subject: 'Industry', A: (data.industry?.artist_centrality || 0) * 10, fullMark: 100 }, // Centrality is usually small
        { subject: 'Resonance', A: (data.resonance?.dissonance_score || 0) * 100, fullMark: 100 },
        { subject: 'Viral', A: (data.platform?.viral_elasticity || 0) * 100, fullMark: 100 },
        { subject: 'Risk', A: 100 - ((data.market?.risk_score || 0) * 100), fullMark: 100 },
    ];

    return (
        <div className="h-64 w-full bg-pro-gray-900 rounded-xl shadow-neu-pressed flex items-center justify-center p-4">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                    <PolarGrid stroke="#333" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#888', fontSize: 10 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                        name="Track Profile"
                        dataKey="A"
                        stroke="#00f0ff" // Electric Cyan
                        strokeWidth={2}
                        fill="#00f0ff"
                        fillOpacity={0.3}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default VibeRadar;
