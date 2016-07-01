var searchBar = $('#searchBar'),
    //add new Query parameters
    addQueryTextId = $('#addQueryTextId'),
    addQueryTagsId = $('#addQueryTagsId'),
    //new query parameters end here

    messageDiv = $('#messageDiv'),
    addQueryDiv = $('#addQueryDiv'),
    enableAddQuery = $('#enableAddQuery'),
    cancelAddQuery = $('#cancelAddQuery'),
    answerToQueryDiv = $('#answerToQueryDiv'),
    enableAnswerToQuery = $("#enableAnswerToQuery"),
    cancelAnswerToQuery = $('#cancelAnswerToQuery'),
    resultDiv = $('#resultDiv'),
    resultDivUL = $('#resultDiv ul'),
    answerText = $('#answerText'),
    csrf_token = $('#csrf_token').val(),
    theInfoAboutDiv = $('#theInfoAboutDiv'),
    closeTheInfoAboutDiv = $('#closeDesc'),
    dotsLoader = $('#dots-loader'),
    votingSection = $('.votingSection'),
    aboutTheInfo = $('#aboutTheInfo'),
    quesDict = $('#quesDict'),
    isQueryDiv = false,
    isAnswerDiv = false,
    isResultData = false,
    queryIdArray = [],
    queryTagsArray = [],
    queryTextArray = [],
    queryAnswersArray = [],
    queryAnswersVoteSortedArrray = [];




