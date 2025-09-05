// @ts-nocheck
/**
 * Admin dashboard chart initialization
 * This is a Jinja template that will be processed server-side
 * The output is JavaScript code that initializes charts
 */

document.addEventListener('DOMContentLoaded', function() {
    // Publication status chart
    const statusCtx = document.getElementById('publishStatusChart')?.getContext('2d');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: ['Published', 'Draft'],
                datasets: [{
                    data: [{{ published_posts }}, {{ draft_posts }}],
                    backgroundColor: ['#28a745', '#6c757d'],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Category distribution chart
    const categoryCtx = document.getElementById('categoryChart')?.getContext('2d');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'bar',
            data: {
                labels: [{% for category in posts_by_category %}"{{ category[0] }}"{% if not loop.last %}, {% endif %}{% endfor %}],
                datasets: [{
                    label: 'Number of Posts',
                    data: [{% for category in posts_by_category %}{{ category[1] }}{% if not loop.last %}, {% endif %}{% endfor %}],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});
