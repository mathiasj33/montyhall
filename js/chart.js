import * as util from './util.js';

export class BarChart {
    constructor(id, maxValue) {
        this.id = id;
        this.chart = null;
        this.data = null;
        this.maxValue = maxValue;
    }

    draw(data) {
        if (JSON.stringify(data) === JSON.stringify(this.data)) return;
        console.log('Update')
        this.data = data;
        data = util.jsonToArray(data);

        const dataTable = google.visualization.arrayToDataTable(data, true);
        const options = {
            legend: {position: 'none'},
            vAxis: {baseline: 0, viewWindow: {max: this.maxValue}}
        };
        this.chart = this.chart ? this.chart : new google.charts.Bar(document.getElementById(this.id));
        this.chart.draw(dataTable, google.charts.Bar.convertOptions(options));
    }
}
