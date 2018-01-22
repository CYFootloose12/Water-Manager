data = [
  {
    key: "Cumulative Return",
    values: [
      { 
        "label" : "Sunday" ,
        "value" : 19.3
      } , 
      { 
        "label" : "Monday" , 
        "value" : 5.8
      } , 
      { 
        "label" : "Tuesday" , 
        "value" : 10.3
      } , 
      { 
        "label" : "Wednesday" , 
        "value" : 12.7
      } , 
      { 
        "label" : "Thursday" ,
        "value" : 0.551
      } , 
      { 
        "label" : "Friday" , 
        "value" : 0.345
      } , 
      { 
        "label" : "Saturday" , 
        "value" : 22.4
      } 
    ]
  }
]

nv.addGraph(function() {
  var chart = nv.models.discreteBarChart()
    .x(function(d) { return d.label })
    .y(function(d) { return d.value })
    .staggerLabels(false)
    .tooltips(false)
    .showValues(true)

  chart.titl

  chart.xAxis
    .axisLabel('Day of the Week')
    ;

  chart.yAxis
    .axisLabel('Amount of Water Received (mL)')
    .tickFormat(d3.format('0.01f'))
    ;

d3.select('#watering-amount-chart svg')
  .append("text")
  .attr("x", 275)             
  .attr("y", 12)
  .attr("text-anchor", "middle")  
  .text("Weekly Watering Amount");

  d3.select('#watering-amount-chart svg')
    .datum(data)
    .transition().duration(500)
    .call(chart)
    ;

  nv.utils.windowResize(chart.update);

  return chart;
});

