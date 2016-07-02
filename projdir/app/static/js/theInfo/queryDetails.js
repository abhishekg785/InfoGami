var provideAnswer = $('#giveAnswerButton'),
    voteAnswer = $('.voteAnswerButton'),
    token = $('#token').val(),
    voteDivStr = 'voteDiv',
    answerForm = $('#answerForm'),
    answerTextId = $('#answerText'),
    errorMessageDiv = $('#errorMessage'),
    cancelAnswerButton = $('#cancelAnswerButton'),
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
        $('#'+voteDivId).text('Votes:' + data.newVoteCount);
        location.reload();
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
  },

  undoVoteAnswer:function(answerId){
    var post_data = {
      'answer_id':answerId,
      'csrfmiddlewaretoken':token
    }
    $.ajax({
      url:'http://localhost:8000/theInfo/undo-vote-answer/',
      type:'POST',
      data:post_data,
      success:function(data){
        voteDivId = voteDivStr + answerId;
        $('#'+voteDivId).text('Votes:' + data.newVoteCount);
        location.reload();
      },
      error:function(error){
        console.log(error);
      }
    });
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

  cancelAnswerButton.click(function(){
    queryDetailsFunctions.hideAnswerForm();
  });

});
