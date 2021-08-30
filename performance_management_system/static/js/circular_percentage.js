let options = {
    startAngle: -1.55,
    size: 110,
    fill: {gradient: ['#7474BF', '#348AC7']}
}

$(".circle .bar").circleProgress(options).on('circle-animation-progress',

function(event, progress, stepValue){
    stepValue = stepValue * max_rate
    let text = String(stepValue.toFixed(2)) 
    $(this).parent().find("span").text(text );
}
);


$(".circle .bar").circleProgress(options).on('circle-animation-end',

    function(event){
        let stepValue = parseFloat($(this).data('value'));
        stepValue = stepValue * max_rate
        let text = ''
        switch(parseInt(stepValue)){
            case 5:
                text = 'OUTSTANDING'
                break;
            case 4:
                text='PROFICIENT'
                break;
            case 3:
                text='MARGINAL'
                break;
            case 2:
                text='NEEDS IMPROVEMENT'
                break;
            case 1:
                text='FAILED'
            case 0:
                text='FAILED'
                break;

        }

        $(this).parent().find("span").append(
            `
                <p class='text-xs font-sans' >
            `+text+
            '</p>'
        );
    }
);