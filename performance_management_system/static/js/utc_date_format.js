
console.log(Intl.DateTimeFormat().resolvedOptions().timeZone);
// $( ".utc-to-convert" ).each(function() {
//     let get_utc = $(this).html()
//     let convert_to_local_timezone = new Date(get_utc)
//     let formatted_date = 
//     '( '+
//     convert_to_local_timezone
//         .toLocaleTimeString('en-US', 
//         { 
//         hour: '2-digit',
//         minute: '2-digit', 
//         })
//     +
//         ' of ' 
//     + 
//     convert_to_local_timezone
//         .toLocaleDateString('en-US',
//         { 
//         month: 'short',
//         day: 'numeric' 
//         })
//     +
//     ' )'



//     $( this ).html(formatted_date)
// });