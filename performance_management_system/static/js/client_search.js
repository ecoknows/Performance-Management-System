
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
            'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
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
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                        
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
                'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                
            },
            success: function(data){
                container.html(data.html)
                pages_indicator.html(data.pages_indicator)
            }
        })


    })

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
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
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
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }

    })

    function key_up_func(element){
        
        element.keyup(function(e){
            e.preventDefault();
            let search_query = $(this).val()

            let elements_value = {
                'name' : name.val(),
                'address': address.val(),
                'contact_number': contact_number.val(),
                'status': status.val(),
                'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,

                'sort': current_sort ? current_sort.val(): null,
                'page': current_page,
            }
            
            if(search_query == ''){
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        ...elements_value,
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                        
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
                        ...elements_value,
                    },
                    success: function(data){
                        container.html(data.html)
                        pages_indicator.html(data.pages_indicator)
                    }
                })
            }


        });

    }

    key_up_func(name);
    key_up_func(contact_number);
    key_up_func(address);

})