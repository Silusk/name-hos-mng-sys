alert("Welcome to our site");

// Smooth scroll for nav links
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Optional confirmation alert (does not block Flask submission)
const form = document.getElementById('contactForm');
form.addEventListener('submit', () => {
    alert('Thank you! Your message has been sent.');
});