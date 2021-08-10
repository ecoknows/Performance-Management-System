

$(function(){
    let url = 'search'
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    let container = $('#client-list-container')
    let pages_indicator = $('#pages-indicator')
    
    next_button.click(function(){
        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'page': next_page == null ? current_page : next_page,
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
        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'page': previous_page == null ? null : previous_page,
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
    let container = $('#client-list-container')
    let pages_indicator = $('#pages-indicator')
    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'page': page_click,
        },
        success: function(data){
            container.html(data.html)
            next_number = data.next_number
            previous_number = data.previous_number
            current_page = page_click
            pages_indicator.html(data.pages_indicator)
        }
    })
}