var theInfoFunctions = {
  checkAddQueryForm:function(){
    var queryText = addQueryTextId.val(),
        tagsText = addQueryTagsId.val();
    if(queryText == '' || tagsText == ''){
      theInfoFunctions.errorMessageDiv('all fields are required');
      return false;
    }
    else{
      var commaIndex = tagsText.indexOf(',');
      if(commaIndex == -1){
        var newVal = tagsText + ','
        $('#addQueryTagsId').val(newVal);
      }
    }
    return true;
  },

  displayAddQueryDiv:function(){
    addQueryDiv.css('display','block');
  },

  hideAddQueryDiv:function(){
    addQueryDiv.css('display','none');
  },

  errorMessageDiv:function(error_str){
    messageDiv.text(error_str);
    messageDiv.css('color','red');
  },

  displayGiveMessageDiv:function(){
    answerToQueryDiv.css('display','block');
  },

  hideGiveMessageDiv:function(){
    answerToQueryDiv.css('display','none');
  },

  get_query_results:function(){
    var queryText = searchBar.val();
        postData = {
          'query_text':queryText,
          'csrfmiddlewaretoken':csrf_token
        }
    $.ajax({
      url:'http://localhost:8000/theInfo/search-query/',
      type:'POST',
      data:postData,
      success:function(data){
        if(data.length > 0){
          messageDiv.text('');
          resultDiv.text('');
          resultDiv.append('<h1><u>Results found for <i>"'+ queryText +'"</i></u></h1>');
          theInfoFunctions.setData(data).loadData();
          theInfoFunctions.hideLoader();
        }
        else{
          theInfoFunctions.hideLoader();
          theInfoFunctions.setNoDataMessage();
        }
      },
      error:function(error){
        console.log(error);
      }
    });
  },


  setData:function(dataArr){
    queryIdArray = [];
    queryTextArray = [];
    queryAnswersArray = [];
    queryTagsArray = [];
    queryAnswersVoteSortedArrray = [];
    dataArr.forEach(function(data){
      var queryId = data.query_id,
          queryAnswers = data.query_answers,
          queryTags = data.query_tags,
          queryText = data.query_text;
      queryIdArray.push(queryId);
      queryTextArray.push(queryText);
      queryAnswersArray.push(queryAnswers);
      queryTagsArray.push(queryTags)
    });
    //creating the arry consisting of message object only
    var answerArrLen = queryAnswersArray.length;
    for(var i = 0 ; i < answerArrLen ; i++){
      var ansArr = queryAnswersArray[i];
      var ansArrLen = ansArr.length;
      if(ansArrLen > 0){
        for(var j = 0 ; j < ansArrLen ; j++){
          var ansObj = {
            'queryIndex':i,
            'answerText':ansArr[j].ans_text,
            'answerVote':ansArr[j].ans_vote,
            'ansId':ansArr[j].ans_id,
            'ansUser':ansArr[j].ans_username,
            'ansUserId':ansArr[j].ans_user_id,
            'loggedUserAnswerVoteStatus':ansArr[j].vote_status_for_logged_user
          }
          queryAnswersVoteSortedArrray.push(ansObj);
        }
      }
    }
    //sorting the array on the basis of votes
    queryAnswersVoteSortedArrray.sort(function(a,b){
      return a.answerVote - b.answerVote;
    }).reverse();
    return theInfoFunctions;
  },


  loadData:function(){
    var queryAnswerObjLen = queryAnswersVoteSortedArrray.length,
        queryAnswerTextDiv = $('.queryAnswer'),
        queryAnswerTagDiv = $('.answerTags'),
        answerQueryDiv = $('.answerQuery');
    if(queryAnswerObjLen){
      for(var i = 0 ; i < queryAnswerObjLen ; i++){
        var answerQueryIndex = queryAnswersVoteSortedArrray[i].queryIndex,
            answerTags = queryTagsArray[answerQueryIndex],
            queryId = queryIdArray[answerQueryIndex],
            tagArrLen = answerTags.length,
            answerVote = queryAnswersVoteSortedArrray[i].answerVote,
            ansId = queryAnswersVoteSortedArrray[i].ansId,
            queryAnswerDivId = 'queryAnswer' + ansId,
            ansUsername = queryAnswersVoteSortedArrray[i].ansUser,
            ansUserId = queryAnswersVoteSortedArrray[i].ansUserId,
            loggedUserAnswerVoteStatus = queryAnswersVoteSortedArrray[i].loggedUserAnswerVoteStatus,
            votingSectionId = 'votingSection' + ansId;
        tags = answerTags.join()
        var item;
        if(!loggedUserAnswerVoteStatus){   //user has not voted
          var voteButtonId = 'voteButton' + ansId;
          item = "<div id = '"+ queryAnswerDivId +"' class = 'queryAnswer'><p>"+ queryAnswersVoteSortedArrray[i].answerText +"</p><div class = 'answerInfo'><div class = 'answerTags'>Tags:<i>"+ tags +"</i></div><div class = 'answerQuery'>Under:<a href = '/theInfo/query/"+ queryId +"/details/'><i>'"+ queryTextArray[answerQueryIndex]+ "'</i></a></div></div><div id = '"+ votingSectionId +"' class = 'votingSection'><button id = '"+ voteButtonId +"' onclick = 'theInfoFunctions.voteQueryAnswer("+ ansId +")'>Vote</button><div class = 'voteCount'>"+ answerVote + "</div></div></div>by:<a href = '/user/profile/" + ansUserId +"'>"+ ansUsername +"</a><hr/>";
        }
        else{
          var undoButtonId = 'undoButton' + ansId;
          item = "<div id = '"+ queryAnswerDivId +"' class = 'queryAnswer'><p>"+ queryAnswersVoteSortedArrray[i].answerText +"</p><div class = 'answerInfo'><div class = 'answerTags'>Tags:<i>"+ tags +"</i></div><div class = 'answerQuery'>Under:<a href = '/theInfo/query/"+ queryId +"/details/'><i>'"+ queryTextArray[answerQueryIndex]+ "'</i></a></div></div><div id = '"+ votingSectionId +"' class = 'votingSection'><h1 style = 'color:green'>Voted</h1><button id ='"+ undoButtonId +"' onclick = 'theInfoFunctions.undoAnswerVote("+ ansId +")'>Undo</button><div class = 'voteCount'>"+ answerVote + "</div></div></div>by:<a href = '/user/profile/" + ansUserId +"'>"+ ansUsername +"</a><hr/>";
        }
        resultDiv.append(item);
      }
    }
  },

  displayLoader:function(){
    console.log(dotsLoader);
    dotsLoader.css('display','block');
  },

  hideLoader:function(){
    dotsLoader.css('display','none');
  },

  voteQueryAnswer:function(answerId){
    post_data = {
      'answer_id':answerId,
      'csrfmiddlewaretoken':csrf_token
    };

    $.ajax({
      url:'http://localhost:8000/theInfo/vote-answer/',
      type:'POST',
      data:post_data,
      success:function(data){
        newVoteCount = data.newVoteCount;
        theInfoFunctions.voteChangesInDOM(newVoteCount,answerId,'vote');
      },
      error:function(error){
        console.log(error);
      }
    });
  },

//handles the Info about the page
  showAboutTheInfo:function(){
    theInfoAboutDiv.css('display','block');
  },

  hideAboutTheInfo:function(){
    theInfoAboutDiv.css('display','none');
  },

  undoAnswerVote:function(answerId){
    post_data = {
      'answer_id':answerId,
      'csrfmiddlewaretoken':csrf_token
    }
    $.ajax({
      url:'http://localhost:8000/theInfo/undo-vote-answer/',
      type:'POST',
      data:post_data,
      success:function(data){
        newVoteCount = data.newVoteCount;
        theInfoFunctions.voteChangesInDOM(newVoteCount,answerId,'undo');
      },
      error:function(error){
        console.log(error);
      }
    });
  },


  voteChangesInDOM:function(newVoteCount,answerId,type){
    var votingSectionId = 'votingSection' + answerId;
    var queryAnswerId = 'queryAnswer' + answerId;   //id of each div having the whole answer
    var selectionStr = '#' + queryAnswerId + ' ' + '.voteCount';
    $(selectionStr).text(newVoteCount);
    if(type == 'vote'){
      //change button to undo and label = voted
      //display:none for voteButton + ansId
      $('#'+votingSectionId).text('');
      var undoButtonId = 'undoButton' + answerId;
      $('#' + votingSectionId).append("<h1 style = 'color:green'>Voted</h1><button id = '"+ undoButtonId +"' onclick = 'theInfoFunctions.undoAnswerVote("+ answerId +")'>Undo</button><div class = 'voteCount'>"+ newVoteCount + "</div>");
    }
    else if(type == 'undo'){
      //change button to vote
      $('#'+votingSectionId).text('');
      var voteButtonId = 'voteButton' + answerId;
      $('#' + votingSectionId).append("<button id = '"+ voteButtonId +"' onclick = 'theInfoFunctions.voteQueryAnswer("+ answerId +")'>Vote</button><div class = 'voteCount'>"+ newVoteCount + "</div>");
    }
  },

  setNoDataMessage:function(){
    resultDiv.append("<h1><u>No results Found!!!</u></h1><p>But Yes!!! You can add your own query to 'TheInfo' and make it better</p>")
  }


};

