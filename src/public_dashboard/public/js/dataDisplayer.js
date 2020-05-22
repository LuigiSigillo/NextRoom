var socket = io({transports: ['websocket']});

console.log('CLIENT: connection made');

//keep the last suggestions
let last_suggestions = [];
let button = null;

//function that displays the suggestion it takes in input
function display_suggestion(suggestion){
  console.log(suggestion);
}

//function associated to the button in the webapp to display the next suggestion
function next_suggestion(){
  let suggestion = last_suggestions.pop();
  if(suggestion){
    display_suggestion(suggestion);
  }
  else{
    alert('there are no more suggestions available for you :(');
  }
}

//Function to create button if it does not exist
function create_next_suggestion_button(){
  if(button == null){
    button = document.createElement('button');
    button.innerText = 'Next Room';
    const body = document.getElementById('body');
    button.addEventListener("click", event => {
      next_suggestion();
    });
    body.appendChild(button);
  }
}


//You can create multiple instances of these listeners to listen for different kind of messages
socket.on('suggestions', function(suggestions){
  alert('You have a new suggestion!');
  last_suggestions = suggestions.reverse();
  next_suggestion();
  create_next_suggestion_button();
});