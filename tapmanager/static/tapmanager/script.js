
$(document).ready( function () {
	FastClick.attach(document.body);
	//var attachFastClick = require('fastclick');
	//attachFastClick(document.body);
	$(".btn-add").click( function() {
		var value = $(this).parent().prev().val();
		value = parseInt(value) + 1;
		if (isNaN(value))
			value = 1;
		$(this).parent().prev().val(value);
	});
	$(".btn-minus").click( function() {
		var value = $(this).parent().next().val();
		value = parseInt(value) - 1;
		if (isNaN(value) || value <= 0)
			$(this).parent().next().val('');
		else
			$(this).parent().next().val(value);
	});
	$(".list-group-item>a").click( function() {
		
		if (!$(this).next().is(":visible")) {
			$(".list-group-item>a").each( function() {
				$(this).next().hide();
			});
			$(this).next().show();
		}
		else
			$(this).next().hide();
		
		//$(this).next().animate({height:"toggle"});
	});
});

