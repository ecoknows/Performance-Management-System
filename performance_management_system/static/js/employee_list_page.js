
$(function(){

    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#employee-list-container')
    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'filter_query': filter_query,
            'user_filter': user_filter == 'None' ? null : user_filter,
            'user_filter_exclude':  user_filter_exclude == 'None' ? null : user_filter_exclude,
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
                'filter_query': filter_query,
                'user_filter': user_filter == 'None' ? null : user_filter,
                'user_filter_exclude':  user_filter_exclude == 'None' ? null : user_filter_exclude,
            },
            success: function(data){
                container.html(data)
            }
        })


    });
})