/*
 * 初始化按钮的loading功能，点击后将显示Loading字样，并且按钮被disabled掉，无法连续点击，防止二次提交
 * 超过3秒后按钮将恢复原状
 */
$(function(){
	$('button[data-loading-text]').click(function () {
	    var btn = $(this).button('loading');
	    setTimeout(function () {
	        btn.button('reset');
	    }, 3000);
	});
});

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