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

$(function(){

    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#client-list-page')

    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'filter': filter == 'None' || filter == 'All' ? null : filter,
            'user_filter': user_filter == 'None'  ? null : user_filter,
            'user_filter_exclude': user_filter_exclude == 'None'  ? null : user_filter_exclude,
        },
        success: function(data){
            container.html(data)
        }
    })
   
    search_input.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        

        
        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'search_query' : search_query,
                'filter': filter == 'None' || filter == 'All' ? null : filter,
                'user_filter': user_filter == 'None' ? null : user_filter,
                'user_filter_exclude': user_filter_exclude == 'None'  ? null : user_filter_exclude,
            },
            success: function(data){
                container.html(data)
            }
        })


    });
})