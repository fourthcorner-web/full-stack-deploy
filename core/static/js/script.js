$(function () {
    try {
        $('.nav-btn').on('click', function () {
            $(this).toggleClass('open');
        });
    } catch (error) {
        console.error('Error initializing nav button:', error);
    }
});

$(window).ready(function () {
    try {
        // Throttle scroll event for better performance
        var ticking = false;
        $(window).scroll(function () {
            if (!ticking) {
                window.requestAnimationFrame(function() {
                    try {
                        var scroll = $(window).scrollTop();
                        if (scroll > 100) {
                            $("#header").addClass('glass-effect');
                        } else {
                            $("#header").removeClass("glass-effect");
                        }
                    } catch (error) {
                        console.error('Error in scroll handler:', error);
                    }
                    ticking = false;
                });
                ticking = true;
            }
        });
    } catch (error) {
        console.error('Error initializing scroll handler:', error);
    }
})



