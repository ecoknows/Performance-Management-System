
$(function(){
    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#client-list-page')

    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'filter_query': filter_query,
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
            url : url,
            type: 'GET',
            data:{
                'search_query' : search_query,
                'filter_query': filter_query,
                'employee_id': employee_id,
                
            },
            success: function(data){
                container.html(data)
            }
        })


    });
})