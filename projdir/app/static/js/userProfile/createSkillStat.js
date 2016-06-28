var user_id = document.getElementById("userId").value,
    div_name = "user_stat_visual",
    user_skill_stat_div = $('#user_skill_stat_div');
$.ajax({
  url:"http://localhost:8000/get-user-skills-stat-api/v1/" + user_id + "/",
  type:'GET',
  success:function(data){
    var data_length = data.length;
    if(data_length){
      user_skill_stat_div.css('display','block');
      createStatVisual(data,div_name);
    }
  },
  error:function(e){
    console.log(e);
  }
});
