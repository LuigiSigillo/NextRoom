// Create connection to database
const config = {
    authentication: {
      options: {
        userName: "DBAdmin Username",
        password: "DB password"
      },
      type: "default"
    },
    server: "<server name>.database.windows.net",
    options: {
      database: "DB name",
      encrypt: true,
      rowCollectionOnRequestCompletion: true,
      trustServerCertificate: true
    }
  };

  module.exports = config;