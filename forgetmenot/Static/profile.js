$(document).ready(function() {
    // Show or hide the sticky footer button
    var table = document.getElementById("table");
    var current_song_index = 0;
    addRowHandlers(table);
    nextSong(table);

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

    //Flot Donut chart
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

    // $('.progress').spin();
    // $.get('/profile/update', function(){
    //     $('.progress').spin(false);
    // });

});

function addRowHandlers(table) {
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = 
            function(row) 
            {
                return function() { 
                    var cell = row.getElementsByTagName("th")[0];
                    var sc_id = row.id;

                    url = "https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/" + sc_id
                    settings = '&amp;color=ff5500&amp;auto_play=true&amp;hide_related=true&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false'
                    $('#sc_player').attr('src', url + settings)
                };
            };
        currentRow.onclick = createClickHandler(currentRow);
    }
}

function nextSong(table){
    var widgetIframe = document.getElementById('sc_player'),
        widget = SC.Widget(widgetIframe),
        newSoundUrl = 'http://api.soundcloud.com/tracks/13692671';

    widget.bind(SC.Widget.Events.READY, function() {
        // load new widget
        console.log("widget ready")
        widget.bind(SC.Widget.Events.FINISH, function() {
            console.log("finished")
            table.rows[43].trigger()
        });
    });
};
