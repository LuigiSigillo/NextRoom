const { Connection, Request, TYPES } = require("tedious");
const config = require("./config")

class DBHandler
{
//To be edited according to the table
  insertRow(macAddr,socket,response) {  
    const connection = new Connection(config);

    connection.on("connect", err => {
        if (err) {
          console.error(err.message);
        } else {
          const request = new Request("INSERT dbo.CurrentVisits (device_id, room1) VALUES (@device_id, @room1); select @@identity", function(err) {  
            if (err) {  
               console.log(err);
              } else {
                console.log('Insert complete')
              }  
              connection.close()
           });

           request.addParameter('room1', TYPES.DateTime, new Date());
           request.addParameter('device_id', TYPES.VarChar, macAddr);

           request.on('row', function(columns) {
             console.log("new id =  %d", columns[0].value)
             //socket.emit('startVisit', { "id": columns[0].value })
             var obj = { visitId : columns[0].value };
             //response.writeHead(200, {"Content-Type": "application/json"});
             response.send(JSON.stringify(obj));
             
           });    
           connection.execSql(request);
        }
    });
  }
}

module.exports = DBHandler;