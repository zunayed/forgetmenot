$(document).ready(function() {
    // Show or hide the sticky footer button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.go-top').fadeIn(200);
        } else {
            $('.go-top').fadeOut(200);
        }
    });
    // Animate the scroll to top
    $('.go-top').click(function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, 300);
    });


    //search box
    var $rows = $('#track_table tr');
    $('#search').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        
        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
    });

    var chart_array = [];

    var label = "Alive " + 45;
    var value = 45;
    var data1 = {
        label: label,
        data: value,
        color: "#FF5050"
    };

    var label = "dead " + 2 ;
    var value = 2;
    var data2 = {
        label: label,
        data: value,
        color: "#33CCCC"
    };

    chart_array.push(data1, data2); 

    $.plot('#placeholder1', chart_array, {
        series: {
            pie: {
                innerRadius: 0.5,
                show: true
            }
        }
    });

});