(function () {
var header = document.getElementById('mainHeader');
var typingText = document.getElementById('typing-text');

if (header) {
var onScroll = function () {
if (window.scrollY > 20) {
header.classList.add('is-scrolled');
} else {
header.classList.remove('is-scrolled');
}
};

onScroll();
window.addEventListener('scroll', onScroll, { passive: true });
}

if (typingText) {
var roles = [
'Full Stack Python Developer',
'Backend Engineer',
'Software Engineer',
'Problem Solver'
];

var roleIndex = 0;
var charIndex = 0;
var deleting = false;

var typeLoop = function () {
var currentRole = roles[roleIndex];

if (!deleting) {
charIndex += 1;
typingText.textContent = currentRole.slice(0, charIndex);

if (charIndex === currentRole.length) {
deleting = true;
setTimeout(typeLoop, 1300);
return;
}

setTimeout(typeLoop, 85);
} else {
charIndex -= 1;
typingText.textContent = currentRole.slice(0, charIndex);

if (charIndex === 0) {
deleting = false;
roleIndex = (roleIndex + 1) % roles.length;
setTimeout(typeLoop, 250);
return;
}

setTimeout(typeLoop, 45);
}
};

typeLoop();
}

var projectItems = document.querySelectorAll('#portfolio .project-reveal');

if (projectItems.length > 0 && 'IntersectionObserver' in window) {
var revealObserver = new IntersectionObserver(function (entries, observer) {
entries.forEach(function (entry) {
if (entry.isIntersecting) {
var delay = Number(entry.target.getAttribute('data-delay') || '0');
setTimeout(function () {
entry.target.classList.add('is-visible');
}, Math.max(0, delay * 1000));
observer.unobserve(entry.target);
}
});
}, { threshold: 0.2 });

projectItems.forEach(function (item) {
revealObserver.observe(item);
});
}
})();