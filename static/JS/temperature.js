var chartData = {
  labels:dateValues,
  datasets:[
    {
      data:minValues,
      label:'最低気温',
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgb(54, 162, 235)",
      fill:'origin'
    },
    {
      data:aveValues,
      label:'平均気温',
      backgroundColor: "rgba(255, 206, 86, 0.2)",
      borderColor: "rgb(255, 206, 86)",
      fill: 0
    },
    {
      data:maxValues,
      label:'最高気温',
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      borderColor: "rgb(255, 99, 132)",
      fill: 1
    },
  ]
};

// 要素の指定
var line_elem = document.getElementById('line').getContext('2d');

// 描画
var line = new Chart(line_elem, {
  type:'line',
  data:chartData,
})
