
$(function(){

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
})