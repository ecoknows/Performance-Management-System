
var ctx = document.getElementById('myChart').getContext('2d');

var bublegum_gradient = ctx.createLinearGradient(0, 0, 0, 600);
bublegum_gradient.addColorStop(0, '#93EDC7');
bublegum_gradient.addColorStop(1, '#1CD8D2');

var red_gradient = ctx.createLinearGradient(0, 0, 0, 600);
red_gradient.addColorStop(0, '#F08787');
red_gradient.addColorStop(1, '#FF3F3F');

var purple_gradient = ctx.createLinearGradient(0, 0, 0, 600);
purple_gradient.addColorStop(0, '#AD86FF');
purple_gradient.addColorStop(1, '#7C3FFF');

var green_gradient = ctx.createLinearGradient(0, 0, 0, 600);
green_gradient.addColorStop(0, '#7DDB97');
green_gradient.addColorStop(1, '#00A62E');

var orange_gradient = ctx.createLinearGradient(0, 0, 0, 600);
orange_gradient.addColorStop(0, '#FFB9A3');
orange_gradient.addColorStop(1, '#EE3900');

var blue_gradient = ctx.createLinearGradient(0, 0, 0, 600);
blue_gradient.addColorStop(0, '#B3B1F4');
blue_gradient.addColorStop(1, '#0500EF');




var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [5, 4, 2, 3 , 1, 1],
            backgroundColor: [
                bublegum_gradient,
                red_gradient,
                purple_gradient,
                green_gradient,
                orange_gradient,
                blue_gradient
            ]   
        }]
    },
    options: {
        plugins: {
            legend: {
              display: false
            }
        },
        scales: {
            y: {
                ticks :{
                    display: false
                }
            },
            x: {
                display:false
            },
        }
    }
});