//make connection to the backend, this variable is enabled by the html file
var socket = io({transports: ['websocket']});

//You can create multiple instances of these listeners to listen for different kind of messages
socket.on('The same label you assigned to the message in the server side script>', function(msg){
  //Do something to display data
});