# Architecture

![Diagram](Images/Architecture_diagram.png)

## Board's features

### Bluetooth beacon

We will use the concept of bluetooth beacons. In this way an IoT device will recognize the smartphones in one section using a bluetooth scan and checking the replies from the smartphones.
Using the [Bluetooth Low Energy (BLE).](https://doc.riot-os.org/group__ble.html#details)

### MQTT

Our initial idea was to use LoRa and TTN to communicate between the boards present in each section, and Azure IoT Hub, but after a load test we councluded that this was not suitable for our solution. So we changed our mind and decided to use MQTT for this purpose. Also, to face the BLE false positives problem we decided that the boards will publish data to two MQTT topics, one to communicate between each other, to reach a consensus on the final list of devices present in each section, and the other to communicate with Azure IoT Hub.

## Cloud infrastructure

### MQTT broker

To use the MQTT protocol it is essential to use an MQTT broker. To perform our imulation this MQTT broker will be run on our laptop using [Mosquitto](www.mosquitto.org) but in the museum this task will be implemented by a dedicated board, or by another computer that has to always listen to MQTT messages to allow the system to work correctly.

### Azure IoT Hub

We are using the Azure IoT Hub service as a central message hub to communicate between the application and the devices. The data will arrive to the IoT Hub. Using an Azure Function we can redirect this flow of data to an Azure SQL DB, and process them in order to generate suggestions

### Data Processing

Basically there will be an Azure function that will perform three tasks:

1. Redirect the incoming data flow from the Azure IoT Hub to an SQL DB in order to easily retrieve the history of past visits. This is fundamental for our algorithm to work.
2. Redirect the incoming data flow from the Azure IoT Hub to the curators' dashboard through an HTTP POST message
3. Implement an algorithm that generates a sorted list of suggestions basing its choice on the sum of two scores: a similarity score between the current visit and the others present in the database,  and a score computed on how many people are currently in the section (this will increment as the number of people becomes smaller). The algorithm sorts the list of section in in a decreasing order, using the computed score as a key, and send the list of suggestions to the web application through a HTTP POST message.

### Web Application

We will use a Web Application, written in node.js, to handle the start of the visit at the museum and the relative information to enter in the first phase.
The application will receive info on the next interesting section to see during the visit based on the time spent in the previous sections, and based on how many people is currently in that section.

### Curators Dashboard

We will also implement a curators' dashboard, since the problem of facing COVID-19 addresses everybody: both the curators of the museum, and the users of the museum that want to visit it. It shows the number of people that are present in a given section in a given time. So this dashoard is able to retrieve data from the Database to show the curators the history of past visits, and realtime data that it will get through a HTTP POST request.

The old version of this doucment can be found [here](OlderVersions/Architecture01)
