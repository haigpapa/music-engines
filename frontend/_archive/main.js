// Glitch Effect for Hero Text
const glitchTexts = document.querySelectorAll('.glitch');

glitchTexts.forEach(text => {
  let originalText = text.getAttribute('data-text');
  let iterations = 0;
  
  const interval = setInterval(() => {
    text.innerText = originalText
      .split('')
      .map((letter, index) => {
        if (index < iterations) {
          return originalText[index];
        }
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[Math.floor(Math.random() * 26)];
      })
      .join('');
    
    if (iterations >= originalText.length) {
      clearInterval(interval);
    }
    
    iterations += 1 / 3;
  }, 30);
});

// Smooth Scroll for Navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Intersection Observer for Fade-in Animations
const observerOptions = {
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
  section.classList.add('fade-in-section');
  observer.observe(section);
});

// Hit Science Form Handler
const form = document.getElementById('analysis-form');
const resultsContainer = document.querySelector('#analysis-results pre');

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const fileInput = document.getElementById('audio-file');
        const artistInput = document.getElementById('artist-name');
        const submitBtn = form.querySelector('button');
        
        if (!fileInput.files[0]) return;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('artist_id', artistInput.value);
        formData.append('platform', "Spotify");
        formData.append('target_markets', "US,UK");

        submitBtn.textContent = "Analyzing...";
        submitBtn.disabled = true;
        resultsContainer.textContent = "Processing audio... (this may take a moment)";

        try {
            const response = await fetch('/hit-science/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const data = await response.json();
            resultsContainer.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            resultsContainer.textContent = `Error: ${error.message}`;
        } finally {
            submitBtn.textContent = "Analyze Track";
            submitBtn.disabled = false;
        }
    });
}
