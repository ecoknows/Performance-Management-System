let options = {
    startAngle: -1.55,
    size: 150,
    fill: {gradient: ['#fc4a1a', '#f7b733']}
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