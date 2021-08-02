$(function(){
    let on_load_done = true
    let has_next = true
    let current_page = 1

    let $notification_container = $('#user-notifications')

    $(window).scroll(function () {
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10 && on_load_done) {
            on_load_done = false
            if (has_next){
                $.ajax({
                    type: "GET",
                    data: {
                        current_page : current_page,
                    },
                    success: function (data) {
                        $notification_container.append(data.html)
                        current_page = data.next_number
                        has_next = data.has_next
                        on_load_done = true
                    },
                });
            }else{
                $('#more-button').addClass('hidden')
            }
            
        }
    }); 
    
$('#more-button').click(function(){
    if (current_page > 1)
        current_page++
    $.ajax({
        type: "GET",
        data: {
            current_page : current_page,
        },
        success: function (data) {
            $notification_container.append(data.html)
            current_page = data.next_number
            has_next = data.has_next
        },
    });
})
})