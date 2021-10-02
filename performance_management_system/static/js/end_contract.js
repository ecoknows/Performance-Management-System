
function end_contract(employee_id, button){

    let get_notif_text = $(button).parent().find('.notification_text')

    $.ajax({
        type:'POST',
        data:{
            'employee_id': employee_id,
            'action': 'end_contract',
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function(data){
            refresh_table();
        }
    })

}


function refresh_table(){
    let url = 'search/employees/'
    let pages_indicator = $('#pages-indicator')
    let back_button = $('#back-button')
    let next_button = $('#next-button')

    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'page': current_page,
            'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
        },
        success: function(data){
            $('#container-page-indicator').removeClass('hidden')
            container.html(data.html)
            next_page = data.next_number
            back_button.removeClass('hidden')
            next_button.removeClass('hidden')
            pages_indicator.html(data.pages_indicator)
        }
    })

}