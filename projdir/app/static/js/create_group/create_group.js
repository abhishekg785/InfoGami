/*
*  author: abhishek goswami
*  abhishekg785@gmail.com
*/

  var token = $('#token').val(),
  // console.log(token);
  groupDashboardFunctions = {
    sendMessage:function(group_id){
      var messageTextIdStr = 'messageText' + group_id;
          messageTextId = $('#'+messageTextIdStr),
          messageGroupStr = 'messageGroup' + group_id,
          messageGroupId = $('#' + messageGroupStr),
          messageLogStr = 'messageLog' + group_id,
          messageLogId = $('#' + messageLogStr);
      messageText = messageTextId.val();
      console.log(messageText.length);
      if(messageTextId.val() == ''){
        messageLogId.css('color','red');
        messageLogId.text('Message field is required');
        return;
      }
      messageGroupId.text('Sending...');
      var postData = {
        'csrfmiddlewaretoken':token,
        'messageText':messageTextId.val(),
        'group_id':group_id
      }
      $.ajax({
        url:'http://localhost:8000/group/send-group-message-api/',
        type:'POST',
        data:postData,
        success:function(data){
          messageTextId.val('');
          messageGroupId.text('Send');
          message = data.message;
          if(message == 'success'){
            messageLogId.css('color','green');
            messageLogId.text('You message has been sent to the users of the group');
          }
          else if(message == 'nouser'){
            messageLogId.css('color','red');
            messageLogId.text('No users in the group');
          }
        },
        error:function(error){
          console.log(error);
        }
      })
    },
  }
  function sendMessage(group_id){
    var messageAreaId = 'messageArea' + group_id;
    $('#'+messageAreaId).css('display','block');
  }

  function cancelMessage(group_id){
    var messageAreaId = 'messageArea' + group_id;
    $('#'+messageAreaId).css('display','none');
  }

  function sendMessageToGroup(group_id){
    groupDashboardFunctions.sendMessage(group_id);
  }
