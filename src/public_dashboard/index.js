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

let groundTruth = { 20: ["room1", "room2"] }

io.on('connection', function (socket) {
    console.log('SERVER: connection made');
    /*
        socket.on('macAddr', function (macAddr) {
            console.log("macaddr:", macAddr)
            db.insertRow(macAddr,socket)
            
        })
    */
});

//receive suggestions via http POST requests   
app.post('/', function (request, response) {
    var visitId = request.param("visitid");
    var suggList = request.param("sugg_list")
    console.log(suggList)
    response.send("200");
    console.log(visitId)
    //socket.broadcast.emit('suggestions'+visitId, suggList);
    groundTruth[visitId] = suggList
});


// receive the macaddress from mobileapp and send back the visit id
app.post('/macaddr', function (request, response) {
    console.log("ciao")
    var macAddr = request.param("macAddr");
    db.insertRow(macAddr, socket, response);
    // rispondi nel db.insertrow
});


// handle the get from the mobileApp
app.get("/visit/:id", function (request, response) {
    var id = request.params.id;
    // do something with id
    // send a response to user based on id
    var obj = {
        id: id,
        suggList: groundTruth[id]
    };

    //response.writeHead(200, { "Content-Type": "application/json" });
    response.send(JSON.stringify(obj));
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