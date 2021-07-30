$(function(){
    $( ".infinite-chart" ).each(function() {
        let infinite_chart = $(this)
        let canvas = infinite_chart.find('#chart')
        let table = infinite_chart.find('#chart-tbody')
        let page_number = infinite_chart.find('#page-number')
        let page_status = 1
        let ctx = canvas[0].getContext('2d');
        let next_btn = infinite_chart.find('#next-btn')
        let back_btn = infinite_chart.find('#back-btn')


        $.ajax({
            url: canvas.data("url"),
            type: 'GET',
            data: {
              'page': 1,
              'max_page': 4,
            },
            success: function (data) {
            table.html(data.html_chart)
            
            if (data.data != '')
              page_number.html(page_status)
    
            
            chart = new Chart( ctx, {
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
                        label: 'Percentage', // for legend
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
            url: canvas.data("url"),
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
    

              table.html(data.html_chart)
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
            url: canvas.data("url"),
            type: 'GET',
            data: {
              'page': page_status,
              'max_page': 4,
            },
            success: function (data) {

              table.html(data.html_chart)
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


})