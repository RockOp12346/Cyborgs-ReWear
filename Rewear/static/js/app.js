document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    const learnMoreButtons = document.querySelectorAll('.learn-more');

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        if (name && email && message) {
            alert(`Thank you, ${name}! Your message has been sent.`);
            contactForm.reset();
        }
    });

    learnMoreButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const serviceTitle = e.target.closest('.card').querySelector('.card-title').textContent;
            alert(`More details about ${serviceTitle} coming soon!`);
        });
    });

    // Smooth scrolling for navigation
    document.querySelectorAll('a.nav-link').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
});