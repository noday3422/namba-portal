var chartData = {
  labels:labels,
  datasets:[
    {
      backgroundColor:'#dddddd',
      data:values1
    },
    {
      backgroundColor:'#0984e3',
      data:values2
    },
  ]
};

// 要素の指定
var chart_elem = document.getElementById('bar').getContext('2d');
var line_elem = document.getElementById('line').getContext('2d');

// 描画
var bar = new Chart(chart_elem, {
  type:'bar',
  data:chartData,
  options:{
    scales:{
      yAxes:[{
        ticks:{
          beginAtZero:true
        }
      }]
    }
  }
})

var line = new Chart(line_elem, {
  type:'line',
  data:chartData,
})
