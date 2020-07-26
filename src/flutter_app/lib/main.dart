import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_blue/flutter_blue.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart' as blueSerial;
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert' as convert;
import 'package:collection/collection.dart';
import 'dart:math';
import 'dart:convert' show utf8;

String UNIQUEID = "";
void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Next Room',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        routes: {
          '/': (context) => HomePage(),
          '/visitPage': (context) => VisitPage(),
        },
      );
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
          decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage(
                'images/room0.jpg',
              ),
              fit: BoxFit.cover,
            ),
          ),
          child: Align(
            alignment: Alignment(0.0, -0.6),
            child: Text(
              "Next Room",
              style: TextStyle(
                fontSize: 60.0,
                fontWeight: FontWeight.bold,
                fontFamily: 'BlackOpsOne',
              ),
            ),
          )),
      floatingActionButton: Center(
        child: Align(
          alignment: Alignment(0.2, 0.5),
          child: Container(
            width: 300,
            height: 150,
            child: FloatingActionButton.extended(
              onPressed: () {
                Navigator.pushNamed(context, '/visitPage');
              },
              label: Text(
                'Start Visit',
                style: TextStyle(
                  fontSize: 30.0,
                ),
              ),
              backgroundColor: Colors.red[800],
            ),
          ),
        ),
      ),
    );
  }
}

class VisitPage extends StatefulWidget {
  VisitPage({Key key, this.title}) : super(key: key);
  final String title;
  final FlutterBlue flutterBlue = FlutterBlue.instance;
  final List<BluetoothDevice> devicesList = new List<BluetoothDevice>();
  final Map<Guid, List<int>> readValues = new Map<Guid, List<int>>();
  ScanResult minSignalStrengthDevice;

  @override
  _VisitPageState createState() => _VisitPageState();
}

class _VisitPageState extends State<VisitPage> {
  final _writeController = TextEditingController();
  String visitId = "";
  List<BluetoothService> _services;
  Timer timer;
  List<dynamic> suggestions;
  Function eq = const ListEquality().equals;
  int suggestionsCounter = 0;
  List<String> backgrounds = [
    'images/room1.jpg',
    'images/room2.jpg',
    'images/room3.jpg'
  ];
  Random _random = Random();
  BluetoothCharacteristic targetCharacteristic;

  @override
  void initState() {
    super.initState();
    connectToNearestDevice();

    //Bluetooth Timer
    new Timer.periodic(new Duration(seconds: 20), (Timer t) => connectToNearestDevice());

    //Get Suggestions Timer
    timer = Timer.periodic(Duration(seconds: 30), (Timer t) => updateSuggestions(this.visitId));

    //Proximity coronavirus
    makeDiscoverable(60*60);
    Timer.periodic(Duration(seconds: 50), (Timer t) => restartDiscovery());

  }

  /* *******************************************
   * Bluetooth connectivity part
  ******************************************* */
  _addDeviceTolist(final BluetoothDevice device) {
    if (!widget.devicesList.contains(device)) {
      setState(() {
        widget.devicesList.add(device);
      });
    }
  }

  void connectToNearestDevice() async {
    widget.flutterBlue.connectedDevices
        .asStream()
        .listen((List<BluetoothDevice> devices) {
      for (BluetoothDevice device in devices) {
        _addDeviceTolist(device);
      }
    });
    widget.flutterBlue.scanResults.listen((List<ScanResult> results) {
      for (ScanResult result in results) {
        _addDeviceTolist(result.device);
        if (result.device.name.startsWith("Room")) {
          if (widget.minSignalStrengthDevice != null) {
            if (widget.minSignalStrengthDevice.rssi > result.rssi)
              widget.minSignalStrengthDevice = result;
          } else
            widget.minSignalStrengthDevice = result;
        }
      }
    });
    widget.flutterBlue.startScan(timeout: Duration(seconds: 4)).then((value){
      if (widget.minSignalStrengthDevice != null)
        connectToDevice(widget.minSignalStrengthDevice.device);
        });
  }

  String addressToString(List<int> value) {
    print("siamo nella funzione" + value.toString());
    String valueString = "";
    int i = 0;
    for (var num in value) {
      valueString += num.toString();
      if (i < 4) {
        valueString += ":";
      }
      i += 1;
    }
    print(valueString);
    return valueString;
  }

  void readData(BluetoothCharacteristic characteristic) async {
    List<int> value = await characteristic.read();
    if (value.isNotEmpty) UNIQUEID = addressToString(value);
    if (UNIQUEID != "") {
      print("ci siamo" + UNIQUEID);
      sendMac(UNIQUEID).then((value) => this.visitId = value);
    } else
      print("id unico ancora vuoto " + UNIQUEID + value.toString());
  }

