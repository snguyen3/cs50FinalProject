// https://www.chartjs.org/docs/latest/charts/line.html
// Graphing library: Chart.js powered by MIT

// Process raw data passed from Flask in the form of string
// Reference: Javascript regular expression for removing quotes and whitespaces: https://qawithexperts.com/questions/300/how-to-remove-quotation-marks-double-quotes-from-string-usin

// Process date_list; strip all whitespaces/quotes and turn the string into an int list
var raw_date_list = document.querySelector("#date_list").value;
var date_list = raw_date_list.substring(1, raw_date_list.length - 1);
date_list = date_list.split(",");
for (var i = 0; i < date_list.length; i++) {
    date_list[i] = date_list[i].replace(/[' "]+/g, '');
}

// Process the list of time_planned; strip all whitespaces/quotes and turn the string into an int list
var raw_tp_list = document.querySelector("#tp_list").value;
var tp_list = raw_tp_list.substring(1, raw_tp_list.length - 1);
tp_list = tp_list.split(",");
for (var i = 0; i < tp_list.length; i++) {
    tp_list[i] = parseInt(tp_list[i]);
}

// Process the list of time_spent; strip all whitespaces/quotes and turn the string into an int list
var raw_ts_list = document.querySelector("#ts_list").value;
var ts_list = raw_ts_list.substring(1, raw_ts_list.length - 1);
ts_list = ts_list.split(",");
for (var i = 0; i < ts_list.length; i++) {
    ts_list[i] = parseInt(ts_list[i]);
}

// Graph a line chart with Chart.js
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {

    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        labels: date_list,
        datasets: [{
                label: 'Time Planned',
                borderColor: 'rgb(255, 99, 132)',
                fill: false,
                data: tp_list
        },
            {
                label: 'Time Spent',
                borderColor: 'blue',
                fill: false,
                data: ts_list
        }]
    },
    // Configuration options go here
    options: {
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Time in Min'
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Dates'
                }
            }]
        }
    }
});