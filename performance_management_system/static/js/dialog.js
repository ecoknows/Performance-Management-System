
let dialog = $('#dialog_id')


function dialog_button_trigger(client){
    dialog.css('display','block')
    let src = $(client).parent().parent().find('#client-profile-pic').attr('src')
    let name = $(client).parent().parent().find('#client-name').html()
    let client_id = $(client).data('client-pk')

    $('#client_id').val(client_id)

    $('#client-pic-dialog').attr('src', src)
    $('#client-name-dialog').html(name)
}

function close_dialog(){
    dialog.css('display','none')
}
