document.addEventListener('DOMContentLoaded', function() {
    // This script is ONLY for the homepage (index.html)
    
    // --- STATUS CHECK LOGIC ---
    const statusOverlay = document.getElementById('status-overlay');
    const statusMessage = document.getElementById('status-message');
    const initialStatusData = document.getElementById('initial-status-data');

    function checkInitialStatus() {
        if (!initialStatusData || !statusOverlay) {
            console.error("Required status elements not found on this page.");
            return;
        }

        const isComplete = initialStatusData.dataset.complete === 'true';
        const message = initialStatusData.dataset.message;

        if (isComplete) {
            statusMessage.textContent = "System ready. Welcome.";
            setTimeout(() => {
                statusOverlay.classList.add('hidden');
            }, 1000);
        } else {
            statusMessage.textContent = message;
            const statusInterval = setInterval(async () => {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    statusMessage.textContent = data.message;
                    if (data.complete) {
                        clearInterval(statusInterval);
                        statusMessage.textContent = "System ready. Welcome.";
                        setTimeout(() => {
                            statusOverlay.classList.add('hidden');
                        }, 1000);
                    }
                } catch (error) {
                    statusMessage.textContent = "Cannot reach Minerva's core. Please refresh.";
                    clearInterval(statusInterval);
                }
            }, 3000);
        }
    }
    
    checkInitialStatus();

    // --- NEW: SCROLL ANIMATION LOGIC ---
    const animatedSections = document.querySelectorAll('.animated-section');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Optional: stop observing once animated
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    animatedSections.forEach(section => {
        observer.observe(section);
    });
});
