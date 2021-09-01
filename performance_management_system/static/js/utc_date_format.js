let option = {
    month:'short', 
    day: 'numeric', 
    year: 'numeric', 
    minute:'2-digit', 
    hour: '2-digit'
}


let get_date = new Date($('#utc-date').html())
if ( get_date != 'Invalid Date'){
    let get_time = get_date.toLocaleTimeString('en-Us',option)
    $('#utc-date').html(get_time)
}