import { useState, useRef } from 'react';

const API_BASE = ''; // Relative path for same-origin

export const useAnalysis = () => {
    const [status, setStatus] = useState('idle'); // idle, uploading, processing, completed, error
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [jobId, setJobId] = useState(null);
    const pollInterval = useRef(null);

    const startAnalysis = async (file, lyrics) => {
        setStatus('uploading');
        setError(null);
        setResult(null);
        setJobId(null);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('lyrics', lyrics || '');
        formData.append('artist_id', 'unknown');
        formData.append('platform', 'Spotify');
        formData.append('target_markets', 'US');

        try {
            // Step 1: Upload and Queue Task
            const response = await fetch(`${API_BASE}/analyze`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(`Upload failed: ${response.status} ${errText}`);
            }

            const data = await response.json();

            if (data.status === 'queued') {
                setJobId(data.job_id);
                setStatus('processing');
                startPolling(data.job_id);
            } else {
                throw new Error(data.error || 'Failed to queue task');
            }

        } catch (err) {
            console.error("Analysis Error:", err);
            setError(err.message || "An unexpected error occurred.");
            setStatus('error');
        }
    };

    const startPolling = (id) => {
        if (pollInterval.current) clearInterval(pollInterval.current);

        pollInterval.current = setInterval(async () => {
            try {
                const res = await fetch(`${API_BASE}/jobs/${id}`);
                if (!res.ok) throw new Error('Polling failed');

                const data = await res.json();
                console.log("Job status:", data.status);

                if (data.status === 'completed') {
                    clearInterval(pollInterval.current);

                    // Server returns: { "status": "completed", "result": { "status": "success", "results": ... } }
                    // Worker returns: { "status": "success", "results": result_dict }

                    if (data.result && data.result.results) {
                        setResult(data.result.results);
                    } else if (data.result) {
                        setResult(data.result);
                    }

                    setStatus('completed');
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval.current);
                    setError(data.error || "Task failed");
                    setStatus('error');
                }
                // If 'queued' or 'processing', continue polling

            } catch (err) {
                clearInterval(pollInterval.current);
                setError(err.message);
                setStatus('error');
            }
        }, 2000); // Poll every 2 seconds
    };

    return {
        status,
        jobId,
        result,
        error,
        startAnalysis
    };
};
