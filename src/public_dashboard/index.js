const express = require('express');
const socket = require('socket.io');
let bodyParser = require('body-parser');

//Exprees allows you to handle the place where to find static resources, and allows you to create a server
const app = express();
const port = process.env.PORT || '3000';

//static resources
app.use(express.static('public'));
//Configuring express to use body-parser
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
let DBHandler = require('./scripts/dbhandler');
let server = app.listen(port, () => {
console.log(`Listening to requests on http://localhost:${port}`);
});

let io = socket(server);
let db = new DBHandler();

//function to convert the dictionary into a linked list
function suggest_to_client(request){
    //list to send the message
    let payload = [];

    for(let key in request){
        payload.push(request[key]);
    }
    socket.emit('suggestions', payload);
}

io.on('connection', function(socket){
    console.log('SERVER: connection made');
    //receive suggestions via http POST requests
    app.post('/',function(request,response){
        suggest_to_client(request);
    });


    socket.on('macAddr', function(macAddr){
        console.log("macaddr:",macAddr)
        db.insertRow(macAddr)
        socket.emit('startVisit', {"id" : "25"})
    })
});