var get_display_content_function = function (selector) {
    return function (e) {
	$(".subcontent").hide("fast");
	$(".button-container > button").removeClass("selected");
	$(e.target).addClass("selected");
	$(selector).show("fast");
    };
};
