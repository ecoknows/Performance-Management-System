$(function(){
    let $search_input = $('#search-input')
    let url = $search_input.data('url')
    let $container = $('#pop-box')
    $search_input.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'search_query' : search_query,
            },
            success: function(data){
                if(!data.empty){
                    $container.html(data)
                    $container.removeClass('hidden')
                }else{
                    $container.addClass('hidden')
                }
                    
            }
        })


    });
})