let option = {
    month:'short', 
    day: 'numeric', 
    year: 'numeric', 
    minute:'2-digit', 
    hour: '2-digit'
}


let get_time = new Date($('#utc-date').html()).toLocaleTimeString('en-Us',option)
$('#utc-date').html(get_time)