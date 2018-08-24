$(document).ready(function () {
    $(function () {
        var location = window.location.href;
        var cur_url = location.split('/');
        cur_url = '/' + cur_url.slice(3).join('/');
        $('.backlighting_nav_item').each(function () {
            var link = $(this).find('a').attr('href').split('/');
            link = link.join('/');
            if (cur_url == link) {
                $(this).addClass('active');
            }
        });
    });
});