


$(function () {
    var $chart = $("#radar-chart");
    let chart = null
    let page_number = $('#page-number-radar')
    let page_status = 1
    let next_btn = $('#next-btn-radar')
    let back_btn = $('#back-btn-radar')

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


        chart = new Chart( ctx, {
            type: 'radar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Performance',
                    data: data.data,
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
            },
            success: function (data) {

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