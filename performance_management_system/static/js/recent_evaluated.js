
$(function(){

  let next_btn = $('#recent-next')
  let back_btn = $('#recent-back')
  let page_number = $('#page-number-recent')
  let page_status = 1

  $.ajax({
    url: '/get_recent',
    type: 'GET',
    data: {
      'page': page_status,
    },
    success: function (data) {
        $('#recent_evaluations').html(data.html)
        $('#button-container').show()
        if(data.has_next){
          next_btn.show()
        }else{
          next_btn.hide()
        }
        if(data.has_previous){
          back_btn.show()
        }else{
          back_btn.hide()
        }
    }
  });
  

  next_btn.on('click', function () {
    console.log('eco');
    page_status++
    
    $.ajax({
      url: '/get_recent',
      type: 'GET',
      data: {
        'page': page_status,
      },
      success: function (data) {
          $('#recent_evaluations').html(data.html)
          page_number.html(page_status)
          if(data.has_next){
            next_btn.show()
          }else{
            next_btn.hide()
          }
          if(data.has_previous){
            back_btn.show()
          }else{
            back_btn.hide()
          }
      }
    });

  })

  back_btn.on('click', function () {
    page_status--

    $.ajax({
      url: '/get_recent',
      type: 'GET',
      data: {
        'page': page_status,
      },
      success: function (data) {
          $('#recent_evaluations').html(data.html)
          page_number.html(page_status)
          if(data.has_next){
            next_btn.show()
          }else{
            next_btn.hide()
          }
          if(data.has_previous){
            back_btn.show()
          }else{
            back_btn.hide()
          }
          
      }
    });
  })
    


});