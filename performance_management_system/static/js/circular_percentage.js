let options = {
    startAngle: -1.55,
    size: 150,
    fill: {gradient: ['#7474BF', '#348AC7']}
}

$(".circle .bar").circleProgress(options).on('circle-animation-progress',

function(event, progress, stepValue){
    let text = String(stepValue.toFixed(2).substr(2)) 
    if (stepValue == 1){
        text = '100'
    }
    $(this).parent().find("span").text(text + "%");
}
);