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
    var $rows = $('.track_table tr');
    $('#search').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        
        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
    });


    var alive_num = $('.alive_num').attr('id');
    var dead_num = $('.dead_num').attr('id');

    var chart_array = [];

    var label = "Alive - " + alive_num;
    var value = alive_num;
    var data1 = {
        label: label,
        data: value,
        color: "#B894FF"
    };

    var label = "Dead - " + dead_num ;
    var value = dead_num;
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
        },
        legend: {
            position: "se",
            container: $("#chartLegend")
        }
    });

});