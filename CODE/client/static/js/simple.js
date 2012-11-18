$(document).ready(function () {
    var sock = io.connect('http://localhost:9090');

    var transactions = []
    
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'simple',
            defaultSeriesType: 'spline',
            marginRight: 10,
            events: {
                load: function() {
                    var self = this,
                        price = this.series[0],
                        slow = this.series[1],
                        fast = this.series[2],
                        $transactions = $("#transactions"),
                        typeMap = {
                            "B": "Buy",
                            "S": "Sell"
                        };

                    sock.on('average', function (data) {
                        var x = data['time'],
                            y1 = data['price'],
                            y2 = data['slow'],
                            y3 = data['fast'];

                        price.addPoint([x, y1], true, true);
                        slow.addPoint([x, y2], true, true);
                        fast.addPoint([x, y3], true, true);
                    });

                    sock.on('transaction', function (data) {
                        transactions.push(data);
                        $transactions.prepend('<div class="transaction"><span class="type">' + typeMap[data.type] + ' at $' + data.price + '</span><p>Completed at XX:XX:XX AM by ' + data['strategy'].toUpperCase()  + '</p></div>')
                    });

                    sock.on('complete', function () {

                    });

                    sock.on('ceremony', function (data) {
                        var ceremonyId = data['ceremonyId'];
                        $("#notifications").html("Signature approved - your ceremony ID is: " + ceremonyid);
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
            })()}, {
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
            })()}, {
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
        sock.emit("ready");
        $("#notifications").html("The trading day has started.");
        $("#start").addClass("disabled");
        $("#pause").removeClass("disabled")
                   .removeClass("btn-danger")
                   .addClass("btn-warning");
        $("#reset").removeClass("disabled")
                   .removeClass("btn-danger")
                   .addClass("btn-warning");
    });

    $("#report").on('click', function (e) {
        $("#notifications").html("Report has been sent to Solaris for authentication and signing.");
        sock.emit("report");
    });
});
