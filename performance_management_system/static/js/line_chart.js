var line_quality_of_work_ctx = document.getElementById('line-chart-quality-of-work');

var lineChart = new Chart( line_quality_of_work_ctx, {
    type: 'line',
    data: {
        labels: [
            'Globe Tel...',
            'Smart Tel...',
            'PLDT Tel...',
            'Converge...',
            'Red Rail...',
            'Astorm...',
            'Astorm...',
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [
                5,
                5,
                3,
                2,
                3,
                1,
                5,
            ],
            backgroundColor: [
                bublegum_gradient,
                red_gradient,
                purple_gradient,
                green_gradient,
                orange_gradient,
                blue_gradient
            ],
            borderColor:'#FF7A00',
            label: 'My dataset', // for legend
            tension: 0.1,
            pointRadius: 6,
            pointHoverRadius: 6
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
        },
        scales: {
            y: {
                display: false
            },
            x: {
                display:false
            },
        }
    }
});

var line_initiative_ctx = document.getElementById('line-chart-initiative');

var lineChart = new Chart( line_initiative_ctx, {
    type: 'line',
    data: {
        labels: [
            'Globe Tel...',
            'Smart Tel...',
            'PLDT Tel...',
            'Converge...',
            'Red Rail...',
            'Astorm...',
            'Astorm...',
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [
                5,
                5,
                3,
                2,
                3,
                1,
                5,
            ],
            backgroundColor: [
                bublegum_gradient,
                red_gradient,
                purple_gradient,
                green_gradient,
                orange_gradient,
                blue_gradient
            ],
            borderColor:'#00A62E',
            label: 'My dataset', // for legend
            tension: 0.1,
            pointRadius: 6,
            pointHoverRadius: 6
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
        },
        scales: {
            y: {
                display: false
            },
            x: {
                display:false
            },
        }
    }
});