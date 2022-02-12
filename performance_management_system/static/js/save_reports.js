function save_report(){
    let url = 'save/'

    let employee = $('#search-input-employee');
    let client = $('#search-input-client');
    let project_assign = $('#search-input-project-assign');
    let performance = $('#search-input-performance');
    let date = $('#search-input-date');
    
    let elements_value = {
        'employee': employee.val(),
        'client': client.val(),
        'project_assign': project_assign.val(),
        'performance': performance.val(),
        'date': date.val(),
    }
    
    $.ajax({
        url: url,
        type:'GET',
        data:{
            ...elements_value,
        },
        success: function(data){

            var filename = Date.now().toString();
            var blob = new Blob([data], { type: "application/octetstream" });

            var isIE = false || !!document.documentMode;
            
            if (isIE) {
                window.navigator.msSaveBlob(blob, filename);
            } else {
                var url = window.URL || window.webkitURL;
                link = url.createObjectURL(blob);
                var a = $("<a />");
                a.attr("download", filename +'.json');
                a.attr("href", link);
                $("body").append(a);
                a[0].click();
                $("body").remove(a);
            }
            
        }
    })
    

}