$(function(){

    $.ajax({
        url: '/get_recent',
        type: 'GET',
        data: {
          'page': 1,
        },
        success: function (data) {
            $('#recent_evaluations').html(data)
        }
      });


});