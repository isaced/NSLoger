// Close Message
$("button#message-close").click(function () {
  $("button#message-close").parent().hide("slow");
});


// reply a Comment
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