

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



    var $chart = $("#bar-chart");
    let chart = null
    let page_number = $('#page-number-bar')
    let page_status = 1
    let next_btn = $('#next-btn-bar')
    let back_btn = $('#back-btn-bar')

    $.ajax({
      url: $chart.data("url"),
      type: 'GET',
      data: {
        'page': 1,
        'max_page': 6,
      },
      success: function (data) {

        var ctx = $chart[0].getContext('2d');

        $('#bar-chart-tbody').html(data.html_chart)

        chart = new Chart(ctx, {
            type: 'bar',
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


    next_btn.on('click', function () {
        page_status++
        $.ajax({
            url: $chart.data("url"),
            type: 'GET',
            data: {
              'page': page_status,
              'max_page': 6,
            },
            success: function (data) {
                
              if(data.has_previous){
                back_btn.show()
              }else{
                back_btn.hide()
              }

              if(data.has_next){
                next_btn.show()
              }else{
                next_btn.hide()
              }
    

              $('#bar-chart-tbody').html(data.html_chart)
              chart.data.datasets[0].data = data.data 
              chart.data.labels = data.labels
              page_number.html(page_status)
      
              chart.update();
      
      
      
            }
          });
    });

    
    back_btn.on('click', function () {
        page_status--
        $.ajax({
            url: $chart.data("url"),
            type: 'GET',
            data: {
              'page': page_status,
              'max_page': 6,
            },
            success: function (data) {

              $('#bar-chart-tbody').html(data.html_chart)
              chart.data.datasets[0].data = data.data 
              chart.data.labels = data.labels
              page_number.html(page_status)

              
              if(data.has_previous){
                back_btn.show()
              }else{
                back_btn.hide()
              }

              if(data.has_next){
                next_btn.show()
              }else{
                next_btn.hide()
              }
              
              chart.update();
      
      
      
            }
          });
    });


});