document.addEventListener("DOMContentLoaded", function () {
    $(".select-field").select2({
        width: "100%",
        dropdownAutoWidth: true,
        dropdownCssClass: "select-dropdown",
    }).on("select2:open", function () {
        $(".select-dropdown").css(
            "color", "black",
        );
    });
    $(".select2-selection").css({
        "height": "38px",
        "line-height": "38px",
        "padding-top": "4px",
        "padding-right": "15px"
    });
    $(".select2-container").css({
        "margin-right": "15px"
    });
    $(".select2-selection__arrow").css({
        "height": "38px"
    });
});
