$('#getMessageBoxId').on('click',function(event){
  event.stopPropagation();
  var messageBoxId = $('#messageBoxId');
  messageBoxId.css('display','block');
  $("#getMessageBoxId").css('display','none');
});

//to prevent the wrapper event to occur on messageBoxId div
$("#messageBoxId").on('click',function(event){
  event.stopPropagation();
});


//function to send message
function sendMessage(senderId , receiverId,token){
  //ajax request
  message_text = $('#message_text').val();
  if(message_text == ""){
    alert('Message Field is required');
    return;
  }
  console.log('Messafe'+message_text)
  $('#sendMessageId').text('Sending...');
  var post_data = {
    'sender_id':senderId,
    'receiver_id':receiverId,
    'message_text':message_text,
    'csrfmiddlewaretoken':token
  };
  console.log(post_data);
  $.ajax({
    url:'http://localhost:8000/post-message-api/',
    type:'POST',
    data:post_data,
    dataType:'json',
    success:function(data){
      console.log(data);
      sucessFunc();
    },
    error:function(error){
      console.log('Error:',error);
    }
  });
}



$('#wrapper').on('click',function(event){
  $('#messageBoxId').css('display','none');
  $("#getMessageBoxId").css('display','block');
});


function sucessFunc(){
  $('#sendMessageId').text('Send');
  $('#message_text').val('');
}
