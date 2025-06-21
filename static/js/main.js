document.addEventListener("DOMContentLoaded", function () {
    $(".select-field").select2({
        width: "100%",
        dropdownAutoWidth: true,
        dropdownCssClass: "select-dropdown",
    }).on("select2:open", function () {
        $(".select-dropdown").css("color", "black");
    });
});
