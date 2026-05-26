document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('feedbackModal');
    const input = document.getElementById('decisionInput');
    const title = document.getElementById('modalTitle');
    
    // Grab buttons by ID
    const btnYes = document.getElementById('btn-yes');
    const btnNo = document.getElementById('btn-no');

    function openModal(decision) {
        input.value = decision;
        title.innerText = decision === 'YES' ? "Excellent Choice. Any final words?" : "Wow. Care to explain yourself?";
        modal.style.display = 'flex';
    }

    // Attach listeners
    if (btnYes) btnYes.addEventListener('click', () => openModal('YES'));
    if (btnNo) btnNo.addEventListener('click', () => openModal('NO'));

    // Close modal if clicking outside the content box
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});