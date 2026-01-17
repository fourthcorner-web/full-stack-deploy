// static/js/admin_sortable.js
(function($) {
    $(document).ready(function() {
        $(".inline-group").sortable({
            items: ".inline-related",
            handle: "h3", // Now you can grab anywhere on the title bar
            placeholder: "ui-state-highlight",
            forcePlaceholderSize: true, // Prevents layout "glitching"
            opacity: 0.8,
            cursor: "grabbing",
            tolerance: "pointer", // Makes it more sensitive/faster
            start: function(event, ui) {
                // Set the height of the placeholder to match the item being dragged
                ui.placeholder.height(ui.item.height());
            },
            update: function(event, ui) {
                $(this).find(".inline-related").each(function(index) {
                    $(this).find("input[id$='-order']").val(index);
                });
            }
        });
        
        // Change cursor to 'grab' when hovering over the header
        $(".inline-related h3").css("cursor", "grab");
    });
})(django.jQuery);