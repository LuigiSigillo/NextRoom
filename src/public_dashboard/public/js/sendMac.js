var socket = io({ transports: ['websocket'] });

socket.on('startVisit', function (body) {
    alert('You can start the visit!');

    document.location.href = "tour.html#id="+body["id"];
  });
  
  var myForm = document.getElementById("myForm");
  myForm.addEventListener("submit", function (e) {
    var macAddr = document.getElementById("MACaddress").value;
    e.preventDefault();
    console.log(macAddr)
    socket.emit('macAddr', macAddr)
  });
  