var socket = io({ transports: ['websocket'] });

console.log('CLIENT: connection made');

//keep the last suggestions
let last_suggestions = [];
let button = null;

//function that displays the suggestion it takes in input
function display_suggestion(suggestion) {
  document.getElementById("sugg").innerHTML = "The next room suggested is " + suggestion.split("room")[1]
  console.log(suggestion);
}

//function associated to the button in the webapp to display the next suggestion
function next_suggestion() {
  let suggestion = last_suggestions.shift();
  if (suggestion) {
    display_suggestion(suggestion);
  }
  else {
    alert('there are no more suggestions available for you :(');
  }
}

//Function to create button if it does not exist
function create_next_suggestion_button() {
    div = document.getElementById("nextroomcontainer")
    button = document.createElement('button');
    button.innerText = 'Next Room';
    button.className = "button"
    button.addEventListener("click", event => {
      next_suggestion();
    });
    div.appendChild(button)
  
}

function takeId() {
  var url = window.location.href
  var id = url.split("#id=")[1]
  document.getElementById("visitid").innerHTML = "Your visit id is " + id;
  return id
}
var id = takeId()
console.log(id)
//You can create multiple instances of these listeners to listen for different kind of messages
socket.on('suggestions'+id, function (suggestions) {
  alert('You have a new suggestion!');
  last_suggestions = suggestions;
  next_suggestion();
  create_next_suggestion_button();
});

