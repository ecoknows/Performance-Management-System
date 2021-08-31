
$(function(){

    let pages_indicator = $('#pages-indicator')
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    
    let name = $('#search-input-name')
    let message = $('#search-input-message')
    let time = $('#search-input-time')
    let status = $('#search-input-status')
    let sort = $('.fa-sort')

    sort.click(function(){
        let latest_sort = $(this)
        let field_name = latest_sort.data('field-name')
       
        
        if(current_sort){
            current_sort.removeClass('sort-active')

            if(latest_sort.data('field-name') == current_sort.data('field-name')){
                
                $.ajax({
                    url : table_url,
                    type: 'GET',
                    data:{
                        'name' : name.val(),
                        'message': message.val(),
                        'time': time.val(),
                        'status': status.val(),
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    },
                    success: function(data){
                        container.html(data.html)
                    }
                })
                current_sort = null
    
                return
            }
        }

        
        latest_sort.addClass('sort-active')
        current_sort = latest_sort

        $.ajax({
            url : table_url,
            type: 'GET',
            data:{
                'name' : name.val(),
                'message': message.val(),
                'time': time.val(),
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


    $.ajax({
        url : table_url,
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
   
    name.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()
        
        if(search_query == ''){
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'message': message.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val() : null,
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                }
            })
        }else{
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'name' : search_query,
                    'message': message.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }


    });

    message.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()
        if(search_query == ''){
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'message': message.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                }
            })
        }else{
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'message' : search_query,
                    'name': name.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }


    });

    
    time.keyup(function(e){
        e.preventDefault();
        let search_query = $(this).val()

        if(search_query == ''){
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'message': message.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                }
            })
        }else{
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'time' : search_query,
                    'name': name.val(),
                    'message': message.val(),
                    'status': status.val(),
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
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
                url : table_url,
                type: 'GET',
                data:{
                    'name' : name.val(),
                    'message': message.val(),
                    'time': time.val(),
                    'status': status.val(),
                    'sort': current_sort ? current_sort.val(): null,
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                    'page': current_page,
                },
                success: function(data){
                    container.html(data.html)
                }
            })
        }else{
            $.ajax({
                url : table_url,
                type: 'GET',
                data:{
                    'status' : search_query,
                    'time' : time.val(),
                    'name': name.val(),
                    'message': message.val(),
                    'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    
                },
                success: function(data){
                    container.html(data.html)
                    pages_indicator.html(data.pages_indicator)
                }
            })
        }

    })
})