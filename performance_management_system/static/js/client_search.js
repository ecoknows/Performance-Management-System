
$(function(){

    let url = 'search'
    let container = $('#client-list-container')
    let pages_indicator = $('#pages-indicator')
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    
    let name = $('#search-input-name')
    let address = $('#search-input-address')
    let contact_number = $('#search-input-contact-number')
    let status = $('#search-input-status')
    let sort = $('.fa-sort')
    let previous_sort = null

    sort.click(function(){
        let current_sort = $(this)
        let field_name = current_sort.data('field-name')
       
        
        if(previous_sort){
            previous_sort.removeClass('sort-active')

            if(current_sort.data('field-name') == previous_sort.data('field-name')){
                
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        'name' : name.val(),
                        'address': address.val(),
                        'contact_number': contact_number.val(),
                        'status': status.val(),
                        'filter_query': filter_query,
                    },
                    success: function(data){
                        container.html(data.html)
                    }
                })
                previous_sort= null
    
                return
            }
        }

        
        current_sort.addClass('sort-active')
        previous_sort = current_sort

        $.ajax({
            url : url,
            type: 'GET',
            data:{
                'name' : name.val(),
                'address': address.val(),
                'contact_number': contact_number.val(),
                'status': status.val(),
                'sort': field_name,
                'filter_query': filter_query,
            },
            success: function(data){
                container.html(data.html)
                pages_indicator.html(data.pages_indicator)
            }
        })


    })


    $.ajax({
        url : url,
        type: 'GET',
        data:{
            'filter_query': filter_query,
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
                    'sort': previous_sort ? previous_sort.val() : null,
                    'filter_query': filter_query,
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
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
                    'filter_query': filter_query,
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
                    'sort': previous_sort ? previous_sort.val(): null,
                    'filter_query': filter_query,
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
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
                    'filter_query': filter_query,
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
                    'sort': previous_sort ? previous_sort.val(): null,
                    'filter_query': filter_query,
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
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
                    'filter_query': filter_query,
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
                    'sort': previous_sort ? previous_sort.val(): null,
                    'filter_query': filter_query,
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
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
                    'filter_query': filter_query,
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }

    })
})