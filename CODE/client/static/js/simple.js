$(document).ready(function () {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'simple',
            defaultSeriesType: 'spline',
            marginRight: 10,
            events: {
                load: function() {

                    // set up the updating of the chart each second
                    var price = this.series[0],
                        sta   = this.series[1],
                        lta   = this.series[2];

                    setInterval(function() {
                        var x = (new Date()).getTime(),
                            // current time
                            y1 = Math.random(),
                            y2 = Math.random();
                            y3 = Math.random();

                        price.addPoint([x, y1], true, true);
                        sta.addPoint([x, y2], true, true);
                        lta.addPoint([x, y3], true, true);
                    }, 500);
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
            })()},{
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
            })()},{
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
});