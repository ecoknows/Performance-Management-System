$(function(){
    $('.notify-button').click(function(){
        let client_id = $(this).data('client_id')
        let user_evaluation_id = $(this).data('user_evaluation_id')

        $.ajax({
            type:'POST',
            data:{
                'client_id': client_id,
                'user_evaluation_id': user_evaluation_id,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(data){
                console.log(data.message);
            }
        })
    })
})