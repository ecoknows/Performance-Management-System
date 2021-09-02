
$(function(){
    let url = 'search/evaluations/'
    let pages_indicator = $('#pages-indicator')
    let back_button = $('#back-button')
    let next_button = $('#next-button')
    
    let employee = $('#search-input-employee')
    let client = $('#search-input-client')
    let project_assign = $('#search-input-project-assign')
    let performance = $('#search-input-performance')
    let date = $('#search-input-date')


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
        
        let elements_value = {
            'employee': employee.val(),
            'client': client.val(),
            'project_assign': project_assign.val(),
            'performance': performance.val(),
            'date': date.val(),
        }
        
        if(current_sort){
            current_sort.removeClass('sort-active')

            if(latest_sort.data('field-name') == current_sort.data('field-name')){
                
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        ...elements_value,
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    },
                    success: function(data){
                        container.html(data.html)
                        pages_indicator.html(data.pages_indicator)
                    }
                })
                current_sort= null
    
                return
            }
        }

        
        latest_sort.addClass('sort-active')
        current_sort = latest_sort


        $.ajax({
            url : url,
            type: 'GET',
            data:{
                ...elements_value,
                'sort': field_name,
                'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
            },
            success: function(data){
                container.html(data.html)
                pages_indicator.html(data.pages_indicator)
            }
        })


    })

    function key_up_func(element){
        element.keyup(function(e){
            e.preventDefault();
            let search_query = $(this).val()

            let elements_value = {
                'employee': employee.val(),
                'client': client.val(),
                'project_assign': project_assign.val(),
                'performance': performance.val(),
                'date': date.val(),
            }
            
            if(search_query == ''){
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        ...elements_value,
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
                        ...elements_value,
                        'sort': current_sort ? current_sort.val(): null,
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    },
                    success: function(data){
                        container.html(data.html)
                        pages_indicator.html(data.pages_indicator)
                    }
                })
            }
        });
    }

    function change_func(element){
        element.change(function(){
            let search_query = $(this).val();
            let elements_value = {
                'employee': employee.val(),
                'client': client.val(),
                'project_assign': project_assign.val(),
                'performance': performance.val(),
                'date': date.val(),
            }
            
    
            if(search_query == 'All'){
                $.ajax({
                    url : url,
                    type: 'GET',
                    data:{
                        ...elements_value,
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
                        ...elements_value,
                        'sort': current_sort ? current_sort.val(): null,
                        'timezone': Intl.DateTimeFormat().resolvedOptions().timeZone,
                    },
                    success: function(data){
                        container.html(data.html)
                        pages_indicator.html(data.pages_indicator)
                    }
                })
            }
    
        })

    }

    key_up_func(employee);
    key_up_func(client);
    key_up_func(project_assign);
    key_up_func(date);

    change_func(performance);


})