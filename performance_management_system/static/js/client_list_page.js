
function notify_client(client_id){

    $.ajax({
        type:'POST',
        data:{
            'client_id': client_id,
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function(data){
            $(".notify").toggleClass("active");
            $("#notifyType").toggleClass("notify-successfull");
            $(".notify").css({'background-color': 'rgba(9, 79, 38, 0.809)'});
            
            setTimeout(function(){
                $(".notify").removeClass("active");
                $("#notifyType").removeClass("notify-successfull");
            },2000);
        }
    })

}