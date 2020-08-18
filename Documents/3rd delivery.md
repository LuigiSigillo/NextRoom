- Changes made to your design, architecture and evaluation plan since the 2nd delivery. You should justify the need for these changes.
- Brief presentation of the technical work done since the 2nd delivery.
- Brief presentation of the evaluation conducted since the 2nd delivery.
- A brief list of the functionality that is still missing and which you aspect you did not manage to evaluate.

# 3rd Delivery

## Comments received during the 2nd presentation

We have presented our idea to our IoT class and the main critiques were:

1. An advice that professors gave us is to improve our solution for the covid-19 problem. So takint into account not only the number of people present in each section of the musem but also the respect of the distance between people. We decided to follow this advice and try this difficult challenge.

2. We used Bluetooth beacons, but we want to underline the fact that our beacons are not passive, so we called them beacon in an unproper way. The iot boards are active components of our project infact they communicates with the smartphones and with the cloud infrastructure.

## Our solution

Taking into account these useful advices and critiques, we came out with the following solutions:

1. We really appreciated the advice that professors gave us, in fact we decided to include some features to address the problem of guided visits in these times in which sections cannot be overcrowded.
2. Our application uses Bluetooth beacons to monitor the tours that people makes in the museum.

## Changes from the 2nd delivery

The main changes from the first delivery are:

1. We decided to discard the idea of using a website, we have develeped instead a mobile application.

2. We faced the problem of social distancing because of the COVID-19 inside our mobile application and added that to our solution.

3. Since we have the possibility to test on a physical board we have changed our plans to evaluate our system.

## Technical work done so far

Our work, from a technical point of view up to now is:

1. We have implemented the cloud infrastructure to make the system work:

    1.1. We implemented a Database with all the necessary tables to mantain useful data to be processed by our system.

    1.2. We implemented a scoring algorithm that takes into account the similarity between recent visits and the current visit, and the number of people that is currently in each section.
2. We have a starting version of the web application that gives suggestion about the next room to visit, taking into account the taste of the visitor and the crowding situation in each section.

## Evaluation done so far

1. We have evaluated our system sending messages through LoRa and The Things Network. We started an experiment on Fit IoT lab, sending LoRa messages to TTN and then bridge them to IoT Hub every 5 seconds, that is a frequency that we do expect to be necessary to our system in the worst case. Monitoring messages incoming on Azure IoT hub for 10 minutes, we observed that we had about 60% packet loss, that for our system is absolutely not affordable. So, due to this and to the possibiliyt to get real boards we changed this part of the architecture trying to use MQTT.

## Evaluation to do

As our initial idea has changed a bit, like our current situation with the pandemic, we have to rethink about how to do a better and more precise evaluation:

1. We added some functionalities to the boards, so we have to test whether this is feasible. infact the boards in our plans have to communicate with each other to reach a consensus about the final list of devices in each section, moreover they have to send this list to the cloud, so, since we have only one avilable board, we plan to do a load test with an ad hoc MBED OS program that performs a simulation of 20 BLE devices in a single section. If the board can handle this load, looking a the space available in each section we can be happy about that. Otherwise the computation will be done using the computational power of the cloud.

2. We have to test whether our cloud architecture is efficient enough for our purposes, our target remains to manage 20 devices per room. So we will perform a simulation, through a Python script, sending data to the cloud and analyzing the behaviour of our algorithm, taking into account that saving data to the DB, from what we have experienced so far, is an important bottleneck

3. Evaluation of MQTT (we have to repeat a similar experiment using MQTT)
