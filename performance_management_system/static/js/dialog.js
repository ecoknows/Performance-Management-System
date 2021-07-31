
let dialog = $('#dialog_id')
let current_client_pk = null


function dialog_button_trigger(client){
    dialog.css('display','block')
    let src = $(client).find('#client-profile-pic').attr('src')
    let name = $(client).find('#client-name').html()

    current_client_pk = $(client).data('client-pk')

    $('#client-pic-dialog').attr('src', src)
    $('#client-name-dialog').html(name)
}

function close_dialog(){
    dialog.css('display','none')
}

function refresh_clients(){

    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#pick-client-container')

    $.ajax({
        url : url + '/pick_client',
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'employee_id': employee_id,
        },
        success: function(data){
            container.html(data)
        }
    })

    search_input.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        $.ajax({
            url : url  + '/pick_client',
            type: 'GET',
            data:{
                'search_query' : search_query,
                'employee_id': employee_id,
            },
            success: function(data){
                container.html(data)
            }
        })


    });
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
