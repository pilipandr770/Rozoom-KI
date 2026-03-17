/**
 * Language switcher – direct navigation (no AJAX).
 * The server sets the cookie and redirects back to the same page.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Visual feedback only: animate the clicked button.
    document.querySelectorAll('.lang-button').forEach(function (btn) {
        btn.addEventListener('click', function () {
            this.classList.add('clicked');
            // Let default <a> navigation handle the rest.
        });
    });
});
