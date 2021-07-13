

var color_ctx = document.getElementById('bar-chart').getContext('2d');

var bublegum_gradient = color_ctx.createLinearGradient(0, 0, 0, 300);
bublegum_gradient.addColorStop(0, '#93EDC7');
bublegum_gradient.addColorStop(1, '#1CD8D2');

var red_gradient = color_ctx.createLinearGradient(0, 0, 0, 600);
red_gradient.addColorStop(0, '#F08787');
red_gradient.addColorStop(1, '#FF3F3F');

var purple_gradient = color_ctx.createLinearGradient(0, 0, 0, 600);
purple_gradient.addColorStop(0, '#AD86FF');
purple_gradient.addColorStop(1, '#7C3FFF');

var green_gradient = color_ctx.createLinearGradient(0, 0, 0, 600);
green_gradient.addColorStop(0, '#7DDB97');
green_gradient.addColorStop(1, '#00A62E');

var orange_gradient = color_ctx.createLinearGradient(0, 0, 0, 600);
orange_gradient.addColorStop(0, '#FFB9A3');
orange_gradient.addColorStop(1, '#EE3900');

var blue_gradient = color_ctx.createLinearGradient(0, 0, 0, 600);
blue_gradient.addColorStop(0, '#B3B1F4');
blue_gradient.addColorStop(1, '#0500EF');



$(function () {

    var $barChart = $("#bar-chart");


    $.ajax({
      url: $barChart.data("url"),
      type: 'GET',
      data: {
        'page': 3
      },
      success: function (data) {

        var ctx = $barChart[0].getContext('2d');

        $('#bar-chart-tbody').html(data.html_chart)

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: '# of Votes',
                    data: data.data,
                    backgroundColor: [
                        bublegum_gradient,
                        red_gradient,
                        purple_gradient,
                        green_gradient,
                        orange_gradient,
                    ]   
                }]
            },
            options: {
                responsive: true,
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




      }
    });

  });