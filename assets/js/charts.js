getData(drawCharts);

function drawCharts(products) {
  var data = [];
  for (let product of products) {
    var snaps = [];
    for (let snap of product.snaps) {
      snaps.push({
        x: moment.unix(snap.created_at),
        y: snap.price
      })
    }
    var container = document.createElement('div');
    var div = document.createElement('div');
    var h2 = document.createElement('h2');
    var a = document.createElement('a');
    a.href = product.url;
    a.textContent = product.name;
    h2.appendChild(a);
    div.classList.add("ct-chart");
    container.classList.add("col-xs-12", "col-sm-6", "col-md-4", "col-lg-3");
    div.id = "ct-chart-"+product.md5;
    var charts = document.getElementsByClassName("charts")[0];
    container.appendChild(h2);
    container.appendChild(div);
    charts.appendChild(container);
    var data = {
      name: product.name,
      data: snaps
    };
    var chart = new Chartist.Line('#ct-chart-'+product.md5,
      {
        series: [
          data
        ]
      },
      {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('MMM D');
          }
        },
        plugins: [
          Chartist.plugins.tooltip({
            tooltipFnc: function(meta, value) {
              var price = value.split(",")[1];
              var time = value.split(",")[0];
              price = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
              time = moment.unix(time).format("HH:mm");
              return "<span>" + price + " руб.</span>"  + "<br>" + time;
            }
          })
        ]
    });
  }
}
