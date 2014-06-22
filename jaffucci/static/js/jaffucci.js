var get_display_content_function = function (id, url) {
    return function (e) {
	$(".subcontent").hide();
	$(".button-container > button").removeClass("selected");
	$("#" + id.replace("-content", "")).addClass("selected");
	$("#" + id).show();
	window.location = "#" + id;
    };
};
