window.onload = function(){
  //create a WebSocket
  var socket = new WebSocket('ws://localhost:8000 ');

  //open the connection open-event
  socket.onopen = function(event){
    console.log(event);
  }

  //handling error
  socket.onerror = function(error){
    console.log(error);
  }
}
