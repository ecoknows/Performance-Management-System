$(function(){
    $( ".infinite-chart" ).each(function() {
        var ctx = $(this)[0].getContext('2d');

        $.ajax({
            url: $(this).data("url"),
            type: 'GET',
            data: {
              'page': 1,
              'max_page': 4,
            },
            success: function (data) {
                
            
            new Chart( ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Performance',
                        data: data.data,
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
      
            }
          });
      
    });


})