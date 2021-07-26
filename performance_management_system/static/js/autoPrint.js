
$(function(){


    $('#print-evaluation').click(function(){
        window.print();
        // var pdf = new jsPDF('p', 'pt', 'a4');

        // source = $('#evaluation-page')[0];

        // specialElementHandlers = {
        //     '#editor': function (element, renderer) {
        //         return true
        //     }
        // };

        // pdf.fromHTML(
        //     source, 
        //     15, 
        //     15,
        //     {
        //         'width': 170,
        //         'elementHandlers': specialElementHandlers,
        //     }
        // );

        // pdf.save('Test.pdf');


        // var quotes = document.getElementById('evaluation-page');
        // html2canvas(quotes, {
        //     onrendered: function(canvas) {
        //         canvas.getContext('2d');
        //         var HTML_Width = canvas.width;
        //         var HTML_Height = canvas.height;
        //         var top_left_margin = 15;
        //         var PDF_Width = HTML_Width+parseInt(top_left_margin*2);
        //         var PDF_Height = parseInt(PDF_Width*1.5)+parseInt(top_left_margin*2);
        //         var canvas_image_width = HTML_Width;
        //         var canvas_image_height = HTML_Height;
                
        //         var totalPDFPages = Math.ceil(HTML_Height/PDF_Height)-1;
        //         var pages = $('#generatePDF .canvas-container').length;

        //         console.log('height => '+canvas.height+" width => "+canvas.width+'totalpage => '+pages);
                
                
        //         var imgData = canvas.toDataURL("image/jpeg", 1.0);
        //         var pdf = new jsPDF('p', 'pt',  [PDF_Width, PDF_Height]);
        //         pdf.addImage(imgData, 'JPG', top_left_margin, top_left_margin,canvas_image_width,canvas_image_height);
                
        //         for (var i = 1; i <= pages; i++) {
        //             //pdf.addPage(PDF_Width, PDF_Height);
        //             pdf.addPage();
        //             let margin=-parseInt(PDF_Height*i)+parseInt(top_left_margin*4);
        //             if(i>1){
        //                 margin= parseInt(margin+i*8);
        //             }
        //             pdf.addImage(imgData, 'JPG', top_left_margin, margin,canvas_image_width,canvas_image_height);
        //         }
        //         pdf.save("HTML-Document.pdf");
        //     }
        // });


    })
})
