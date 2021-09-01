
$(function(){

    let url = 'search/clients/'
    let pages_indicator = $('#pages-indicator')
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    
    let name = $('#search-input-name')
    let address = $('#search-input-address')
    let contact_number = $('#search-input-contact-number')
    let status = $('#search-input-status')
    let sort = $('.fa-sort')


    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'page': current_page,
        },
        success: function(data){
            $('#container-page-indicator').removeClass('hidden')
            container.html(data.html)
            next_page = data.next_number
            back_button.removeClass('hidden')
            next_button.removeClass('hidden')
            pages_indicator.html(data.pages_indicator)
        }
    })

    sort.click(function(){
        let latest_sort = $(this)
        let field_name = latest_sort.data('field-name')
       
        
        if(current_sort){
            current_sort.removeClass('sort-active')

            if(latest_sort.data('field-name') == current_sort.data('field-name')){
                
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        'name' : name.val(),
                        'address': address.val(),
                        'contact_number': contact_number.val(),
                        'status': status.val(),
                        
                    },
                    success: function(data){
                        container.html(data.html)
                        pages_indicator.html(data.pages_indicator)
                    }
                })
                current_sort = null
    
                return
            }
        }

        
        latest_sort.addClass('sort-active')
        current_sort = latest_sort

        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'name' : name.val(),
                'address': address.val(),
                'contact_number': contact_number.val(),
                'status': status.val(),
                'sort': field_name,
                
            },
            success: function(data){
                container.html(data.html)
                pages_indicator.html(data.pages_indicator)
            }
        })


    })

   
    name.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()
        
        if(search_query == ''){
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'address': address.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val() : null,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }else{
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'name' : search_query,
                    'address': address.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }


    });

    address.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        if(search_query == ''){
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'address': address.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }else{
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'address' : search_query,
                    'name': name.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }


    });

    
    contact_number.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        if(search_query == ''){
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'address': address.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }else{
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'contact_number' : search_query,
                    'name': name.val(),
                    'address': address.val(),
                    'status': status.val(),
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }


    });

    status.change(function(){
        let search_query = $(this).val();

        if(search_query == 'All'){
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'address': address.val(),
                    'contact_number': contact_number.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }else{
            $.ajax({
                url : url,
                type: 'GET',
                data:{
                    'status' : search_query,
                    'contact_number' : contact_number.val(),
                    'name': name.val(),
                    'address': address.val(),
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }

    })
})