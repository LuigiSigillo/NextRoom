import 'package:flutter/material.dart';
import 'package:flutter_blue/flutter_blue.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert' as convert;
import 'package:collection/collection.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'BLE Demo',
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
                'images/dsc_00621.jpg',
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
  BluetoothDevice _connectedDevice;
  List<BluetoothService> _services;
  Timer timer;
  List<dynamic> suggestions;
  Function eq = const ListEquality().equals;
  int suggestionsCounter = 0;

  @override
  void initState() {
    super.initState();
    //Bluetooth Timer
    connectToNearestDevice();
    new Timer.periodic(
        new Duration(seconds: 20), (Timer t) => connectToNearestDevice());

    //Get Suggestions Timer
    //timer =
    //    Timer.periodic(Duration(seconds: 15), (Timer t) => getSuggestions());
    timer = Timer.periodic(Duration(seconds: 10), (Timer t) {
      updateSuggestions();
    });
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
    widget.flutterBlue.startScan(timeout: Duration(seconds: 4)).then(
        (value) => connectToDevice(widget.minSignalStrengthDevice.device));
  }

  void connectToDevice(BluetoothDevice device) async {
    await widget.flutterBlue.stopScan();
    try {
      await device.connect();
    } catch (e) {
      if (e.code != 'already_connected') {
        throw e;
      }
    } finally {
      _services = await device.discoverServices();
    }
    setState(() {
      _connectedDevice = device;
    });
    if (_connectedDevice != null) {
      _connectedDevice.disconnect();
      _connectedDevice = null;
    }
  }

  /* *******************************************
  * Get Suggestions part
  *********************************************/
  Future sendMac() async {
    var postResponse = await http
        .post("https://nextroom.azurewebsites.net/macaddr", body: {
      'macAddr': 'AA:BB:CC:11:00'
    }); // insert the mac address of device?
    print('Response status: ${postResponse.statusCode}');
    print('Response body: ${postResponse.body}');
  }

  Future<List<dynamic>> getSuggestions() async {
    var url = "https://nextroom.azurewebsites.net/visit/20";
    var response = await http.get(url);
    if (response.statusCode == 200) {
      var jsonResponse = convert.jsonDecode(response.body);
      //print(jsonResponse["suggList"]);
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

  void updateSuggestions() {
    getSuggestions().then((value) {
      if (!eq(suggestions, value)) {
        suggestions = value;
        suggestionsCounter = 0;
        _newSuggestionsAlert();
        setState(() {});
      }
    });
  }

  Text updateSuggestionView() {
    try {
      String currentSuggestion = suggestions[suggestionsCounter];
      return Text(currentSuggestion);
    } catch (e) {
      return Text('You have no suggestions available for now :(');
    }
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

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text('Next Room'),
          backgroundColor: Colors.red[800],
        ),
        body: Center(
          child: updateSuggestionView(),
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