  void connectToDevice(BluetoothDevice device) async {
    await widget.flutterBlue.stopScan();
    try {
      await device.connect();
    } catch (e) {
      if (e.code != 'already_connected') {
        print('device not found');
      }
    } finally {
      if (UNIQUEID == "") {
        print("Start of the visit!!");
        _services = await device.discoverServices();
        _services.forEach((service) {
          //print(service);
          service.characteristics.forEach((characteristic) async {
            readData(characteristic);
          });
        });
      }
    }
    sleep(Duration(seconds: 1));
    device.disconnect();
  }

  /* *******************************************
  * Get Suggestions part
  *********************************************/
  Future sendMac(String macFalse) async {
    print("this is the macfalse" + macFalse);
    var postResponse = await http.post(
        "https://nextroom.azurewebsites.net/macaddr",
        body: {'macAddr': macFalse}); // insert the mac address of device?
    print('Response status: ${postResponse.statusCode}');
    print('Response body: ${postResponse.body}');
    var decoded = convert.jsonDecode(postResponse.body);
    var visitId = decoded['visitId'];
    return visitId.toString();
  }

  Future<List<dynamic>> getSuggestions(visitId) async {
    var url = "https://nextroom.azurewebsites.net/visit/" + visitId;
    var response = await http.get(url);
    if (response.statusCode == 200) {
      var jsonResponse = convert.jsonDecode(response.body);
      return jsonResponse["suggList"];
    } else {
      print('Request failed with status: ${response.statusCode}.');
      return List<dynamic>();
    }
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  void updateSuggestions(visitId) {
    getSuggestions(visitId).then((value) {
      if (!eq(suggestions, value) && value != []) {
        suggestions = value;
        suggestionsCounter = 0;
        _newSuggestionsAlert();
        setState(() {});
      }
    });
  }

  String updateSuggestionView() {
    try {
      return suggestions[suggestionsCounter];
    } catch (e) {
      return 'You have no\nsuggestions\navailable for now :(';
    }
  }

  /* *********************************
  * COVID-19 part
  ********************************** */

  blueSerial.FlutterBluetoothSerial istanza = blueSerial.FlutterBluetoothSerial.instance;
  StreamSubscription<blueSerial.BluetoothDiscoveryResult> _streamSubscription;
  List<blueSerial.BluetoothDiscoveryResult> results = List<blueSerial.BluetoothDiscoveryResult>();
  blueSerial.BluetoothDiscoveryResult b;
  bool isDiscovering;
  var counter = {};

  Future<int> makeDiscoverable(timeToBeDiscoverable) async {
    print('Discoverable requested');
    final int timeout = await istanza.requestDiscoverable(timeToBeDiscoverable);
    if (timeout < 0) {
      print('Discoverable mode denied');
      return -1;
    }
    else
      print('Discoverable mode acquired for ${timeout/60} minutes');
    return 1;
  }

  void restartDiscovery() {
    results.clear();
    isDiscovering = true;
    istanza.cancelDiscovery();
    startDiscovery();
  }

  void startDiscovery() {
    _streamSubscription =
        istanza.startDiscovery().listen((r) {
            if( r.device.name != null && ! r.device.name.startsWith("Room")){
              results.add(r);
              print("dispositivo: "+r.device.name +r.rssi.toString());
            }

        });

    _streamSubscription.onDone(() {
        isDiscovering = false;
      results.forEach((element) {
        var distance = pow(10,(-47-element.rssi)/(10*3));
        print(element.device.name +" distance: " +distance.toString());
        if(distance<1) {
          if (counter.containsKey(element.device.name)) {
            if (counter[element.device.name] > 3) {
              print("Covidddddddd");
              counter[element.device.name] = 0;
              _newProximityAlert(element.device.name);
            }
            else {
              print("not yet ");
              counter[element.device.name] += 1;
            }
          }
          else counter[element.device.name] = 1;
        }
        });
    });

  }


  void _newProximityAlert(String devicename) {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("You are too close to "+devicename),
          content: new Text("Keep the security distance between the people"),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Ok"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }



  /* *********************************
  * Build views methods
  ********************************** */
  void _newSuggestionsAlert() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("New Suggestions!"),
          content: new Text("Go ahead to see new suggestions"),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Ok"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  String changeBackground() {
    try {
      String suggestion = suggestions[suggestionsCounter];
      return backgrounds[_random.nextInt(backgrounds.length)];
    } catch (e) {
      return 'images/room0.jpg';
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text('Next Room'),
          backgroundColor: Colors.red[800],
        ),
        body: SizedBox.expand(
          child: Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage(
                  changeBackground(),
                ),
                fit: BoxFit.cover,
              ),
            ),
            child: Align(
              alignment: Alignment(0.0, -0.6),
              child: Text(
                updateSuggestionView(),
                style: TextStyle(
                  fontSize: 30.0,
                  fontFamily: 'BlackOpsOne',
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ),
        floatingActionButton: Align(
          alignment: Alignment(0.2, 0.7),
          child: FloatingActionButton.extended(
            onPressed: () {
              suggestionsCounter += 1;
              setState(() {});
            },
            label: Text('Change suggestion'),
            backgroundColor: Colors.red[800],
          ),
        ),
      );
}
