(function($){
  var message_span = $('.messageSpan'),
      message_heading = $('a#message_heading'),
      load_message = $('#loadMessage'),
      mini_post = $('.mini-post'),
      message_section = $('#messageSection'),
      new_message_count = 0,
      new_message_arr = [],
      new_message_arr_len = 0,
      is_data = false,
      is_read = false,
      csrf_token = $('#csrf_token').val(),
      userId = $('#userId').val();

  baseFunctions = {

    //gets the messsages from the server
    getNewMessages:function(){
      $.ajax({
        url:'http://localhost:8000/user-new-messages/',
        type:'GET',
        success:function(data){
          var data_len = data.length;
          console.log(data_len);
          if(data_len){
            new_message_arr = data;
            new_message_arr_len = data.length;
            baseFunctions.loadMessageData().hideMessageLoader();
            is_data = true;
          }
          else{
            is_data = false;
            message_section.css({'height':'50px','overflow':'hidden'})
            load_message.text('No unread Messages');

          }
        },
        error:function(error){
          console.log(error);
        }
      });
      return baseFunctions
    },

    //loads data into the DOM
    loadMessageData:function(){
      //loads the data
      var list_item = '',
          item_id = '',
          item_class = 'new_messages',
          message_count = 0;
      for(var i = 0 ; i < new_message_arr_len ; i++){
        item_id = 'new_message' + i;
        message_count += new_message_arr[i].message_count;
        list_item = "<article class = '"+ item_class +"' id = '" + item_id +"' style = 'cursor:pointer' class = 'mini-post'><header><p>" + new_message_arr[i].latest_message +"(" + new_message_arr[i].message_count + ")</p><time class='published'>"+ new_message_arr[i].created.split('.')[0] + "</time><a class='author'><img src='/media/"+ new_message_arr[i].sender_profile_pic +"' alt='' /></a><p>by:<a href = ''>" + new_message_arr[i].sender + "</a></p></header></article>";
        mini_post.append(list_item);
      }
      message_span.text('('+ message_count +')');
      message_span.css('color','red');
      return baseFunctions;
    },

    //displaying the message pane
    displayMessagePane:function(){
      $('#messageSection').css('display','block');
      if(is_read && is_data){
        load_message.text('Recent Messages');
      }
      is_read = true;
    },

    hideMessagePane:function(){
      $('#messageSection').css('display','none');
    },

    setMessageLoader:function(){
      load_message.text('Fetching new messages...');
      return baseFunctions;
    },

    hideMessageLoader:function(){
      load_message.text('Unread Messages');
    },

    setMessageStatusSeen:function(){
      var user_id = user_id,
          post_data = {
          'user_id':userId,
          'csrfmiddlewaretoken': csrf_token
          }
      console.log(post_data);
      $.ajax({
        url:'http://localhost:8000/set-message-status-true-api/',
        type:'POST',
        data:post_data,
        success:function(data){
          console.log(data);
          is_data = false;
          message_span.css('display','none');
        },
        error:function(error){
          console.log(error);
        }
      });
    }
  }

  $(document).ready(function(){
    var username = "{{ user.username }}";
    if(username != 'undefined' && username != ''){
      baseFunctions.setMessageLoader().getNewMessages();
      $('.messageLink').hover(
        function(){
          baseFunctions.displayMessagePane();
        },
        function(){
          baseFunctions.hideMessagePane();
          if(is_data == true){
            baseFunctions.setMessageStatusSeen();
          }
        }
      );
    $('#messageSection').hover(
      function(){
        baseFunctions.displayMessagePane();
      },
      function(){
        baseFunctions.hideMessagePane();
        if(is_data == true){
          baseFunctions.setMessageStatusSeen();
        }
      }
    );

    $('.mini-post').on('click','.new_messages',function(){
      window.location = '/message-center';
    });
  }
  });
})(jQuery);
