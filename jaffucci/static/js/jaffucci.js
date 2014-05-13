var get_display_content_function = function (id, url) {
    return function (e) {
	$(".subcontent").hide("fast");
	$(".button-container > button").removeClass("selected");
	$("#" + id.replace("-content", "")).addClass("selected");
	$("#" + id).show("fast");
	window.location = "#" + id;
    };
};
