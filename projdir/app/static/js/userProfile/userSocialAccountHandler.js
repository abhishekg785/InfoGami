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
      $displayUserSocialAccounts = $('#displayUserSocialAccounts'),
      $editSocialAccounts = $('#editSocialAccounts'),
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
          AddSocialAccountFunctions.updateDataINDOM().clearData().successMessage();
        },
        error: function(err){
          AddSocialAccountFunctions.errorMessage();
        }
      })
      return AddSocialAccountFunctions;
    },

    clearData : function(){
      SocialAccountNameArr = [];
      SocialAccountLinkArr = [];
      return AddSocialAccountFunctions;
    },

    successMessage : function(){
      $userSocialAccounts.empty();
      $userSocialAccounts.append('<h1 style = "color:green">All accounts Saved Successfully!</h1>');
    },

    errorMessage : function(){
      $userSocialAccounts.empty();
      $userSocialAccounts.append('<h1 style = "color:red">Error Occurred! Try Refreshing the page</h1>');
    },

    updateDataINDOM : function(){
      //set the all accounts in the $userSocialAccounts
      for(var i = 0 ; i < SocialAccountNameArr.length; i++){
        var item = SocialAccountNameArr[i] + ':' + '<a href = "'+ SocialAccountLinkArr[i] +'">'+ SocialAccountLinkArr[i] +'</a>';
        $displayUserSocialAccounts.append(item);
      }
      return AddSocialAccountFunctions;
    }
  }

  $addSocialInput.click(function(){
    var item = '<div id = "fillSocialAccount'+ AccountCount +'"><input type = "text"  id = "socialAccountName'+ AccountCount +'" class = "socialAccountName" placeholder = "Social Account" /><input type = "text" id = "socialAccountLink'+ AccountCount +'" class = "socialAccountLink" placeholder = "Link to the account"/><button onclick = "cancelSocialAccount('+ AccountCount  +')" class = "cancelSocialAccount" id = "cancelSocialAccount'+ AccountCount +'">Cancel</button><hr/></div>';
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
    }
  });
