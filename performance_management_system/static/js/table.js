

$(function(){
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    let pages_indicator = $('#pages-indicator')
    
    let name = $('#search-input-name')
    let address = $('#search-input-address')
    let position = $('#search-input-position')
    let contact_number = $('#search-input-contact-number')
    let status = $('#search-input-status')
    
    next_button.click(function(){
        let sort = null
        if(current_sort){
            sort = current_sort.data('field-name')
        }
        
        $.ajax({
            url : table_url,
            type: 'GET',
            data:{
                'page': next_page == null ? current_page : next_page,
                
                'name' : name.val(),
                'address': address.val(),
                'position': position.val(),
                'contact_number': contact_number.val(),
                'status': status.val(),
                'sort': sort,

                'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
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
            url : table_url,
            type: 'GET',
            data:{
                'page': previous_page == null ? null : previous_page,
                'name' : name.val(),
                'address': address.val(),
                'position': position.val(),
                'contact_number': contact_number.val(),
                'status': status.val(),
                'sort': sort,

                'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
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
    let pages_indicator = $('#pages-indicator')
    let name = $('#search-input-name')
    let address = $('#search-input-address')
    let position = $('#search-input-position')
    let contact_number = $('#search-input-contact-number')
    let status = $('#search-input-status')
    let sort = null
    if(current_sort){
        sort = current_sort.data('field-name')
    }
    

    $.ajax({
        url : table_url,
        type: 'GET',
        data:{
            'page': page_click,
            'name' : name.val(),
            'address': address.val(),
            'position': position.val(),
            'contact_number': contact_number.val(),
            'status': status.val(),
            'sort': sort,

            'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
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