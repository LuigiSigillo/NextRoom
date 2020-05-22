const { Connection, Request, TYPES } = require("tedious");
const config = require("./config")

class DBHandler
{
  constructor(){}

  queryDatabase(querystring, callback) {
    const connection = new Connection(config);
    connection.on("connect", err => {
        if (err) {
          console.error(err.message);
        } else {

          console.log("Reading rows from the Table...");


          let queryFunction = (err, rowCount, rows) => {
            if (err) {
              console.error(err.message);
            } else {
              console.log(`${rowCount} row(s) returned`);
            }

            let queryResult = {};
            let count = 1;

            rows.forEach(row => {
              let new_row = {};
              row.forEach(column => {
                new_row[column.metadata.colName] = column.value;
              });
              queryResult['event'+count] = new_row;
              count += 1;
            });
            return callback(queryResult);
          }

          // Read all rows from table
          const request = new Request(
            querystring, queryFunction);

          connection.execSql(request);
        }
    });
  }

  //Cloud computing
  lastHourCloudValues(callback){
    return this.queryDatabase('SELECT * FROM Accelerometer.userdata WHERE date >= DATEADD(hour, -1, CURRENT_TIMESTAMP);', callback);
  }

  //Edge Computing
  lastHourEdgeValues(callback){
    return this.queryDatabase('SELECT * FROM Accelerometer.edgeactivity WHERE date >= DATEADD(hour, -1, CURRENT_TIMESTAMP);', callback);
  }

  //To be edited according to the table
  insertRow(date, walking) {  
    const connection = new Connection(config);

    connection.on("connect", err => {
        if (err) {
          console.error(err.message);
        } else {
          const request = new Request("INSERT Accelerometer.edgeactivity (date, walking) VALUES (@date, @walking);", function(err) {  
            if (err) {  
               console.log(err);}  
           });  
           request.addParameter('date', TYPES.DateTime, date);
           request.addParameter('walking', TYPES.Bit, walking);    
           connection.execSql(request);
        }
    });
  }
}

module.exports = DBHandler;