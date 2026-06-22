document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('feedbackModal');
    const input = document.getElementById('decisionInput');
    const title = document.getElementById('modalTitle');
    
    const btnYes = document.getElementById('btn-yes');
    const btnNo = document.getElementById('btn-no');

    // Runaway Button Logic
    const dodgeButton = (button) => {
        const width = button.offsetWidth || 100;
        const height = button.offsetHeight || 45;

        // ONLY move it to the body if it hasn't been moved already.
        // This stops the DOM from thrashing on every single hover.
        if (button.parentNode !== document.body) {
            // Keep its size from collapsing when it leaves its flex parent
            button.style.width = `${width}px`;
            button.style.height = `${height}px`;
            button.style.position = 'fixed';
            button.style.zIndex = '99999';
            document.body.appendChild(button);
        }

        // 2. Set safe boundaries so it doesn't teleport completely off the screen
        const padding = 50; 
        const safeX = Math.max(0, window.innerWidth - width - padding);
        const safeY = Math.max(0, window.innerHeight - height - padding);

        // 3. Generate random coordinates within the safe viewport zone
        const randomX = Math.floor(Math.random() * safeX) + padding;
        const randomY = Math.floor(Math.random() * safeY) + padding;

        // 4. Reposition the button instantly
        button.style.left = `${randomX}px`;
        button.style.top = `${randomY}px`;
    };

    // Trigger the dodge on desktop hover
    btnNo.addEventListener('mouseover', () => {
        dodgeButton(btnNo);
    });

    // Trigger the dodge on mobile screen taps
    btnNo.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Stop the actual button click from firing
        dodgeButton(btnNo);
    });


    // --- Core Modal Logic (unchanged) ---
    function openModal(decision) {
        input.value = decision;
        title.innerText = decision === 'YES' ? "Excellent Choice. How can I get in touch with you?" : "Wow. Care to explain yourself?";
        modal.style.display = 'flex';
    }

    // Only 'Yes' can naturally trigger the modal now
    if (btnYes) btnYes.addEventListener('click', () => openModal('YES'));

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Carousel Logic
    const track = document.getElementById('carouselTrack');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const dotsNav = document.getElementById('carouselNav');
    
    // Safety check in case the elements aren't rendered
    if (track && nextBtn && prevBtn && dotsNav) {
        const dots = Array.from(dotsNav.children);
        let currentIndex = 0;
        const totalSlides = dots.length;

        const updateCarousel = (index) => {
            // Slide the track using CSS transforms
            track.style.transform = `translateX(-${index * 100}%)`;
            
            // Update active dot styling
            dotsNav.querySelector('.current-indicator').classList.remove('current-indicator');
            dots[index].classList.add('current-indicator');
        };

        // Next Button Click
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex === totalSlides - 1) ? 0 : currentIndex + 1;
            updateCarousel(currentIndex);
        });

        // Previous Button Click
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex === 0) ? totalSlides - 1 : currentIndex - 1;
            updateCarousel(currentIndex);
        });

        // Dot Click (jump to specific slide)
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentIndex = index;
                updateCarousel(currentIndex);
            });
        });
    }
});