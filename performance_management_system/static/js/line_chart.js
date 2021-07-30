
$(function () {
    var $chart = $("#line-chart-quality-of-work");
    let chart = null
    let page_number = $('#page-number-quality-of-work')
    let page_status = 1
    let next_btn = $('#next-btn-quality-of-work')
    let back_btn = $('#back-btn-quality-of-work')

    $.ajax({
      url: $chart.data("url"),
      type: 'GET',
      data: {
        'page': 1,
        'max_page': 7,
      },
      success: function (data) {

        var ctx = $chart[0].getContext('2d');
        
        if (data.data != '')
          page_number.html(page_status)



        chart = new Chart( ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'My First Dataset',
                    data: data.data,
                    backgroundColor: [
                        bublegum_gradient,
                        red_gradient,
                        purple_gradient,
                        green_gradient,
                        orange_gradient,
                        blue_gradient
                    ],
                    borderColor:'#FF7A00',
                    label: 'Percentage', // for legend
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
              'max_page': 7,
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
              'max_page': 7,
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

$(function () {
    var $chart = $("#line-chart-initiative");
    let chart = null
    let page_number = $('#page-number-initiative')
    let page_status = 1
    let next_btn = $('#next-btn-initiative')
    let back_btn = $('#back-btn-initiative')

    $.ajax({
      url: $chart.data("url"),
      type: 'GET',
      data: {
        'page': 1,
        'max_page': 7,
      },
      success: function (data) {

        var ctx = $chart[0].getContext('2d');
        
        if (data.data != '')
          page_number.html(page_status)



        chart = new Chart( ctx, {
            type: 'line',
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
                    borderColor:'#00A62E',
                    label: 'Percentage', // for legend
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
              'max_page': 7,
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
              'max_page': 7,
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