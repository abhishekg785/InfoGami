var provideAnswer = $('#giveAnswerButton'),
    voteAnswer = $('.voteAnswerButton'),
    token = $('#token').val(),
    voteDivStr = 'voteDiv',
    answerForm = $('#answerForm'),
    answerTextId = $('#answerText'),
    errorMessageDiv = $('#errorMessage'),
    isForm = false;



var queryDetailsFunctions = {
  voteAnswer:function(answerId){
    post_data = {
      'answer_id':answerId,
      'csrfmiddlewaretoken':token
    }
    $.ajax({
      url:'http://localhost:8000/theInfo/vote-answer/',
      type:'POST',
      data:post_data,
      success:function(data){
        voteDivId = voteDivStr + answerId;
        $('#'+voteDivId).text(data.newVoteCount);
      },
      error:function(error){
        console.log(error);
      }
    });
  },

  hideAnswerForm:function(){
    answerForm.css('display','none');
  },

  displayAnswerForm:function(){
    answerForm.css('display','block');
  },

  checkAnswerForm:function(){
    answerText = answerTextId.val();
    if(answerText == ''){
      console.log(errorMessageDiv);
      errorMessageDiv.css('color','red');
      errorMessageDiv.text('Field cannot be empty');
      return false;
    }
    return true;
  }
}

$(document).ready(function(){
  provideAnswer.click(function(){
    if(isForm == false){
      queryDetailsFunctions.displayAnswerForm();
      isForm = true;
    }
    else{
      queryDetailsFunctions.hideAnswerForm();
      isForm = false;
    }
  });

  provideAnswer.click(function(){

  });

});
