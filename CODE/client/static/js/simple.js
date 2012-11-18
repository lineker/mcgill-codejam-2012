$(document).ready(function () {
    var sock = io.connect('http://localhost:9090');
    
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'simple',
            defaultSeriesType: 'spline',
            marginRight: 10,
            events: {
                load: function() {
                    var price = this.series[0],
+                    sta   = this.series[1],
+                    lta   = this.series[2];
+
                 setInterval(function() {
                     var x = (new Date()).getTime(),
                         // current time
-                        y = Math.random();
-                    series.addPoint([x, y], true, true);
+                        y1 = Math.random(),
+                        y2 = Math.random();
+                        y3 = Math.random();
+                    
                    price.addPoint([x, y1], true, true);
+                   sta.addPoint([x, y2], true, true);
+                   lta.addPoint([x, y3], true, true);




                    var price = this.series[0];
                    sock.emit('ready');
                    sock.on('data', function (data) {
                        var price = self.series[0],
                            x = data['time'],
                            y = data['value'];

                        price.addPoint([x, y], true, true);
                    });
                }
            }
        },
        title: {
            text: 'Simple Moving Average (SMA)',
            style: {
                margin: '10px 100px 0 0' // center it
            }
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'}]
        },
        tooltip: {
            formatter: function() {
                return '<b>' + this.series.name + '</b><br/>' + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                },
                animation: {
                    duration: 500,
                    easing: "swing"
                },
                enableMouseTracking: false
            },
            
        },
        series: [{
            data: (function() {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;
                for (i = -19; i <= 0; i++) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                    });
                }
                return data;
            })()}]
    });

    $(".nav > li").on('click', function (e) {
        e.preventDefault();
        $(".active").removeClass("active");
        $(this).addClass("active");
        chart.setTitle({ text: $(this).html() });
    });

    $("#start").on('click', function (e) {
        sock.emit("start"); 
    });

    $("#report").on('click', function (e) {
        if (!$(this).hasClass("disabled")) {
            console.log("reported!");
        }
    });
});
