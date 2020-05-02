# Architecture

![Diagram](Images/Architecture_diagram.png)

## Board's features

### Bluetooth beacon

We will use the concept of bluetooth beacons. In this way an IoT device will recognize the smartphones in one section using a bluetooth scan and checking the replies from the smartphones.
Using the [Bluetooth Low Energy (BLE).](https://doc.riot-os.org/group__ble.html#details)

### LoRaWan

To connect the board to the cloud and retrieve the data we will use the LoRaWan protocol and as well the network services provided by [The Things Network](https://www.thethingsnetwork.org/). We have find out that there is a TTN gateway that covers the area of the Sapienza "Museo dell'Arte Classica", thus we will rely on it.

## Cloud infrastructure

### TTN/Cloud transparent bridge

To retrieve the data arriving on the TTN side, it's necessary to set-up a bridge that will connect to the Azure IoT Hub. This bridge will be hosted in the cloud using [Azure functions](https://azure.microsoft.com/en-us/services/functions/).

### Azure IoT Hub

We are using the Azure IoT Hub service as a central message hub to communicate between the application and the devices. The data will arrive to the IoT Hub. Using the stream analytics function we can redirect them on an Azure SQL DB.

### Data Processing

Basically there will be two Azure functions:

1. Use a function to process the data in the DB and update once a day the new suggestions for the different type of personas.
2. A function in charge of producing the next section list of suggestions for a specific user.

### Web Application

We will use a Web Application, probably written in node.js, to handle the start of the visit at the museum and the relative information to enter in the first phase.
The application will receive info on the next interesting section to see during the visit based on the time spent in the previous sections.

### Disclaimer

We are facing the COVID-19 emergency so we do not know if we will test the project also on real boards. For the moment we are trying to use the [IoT-LAB](https://www.iot-lab.info/) environment.
We will use as operating system for the IoT device [RIOT-OS](https://riot-os.org/).
