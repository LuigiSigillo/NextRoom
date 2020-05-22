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

let server = app.listen(port, () => {
console.log(`Listening to requests on http://localhost:${port}`);
});

//This is the middleware to enable communication between server and clients(web pages)
let io = socket(server);

io.on('connection', function(socket){

    //The server is now connected with the client and you can start performing operations
    console.log('SERVER: connection made');
    //This is express that allows you to handle http post requests (for now the dashboard will receive http post messages)
    app.post('/',function(request,response){
        socket.emit('suggestions', request);
    });

    setInterval(function () {
        socket.emit('suggestions', ['room1', 'room2', 'room3']);
    }, 10000);
});