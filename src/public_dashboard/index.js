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



io.on('connection', function (socket) {
    console.log('SERVER: connection made');

    //receive suggestions via http POST requests
    app.post('/', function (request, response) {
        var visitId = request.param("visitid");
        var suggList = request.param("sugg_list")
        console.log(suggList)
        response.send("200");
        console.log(visitId)
        socket.broadcast.emit('suggestions'+visitId, suggList);
        
    });



    socket.on('macAddr', function (macAddr) {
        console.log("macaddr:", macAddr)
        db.insertRow(macAddr,socket)
        
    })

});



/* CHEAT SHEET SOCKET.IO
 // sending to sender-client only
socket.emit('message', "this is a test");

// sending to all clients, include sender
io.emit('message', "this is a test");

// sending to all clients except sender
socket.broadcast.emit('message', "this is a test");

// sending to all clients in 'game' room(channel) except sender
socket.broadcast.to('game').emit('message', 'nice game');

// sending to all clients in 'game' room(channel), include sender
io.in('game').emit('message', 'cool game');

// sending to sender client, only if they are in 'game' room(channel)
socket.to('game').emit('message', 'enjoy the game');

// sending to all clients in namespace 'myNamespace', include sender
io.of('myNamespace').emit('message', 'gg');

// sending to individual socketid
socket.broadcast.to(socketid).emit('message', 'for your eyes only');

// list socketid
for (var socketid in io.sockets.sockets) {}
 OR
Object.keys(io.sockets.sockets).forEach((socketid) => {}); */