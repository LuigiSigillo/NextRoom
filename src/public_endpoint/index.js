const express = require('express')
const bodyParser = require('body-parser')
import DBHandler from 'scripts/dbHandler'

//Exprees allows you to handle the place where to find static resources, and allows you to create a server
const app = express()
const port = process.env.PORT || '3000'

//Configuring express to use body-parser
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
let server = app.listen(port, () => {
    console.log(`Listening to requests on http://localhost:${port}`)
});

let db = new DBHandler()

let groundTruth = { 20: ["room1", "room2"] }

//receive suggestions via http POST requests   
app.post('/', function (request, response) {
    let visitId = request.param("visitid")
    let suggList = request.param("sugg_list")
    response.send("200")
    //socket.broadcast.emit('suggestions'+visitId, suggList);
    groundTruth[visitId] = suggList
});


// receive the macaddress from mobileapp and send back the visit id
app.post('/macaddr', function (request, response) {
    let macAddr = request.param("macAddr")
    db.insertRow(macAddr, response)
});


// handle the get from the mobileApp
app.get("/visit/:id", function (request, response) {
    let id = request.params.id;
    // do something with id
    // send a response to user based on id
    let obj = {
        id: id,
        suggList: groundTruth[id]
    };

    response.send(JSON.stringify(obj))
});