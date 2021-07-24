
// $(".notify").toggleClass("active");
// $("#notifyType").toggleClass("success");
// $(".notify").css({'background-color': 'rgba(9, 79, 38, 0.809)'});

// $(".notify").addClass("active");
// $("#notifyType").addClass("failure");
// $(".notify").css({'background-color': 'rgba(79, 9, 9, 0.809)'});



$(function(){
	console.log(submit_success);
	if (submit_success == 'success'){
		$(".notify").toggleClass("active");
		$("#notifyType").toggleClass("success");
		$(".notify").css({'background-color': 'rgba(9, 79, 38, 0.809)'});
		
		setTimeout(function(){
			$(".notify").removeClass("active");
			$("#notifyType").removeClass("failure");
		},2000);
		
	}
})