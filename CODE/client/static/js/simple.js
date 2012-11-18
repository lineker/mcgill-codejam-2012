$(document).ready(function () {
    String.prototype.toHHMMSS = function () {
        sec_numb    = parseInt(this);
        var hours   = Math.floor(sec_numb / 3600);
        var minutes = Math.floor((sec_numb - (hours * 3600)) / 60);
        var seconds = sec_numb - (hours * 3600) - (minutes * 60);

        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        var time    = hours+':'+minutes+':'+seconds;
        return time;
    } 

    var sock = io.connect('http://localhost:9090');

    var transactions = [];
    
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
                        var time = 32400 + parseInt(data.time) + "";

                        console.log(time);
                        $transactions.prepend('<div class="transaction"><span class="type">' + typeMap[data.type] + ' at $' + data.price + '</span><p>Completed at ' + time.toHHMMSS() + ' by ' + data['strategy'].toUpperCase()  + '</p></div>')
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
            })()}]
    });

    $("#pause").on('click', function () {
        socket.disconnect();
        $("#notifications").html("Trading stream temporarily paused.");
    });

    $(".nav > li").on('click', function (e) {
        e.preventDefault();
        $(".active").removeClass("active");
        $(this).addClass("active");
        chart.setTitle({ text: $(this).html() });
        var data = (function() {
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
            });
        chart.series[0].setData(data, true);
    });

    $("#managers").on('click', function (e) {
        e.preventDefault();
        $("#simple").css("display", "none");
        $("#schedule").css("display", "block");
    });

    $(".charts").on('click', function (e) {
        e.preventDefault();
        $("#schedule").css("display", "none");
        $("#simple").css("display", "block");
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
