

var pie_ctx = document.getElementById('pie-chart');

var pieChart = new Chart( pie_ctx, {
    type: 'pie',
    data: {
        labels: [
            'Globe Tel...',
            'Smart Tel...',
            'PLDT Tel...',
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [
                5,
                5,
                3,
                2,
                1
            ],
            backgroundColor: [
                bublegum_gradient,
                red_gradient,
                purple_gradient,
                green_gradient,
                orange_gradient,
                blue_gradient
            ],
            label: 'My dataset', // for legend
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
    }
});