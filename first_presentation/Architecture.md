# Architecture

## General
We are facing the COVID-19 emergency so we do not know if we will test the project also on real boards. For the moment we are trying to use the [IoT-LAB](https://www.iot-lab.info/) environment.

We will use as operating system for the IoT device [RIOT-OS](https://riot-os.org/).

## Board's features

### Bluetooth beacon
We will use the concept of bluetooth beacons. In this way an IoT device will recognize the smartphones in one room using a bluetooth scan and checking the replies from the smartphones.
Using the [Bluetooth Low Energy (BLE).](https://doc.riot-os.org/group__ble.html#details)
### LoRaWan
To connect the board to the cloud and retrieve the data we will use the LoRaWan protocol and as well the network services provided by [The Things Network](https://www.thethingsnetwork.org/). We have find out that there is a TTN gateway that covers the area of the museum, thus we will rely on it.

## Cloud infrastructure

### TTN/Cloud transparent bridge
To retrieve the data arriving on the TTN side, it's necessary to set-up a bridge that will connect to the Azure IoT Hub. This bridge will be hosted in the cloud using [Azure functions](https://azure.microsoft.com/en-us/services/functions/).
### Azure IoT Hub
The data will arrive to the IoT Hub. Using the stream analytics function we can redirect them on an Azure SQL DB.
### Data Processing

### Web Application

details on the technical aspects of the product/service, including a high-level presentation of the conceptual architecture of the software and hardware components that make up the product/service, a description of the main software/hardware components (e.g., 1 paragraph for each component), how these components interact (e.g., network protocols, APIs used), a network architecture clearly depicting the IoT elements, Edge components, Cloud components, End-user components.