
let old_button = undefined

function anchor_clickable(anchor){
    let notification_id = $(anchor).data('notification-pk')
    let hr_admin_id = $(anchor).data('hr_admin_id')
    let this_button = $(anchor)
    $.ajax({
        type: 'GET',
        data:{
            'notification_id': notification_id,
        },
        success: function (data) {
            $('#notification-selected').html(data.selected_html)
            $('#notification-container').html(data.notification_html)



            old_button= this_button
        }
    });
}

})