
$(function(){

    let search_input = $('#search-input')
    let url = search_input.data('url')
    let container = $('#client-list-container')
    let pages_indicator = $('#pages-indicator')
    let page = 1

    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'search_query' : search_input.val(),
            'filter_query': filter_query,
            'page': page,
        },
        success: function(data){
            pages_indicator.toggleClass('hidden')
            container.html(data.html)
            pages_indicator.html(data.pages_indicator)
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
            },
            success: function(data){
                container.html(data.html)
            }
        })


    });
})