function createStatVisual(skill_data,div_name){
  var svgHeight = 500 ,
      svgWidth = 1000,
      barPadding = 1,
      heightFactor = 10,
      textPadding = 20,
      textFontSize = 15,
      fillColor = 'red',
      skillStatVisual = d3.select('#'+div_name),
      skill_data_length = skill_data.length,
      visualSVG = skillStatVisual.append('svg')
        .attr('height',svgHeight)
        .attr('width',svgWidth)
  visualSVG.selectAll('rect')
    .data(skill_data)
    .enter()
    .append('rect')
    .attr('x',function(d,i){
      return i * (svgWidth / skill_data_length);
    })
    .attr('y',function(d){
      return svgHeight - (d.count * heightFactor);
    })
    .attr('height',function(d){
      console.log(d.count * heightFactor);
      return d.count * heightFactor;
    })
    .attr('width',function(d,i){
      return svgWidth / skill_data_length - barPadding;
    });

  function appendStatText(){
    var visualText = visualSVG.selectAll('text')
      .data(skill_data)
      .enter()
      .append('text')
      .attr('x',function(d,i){
        return i * (svgWidth / skill_data.length) + 10;
      })
      .attr('y',function(){
        return svgHeight;
      })
      .attr('fill',fillColor)
      .attr('font-size',textFontSize)
      .text(function(d){
        return d.skill + ':' + d.count;
      })
  }
  appendStatText();
}
