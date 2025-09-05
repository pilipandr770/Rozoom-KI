/**
 * Admin dashboard chart initialization
 * Uses the chart data embedded in the HTML in a hidden div
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get chart data from hidden div
    try {
        const chartData = JSON.parse(document.getElementById('chart-data').textContent);
        
        // Publication status chart
        const statusCtx = document.getElementById('publishStatusChart')?.getContext('2d');
        if (statusCtx) {
            new Chart(statusCtx, {
                type: 'pie',
                data: {
                    labels: ['Published', 'Draft'],
                    datasets: [{
                        data: [chartData.publishedPosts, chartData.draftPosts],
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
        if (categoryCtx && chartData.categoryLabels && chartData.categoryData) {
            new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: chartData.categoryLabels,
                    datasets: [{
                        label: 'Number of Posts',
                        data: chartData.categoryData,
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
    } catch (error) {
        console.error('Error initializing dashboard charts:', error);
    }
});
