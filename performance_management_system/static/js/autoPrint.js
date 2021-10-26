
$(function(){
    function CreatePDFfromHTML() {
        $("#evaluation-page").css({"zoom": 0.7}); 
        var HTML_Width = $("#evaluation-page").width();
        var HTML_Height = $("#evaluation-page").height();
        var top_left_margin = 15;
        var PDF_Width = HTML_Width + (top_left_margin * 2);
        var PDF_Height = (PDF_Width * 1.5) + (top_left_margin * 2);
        var canvas_image_width = HTML_Width;
        var canvas_image_height = HTML_Height;
    
        var totalPDFPages = Math.ceil(HTML_Height / PDF_Height) - 1;
        $('.show-on-print').toggle();    
        $('#print-evaluation').css({'display': 'none'});    
        html2canvas($("#evaluation-page")[0],  {width: HTML_Width, height: HTML_Height}).then(function (canvas) {
            var imgData = canvas.toDataURL("image/jpeg", 2.0);
            var pdf = new jsPDF('p', 'pt', [PDF_Width, PDF_Height]);
            pdf.addImage(imgData, 'JPG', top_left_margin, top_left_margin, canvas_image_width, canvas_image_height);
            for (var i = 1; i <= totalPDFPages; i++) { 
                pdf.addPage(PDF_Width, PDF_Height);
                pdf.addImage(imgData, 'JPG', top_left_margin, -(PDF_Height*i)+(top_left_margin*4),canvas_image_width,canvas_image_height);
            }
            pdf.save("Report.pdf");
            $("#evaluation-page").css({"zoom":1}); 
        });
        console.log(HTML_Width, HTML_Height);
        $('.show-on-print').toggle();    
        $('#print-evaluation').css({'display': 'flex'});    
    }

    $('#print-evaluation').click(function(){
        CreatePDFfromHTML();
    })
})