$(window).load(function(){
  enableAddQuery.on('click',function(event){
    event.stopPropagation();
    if(!isQueryDiv){
      theInfoFunctions.displayAddQueryDiv();
      isQueryDiv = true;
    }
    else{
      theInfoFunctions.hideAddQueryDiv();
      isQueryDiv = false;
    }
  });

  cancelAddQuery.on('click',function(){
    theInfoFunctions.hideAddQueryDiv();
  });

  addQueryDiv.click(function(event){
    event.stopPropagation();
  });

  enableAnswerToQuery.click(function(){
    if(!isAnswerDiv){
      theInfoFunctions.displayGiveMessageDiv();
      isAnswerDiv = true;
    }
    else{
      theInfoFunctions.hideGiveMessageDiv();
      isAnswerDiv = false;
    }
  });

  cancelAnswerToQuery.click(function(){
    answerText.val('');
    theInfoFunctions.hideGiveMessageDiv();
  });

  $('body').click(function(){
    theInfoFunctions.hideAddQueryDiv();
  });

  searchBar.on('keydown',function(event){
    if(event.keyCode == 13){
        var query_str = searchBar.val();
        if(query_str == ''){
          theInfoFunctions.errorMessageDiv('Query Field is required!');
        }
        else{
          messageDiv.empty();
          resultDiv.empty();
          theInfoFunctions.displayLoader();
          theInfoFunctions.get_query_results();
        }
    }
    // else{
    //   resultDivUL.text('')
    //   theInfoFunctions.get_query_results();
    // }
  });

  closeTheInfoAboutDiv.click(function(){
    theInfoFunctions.hideAboutTheInfo();
  });

  aboutTheInfo.click(function(){
    theInfoAboutDiv.css('display','block');
  });

  quesDict.click(function(){
    window.location = '/theInfo/queries/';
  });
});
