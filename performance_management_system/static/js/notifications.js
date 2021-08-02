
let old_button = undefined

function anchor_clickable(anchor){
    let notification_id = $(anchor).data('notification-pk')
    let hr_admin_id = $(anchor).data('hr_admin_id')
    let this_button = $(anchor)
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
            if (old_button){
                old_button.removeClass('border-box-blue')
            }
            this_button.addClass('border-box-blue')
            old_button= this_button
        }
    });
}


$(function(){
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