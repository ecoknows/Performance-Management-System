
$(function(){

    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#employee-list-page')

    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'filter': filter == 'None' ? null : filter
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
                'filter': filter == 'None' ? null : filter
            },
            success: function(data){
                container.html(data)
            }
        })


    });
})