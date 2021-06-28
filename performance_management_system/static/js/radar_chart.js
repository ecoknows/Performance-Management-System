

var radar_ctx = document.getElementById('radar-chart');



var radarChart = new Chart( radar_ctx, {
    type: 'radar',
    data: {
        labels: [
            'Globe Tel...',
            'Smart Tel...',
            'PLDT Tel...',
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [4, 5, 3,],
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'transparent',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'    
        }]
    },
    options: {
        responsive: true,
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
        },
    }
});