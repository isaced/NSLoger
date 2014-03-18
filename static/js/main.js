// Close Message
$("button#message-close").click(function () {
  $("button#message-close").parent().hide("slow");
});

// no re submit
// $("form").submit(function(){  
// $(":submit",this).attr("disabled","disabled");  
// });

// Reply Comment
function replyOne(username,at_floor){
    replyContent = $("#reply_content");
	oldContent = replyContent.val();
	prefix = "#" + at_floor + "楼 @" + username + " ";
	newContent = ''
	if(oldContent.length > 0){
	    if (oldContent != prefix) {
	        newContent = oldContent + "\n" + prefix;
	    }
	} else {
	    newContent = prefix
	}
	replyContent.focus();
	replyContent.val(newContent);
}

// Floor add Link
$(function(){
	obj = $(".comment-tableview")
	if (obj.length>0) {
		var str=obj.html();
		var attr=/#[1-9]\d*楼/g;
		str = str.replace(attr, function(floor){
			n = floor.substring(1,floor.length-1);
			return "<a href='#comment"+ n +"' onclick='gotofloor(" + n +")'>"+floor+"</a>";}
		);
		$(".comment-tableview").html(str);
	};
});

var old_element = null;
function gotofloor(floor){
	if (old_element != null) {
		old_element.removeClass("light");
	};	
	var new_element = $("#comment"+floor);
	new_element.addClass("light");
	old_element = new_element;

}