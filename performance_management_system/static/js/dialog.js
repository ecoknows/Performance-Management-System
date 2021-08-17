
let dialog = $('#dialog_id')
let current_client_pk = null


function dialog_button_trigger(client){
    dialog.css('display','block')
    let src = $(client).parent().parent().find('#client-profile-pic').attr('src')
    let name = $(client).parent().parent().find('#client-name').html()

    current_client_pk = $(client).data('client-pk')

    $('#client-pic-dialog').attr('src', src)
    $('#client-name-dialog').html(name)
}

function close_dialog(){
    dialog.css('display','none')
}

function refresh_clients(){

    let pages_indicator = $('#pages-indicator')

    $.ajax({
        url : 'search/clients/',
        type: 'GET',
        data:{
            'page': current_page,
        },
        success: function(data){
            $('#container-page-indicator').removeClass('hidden')
            container.html(data.html)
            next_page = data.next_number
            pages_indicator.html(data.pages_indicator)
        }
    })
}

function check_project_assign(){
    

    if($('#dialog-text-area').val().trim().length > 0){
        project_assign = $('#dialog-text-area');

        $.ajax({
            url: 'add/',
            type: 'POST',
            data:{
                'client_id': current_client_pk,
                'project_assign': project_assign.val(),
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(data){
                if(data.message == 'Successfull'){
                    refresh_clients()
                    dialog.css('display','none')
                    project_assign.val('')
                }
            }
        })

        current_client_pk = null

        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("assign-successfull");
        $(".notify").css({'background-color': 'rgba(9, 79, 38, 0.809)'});
        
        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("assign-successfull");
        },2000);

    }else{
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("fill-project-assign");
        $(".notify").css({'background-color': 'rgba(79, 9, 9, 0.809)'});
        
        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("fill-project-assign");
        },2000);
    }
    
}
