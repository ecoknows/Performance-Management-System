
function notify_both(user_evaluation_id, button){

    let get_notif_text = $(button).parent().find('.notification_text')

    $.ajax({
        type:'POST',
        data:{
            'user_evaluation_id': user_evaluation_id,
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function(data){
            $(".notify").toggleClass("active");
            $("#notifyType").toggleClass("notify-successfull");
            $(".notify").css({'background-color': 'rgba(9, 79, 38)'});
            let created_at = new Date(data.created_at)
            let option = {
                month: 'short',
                year: 'numeric',
                day: 'numeric',
            }
            $(get_notif_text).html('Last notified '+ created_at.toLocaleDateString('en-Us', option) )
            
            setTimeout(function(){
                $(".notify").removeClass("active");
                $("#notifyType").removeClass("notify-successfull");
            },2000);
        }
    })

}