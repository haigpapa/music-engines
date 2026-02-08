const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const analyzeBtn = document.getElementById('analyze-btn');
const loadingBar = document.getElementById('loading-bar');
const resultsSection = document.getElementById('results-section');
const jsonOutput = document.getElementById('json-output');
const dashboardGrid = document.querySelector('.dashboard-grid');
const resultFilename = document.getElementById('result-filename');

let selectedFile = null;

// Drag & Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    dropZone.querySelector('h2').textContent = file.name;
    dropZone.querySelector('p').textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
    analyzeBtn.disabled = false;
    resultFilename.textContent = file.name;

    // Reset view
    resultsSection.classList.add('hidden');
    dashboardGrid.innerHTML = '';
}

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('artist_id', document.getElementById('artist-id').value);
    formData.append('target_markets', document.getElementById('markets').value);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            renderResults(data.results);
            jsonOutput.textContent = JSON.stringify(data, null, 2);
            resultsSection.classList.remove('hidden');
        } else {
            alert(`Error: ${data.error || 'Analysis failed'}`);
        }
    } catch (error) {
        console.error(error);
        alert('Network error. Is the server running?');
    } finally {
        setLoading(false);
    }
});

function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    if (isLoading) {
        loadingBar.classList.remove('hidden');
        analyzeBtn.textContent = "ANALYZING...";
    } else {
        loadingBar.classList.add('hidden');
        analyzeBtn.textContent = "INITIALIZE ANALYSIS";
    }
}

function renderResults(results) {
    dashboardGrid.innerHTML = '';

    // Creative System
    if (results.creative) {
        createCard('Creative Metrics', {
            'Tempo': results.creative.tempo ? `${results.creative.tempo.toFixed(1)} BPM` : 'N/A',
            'Spectral Flux': results.creative.spectral_flux_mean ? results.creative.spectral_flux_mean.toFixed(2) : 'N/A',
            'Explicitness': results.creative.is_explicit ? 'EXPLICIT' : 'Clean',
            'Languages': results.creative.languages ? results.creative.languages.join(', ') : 'Unknown'
        });
    }

    // Platform System
    if (results.platform) {
        createCard('Platform Performance', {
            'Viral Elasticity': results.platform.viral_elasticity ? results.platform.viral_elasticity.toFixed(2) : 'N/A',
            'Optimizations': results.platform.optimizations ? results.platform.optimizations.length : 0
        });
    }

    // Market System
    if (results.market) {
        const risk = results.market.geopolitical_risks || {};
        createCard('Market Risk', {
            'Risk Score': risk.risk_score ? risk.risk_score : 'Low'
        });
    }

    // Audience System
    if (results.audience) {
        createCard('Audience Impact', {
            'Hook Efficacy': results.audience.hook_efficacy ? results.audience.hook_efficacy.toFixed(2) : 'N/A'
        });
    }

    // Industry System
    if (results.industry) {
        createCard('Industry Connectivity', {
            'Centrality': results.industry.artist_centrality ? results.industry.artist_centrality.toFixed(3) : '0.000'
        });
    }
}

function createCard(title, data) {
    const card = document.createElement('div');
    card.className = 'result-card';

    const h4 = document.createElement('h4');
    h4.textContent = title;
    card.appendChild(h4);

    for (const [key, value] of Object.entries(data)) {
        const row = document.createElement('div');
        row.className = 'stat-row';

        const label = document.createElement('span');
        label.textContent = key;

        const val = document.createElement('span');
        val.className = 'stat-value';
        val.textContent = value;
        val.style.color = '#00ff9d'; // consistent highlight

        row.appendChild(label);
        row.appendChild(val);
        card.appendChild(row);
    }

    dashboardGrid.appendChild(card);
}
