
$(function(){
    $('.anchor-clickable').click(function(){
        let user_evaluation_id = $(this).data('user_evaluation')
        let notification_id = $(this).data('notification-pk')
        let this_button = $(this)
        $.ajax({
            type: 'GET',
            data:{
                'user_evaluation_id' : user_evaluation_id,
                'notification_id': notification_id,
            },
            success: function (data) {
                $('#notification-selected').html(data.selected_html)
                $('#notification-container').html(data.notification_html)
                this_button.addClass('shadow-box').removeClass('shadow-box-yellow')
            }
        });
    })
    $.ajax({
        type: 'GET',
        data:{
            'user_evaluation_id' : user_evaluation_first_id,
        },
        success: function (data) {
            $('#notification-selected').html(data.selected_html)
        }
    });
})