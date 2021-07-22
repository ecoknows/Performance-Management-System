
$(function(){
    $('.anchor-clickable').click(function(){
        let notification_id = $(this).data('notification-pk')
        let hr_admin_id = $(this).data('hr_admin_id')
        let this_button = $(this)
        $.ajax({
            type: 'GET',
            data:{
                'notification_id': notification_id,
                'make_it_seen': true,
                'hr_admin_id' : hr_admin_id,
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
            'notification_id': notification_first_id,
            'hr_admin_id' : hr_admin_first_id,
        },
        success: function (data) {
            $('#notification-selected').html(data.selected_html)
        }
    });
})