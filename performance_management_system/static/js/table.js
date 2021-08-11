

$(function(){
    let url = 'search'
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    let pages_indicator = $('#pages-indicator')
    
    next_button.click(function(){
        let sort = null
        if(current_sort){
            sort = current_sort.data('field-name')
        }
        
        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'page': next_page == null ? current_page : next_page,
                'sort':sort,
            },
            success: function(data){
                container.html(data.html)
                next_page = data.next_number
                previous_page = data.previous_number
                current_page = data.current_number
                pages_indicator.html(data.pages_indicator)
                
            }
        })
    })
    
    back_button.click(function(){
        let sort = null
        if(current_sort){
            sort = current_sort.data('field-name')
        }
        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'page': previous_page == null ? null : previous_page,
                'sort':sort,
            },
            success: function(data){
                container.html(data.html)
                next_page = data.next_number
                previous_page= data.previous_number
                current_page = data.current_number
                pages_indicator.html(data.pages_indicator)
            }
        })
    })
})


function page_number_click(page_click){
    let url = 'search'
    let pages_indicator = $('#pages-indicator')
    let sort = null
    if(current_sort){
        sort = current_sort.data('field-name')
    }
    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'page': page_click,
            'sort': sort,
        },
        success: function(data){
            container.html(data.html)
            next_page = data.next_number
            previous_page = data.previous_number
            current_page = parseInt(page_click)
            pages_indicator.html(data.pages_indicator)
        }
    })
}