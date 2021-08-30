$(function(){
	if (submit_success == 'success'){
		$(".notify").toggleClass("active");
		$("#notifyType").toggleClass(success_text);
		$(".notify").css({'background-color': 'rgba(9, 79, 38)'});
		
		setTimeout(function(){
			$(".notify").removeClass("active");
		},2000);
		
	} else if (submit_success == 'failure'){
		$(".notify").toggleClass("active");

		$("#notifyType").toggleClass(failure_text);
		$(".notify").css({'background-color': '#a20000'});
		
		setTimeout(function(){
			$(".notify").removeClass("active");
		},2000);

	}
})