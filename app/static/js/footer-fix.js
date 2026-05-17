// Ensure footer links are always clickable (z-index fix)
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.footer-link, .site-footer a').forEach(function (link) {
        link.style.pointerEvents = 'auto';
        link.style.cursor = 'pointer';
        link.style.zIndex = '1000';
    });
});
