/**
* author : abhishek goswami ( hiro )
* abhishekg785@gmail.com
*
* github : abhishekg785
* userSocialAccountHandler.js :  js file to allow user add and edit its multiple accounts
*/

  var $addSocialInput = $('#addSocialInput'),
      $userSocialAccounts = $('#userSocialAccounts'),
      $saveSocialProfiles = $('#saveSocialProfiles'),
      SocialAccountNameArr = [],
      SocialAccountLinkArr = [],
      AccountCount = 0,
      csrf_token = $('#csrf_token');

  AddSocialAccountFunctions = {
    hideSaveButton : function(){
      $saveSocialProfiles.hide();
    },

    showSaveButton : function(){
      $saveSocialProfiles.show();
    },

    sendData : function(data){
      var postData = {
        'socialAccountData' : JSON.stringify(data),
        'csrfmiddlewaretoken' : csrf_token.val()
      }
      console.log(postData);
      $.ajax({
        url : 'http://localhost:8000/user/social-accounts/save',
        type : 'POST',
        data : postData,
        success : function(res){
          console.log(res);
        },
        error: function(err){
          console.log(err);
        }
      })
    },

    clearData : function(){
      SocialAccountNameArr = [];
      SocialAccountLinkArr = [];
    }
  }

  $addSocialInput.click(function(){
    var item = '<div id = "fillSocialAccount'+ AccountCount +'"><input type = "text"  id = "socialAccountName'+ AccountCount +'" class = "socialAccountName" placeholder = "Social Account" /><input type = "text" id = "socialAccountLink'+ AccountCount +'" class = "socialAccountLink" placeholder = "Link"/><button onclick = "cancelSocialAccount('+ AccountCount  +')" class = "cancelSocialAccount" id = "cancelSocialAccount'+ AccountCount +'">Cancel</button><hr/></div>';
    // $userSocialAccounts.append(item);
    $addSocialInput.before(item);
    AddSocialAccountFunctions.showSaveButton();
    AccountCount++;
  });

  function cancelSocialAccount(id){
    var fillSocialAccountID = 'fillSocialAccount' + id;
    $('#' + fillSocialAccountID).remove();
    AccountCount --;
    if(AccountCount == 0){
      AddSocialAccountFunctions.hideSaveButton();
    }
  }

  $saveSocialProfiles.click(function(){
    if(AccountCount > 0){
      var socialAccountNameArr = document.getElementsByClassName("socialAccountName");
      var socialAccountLinkArr = document.getElementsByClassName("socialAccountLink");
      for(var i = 0 ; i < socialAccountNameArr.length; i++){
        if(socialAccountNameArr[i].value == '' || socialAccountLinkArr[i].value == ''){
          alert("All fields are required");
          return;
        }
        else{
          SocialAccountNameArr.push(socialAccountNameArr[i].value);
          SocialAccountLinkArr.push(socialAccountLinkArr[i].value);
        }
      }
      var SocialAccountJSON = {
        "socialAccountNames" : SocialAccountNameArr,
        "socialAccountLinks" : SocialAccountLinkArr
      }
      console.log(SocialAccountJSON);
      console.log('sending data');
      AddSocialAccountFunctions.sendData(SocialAccountJSON);
      AddSocialAccountFunctions.clearData();
    }
  });
