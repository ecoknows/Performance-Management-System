


$(function () {
    var $chart = $("#pie-chart");
    let chart = null
    let page_number = $('#page-number-pie')
    let page_status = 1
    let next_btn = $('#next-btn-pie')
    let back_btn = $('#back-btn-pie')

    $.ajax({
      url: $chart.data("url"),
      type: 'GET',
      data: {
        'page': 1,
        'max_page': 4,
        '2x2': true,
      },
      success: function (data) {

        var ctx = $chart[0].getContext('2d');

        $('#pie-chart-tbody').html(data.html_chart)

        chart = new Chart( ctx, {
            type: 'pie',
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


    next_btn.on('click', function () {
        page_status++
        $.ajax({
            url: $chart.data("url"),
            type: 'GET',
            data: {
              'page': page_status,
              'max_page': 4,
              '2x2': true,
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
    

              $('#pie-chart-tbody').html(data.html_chart)
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
              'max_page': 4,
              '2x2': true,
            },
            success: function (data) {

              $('#pie-chart-tbody').html(data.html_chart)
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