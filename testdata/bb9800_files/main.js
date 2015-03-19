function change(left,right,num){
	if(num%2==0){
		$(left).addClass("content-right");
		$(left).removeClass("content-left");
		$(right).addClass("content-left");
		$(right).removeClass("content-right");
	}
}

function pageScroll(){
	window.scrollBy(0,-200);
	var scrolltime = setTimeout("pageScroll()",10);
	if($(document).scrollTop() == 0){
		clearTimeout(scrolltime);
	}
}

$(document).ready(function(){
	var k=0,em=1;
	var position=1;
	var pHeight=0;
	var itemH=new Array();
	itemH[0]=0;
	if($(document).scrollTop()==0){
		$("#htime").html($("#ptime1").html());
	}
	$(window).scroll(function(){
		k=0,position=1,pHeight=0;
		while(k<postnum){
			k++;
			if(k==1){
				itemH[k]=$("#"+k).outerHeight()-$("#ptime1").height();
			}
			else
				itemH[k]=$("#"+k).outerHeight();
		}
		while(0<position && position<=postnum){
			if($(document).scrollTop()>=pHeight && $(document).scrollTop()<pHeight+itemH[position]){
				$("#htime").html($("#ptime"+position).html());
				break;
			}
			pHeight+=itemH[position];
			position++;
		}
	});
	
	$("#showmore").mouseenter(function(){
		$(".more").slideDown();
		return false;
	});
	$("#showmore").mouseleave(function(){
		$(".more").slideUp();
		return false;
	});
	
});