# 3rd Delivery

## Comments received during the 2nd presentation

We have presented our idea to our IoT class and the main critiques were:

1. An advice that professors gave us is to improve our solution for the covid-19 problem. So taking into account not only the number of people present in each section of the musem but also the respect of the distance between people. We decided to follow this advice and try this challenge.

## Our solution

Taking into account these useful advices and critiques, we came out with the following solutions:

1. We really appreciated the advice that professors gave us, we decided to include another feature to our application estimating the proximity of two different visitor and check if they are respecting the security distance.

## Changes from the 2nd delivery

The main changes from the second delivery are:

1. We decided to discard the idea of using a website, we have develeped instead a mobile application.

2. We faced the problem of social distancing, because of the COVID-19, inside our mobile application and added that to our project.

## Technical work done for the 3rd delivery

Our work, from a technical point of view done for the 3rd delivery:

1. We have finished the cloud infrastructure to make the system work:

    1.1. Now there is an endpoint reachable from the mobile application to connect to the cloud infrastructure also the smartphones.

    1.2. Fixed the type of messages that the board send to the IoT Hub.

2. We have finished the first version of the mobile application written in Flutter that gives suggestion about the next room to visit, taking into account the taste of the visitor and the crowding situation in each section.

## Evaluation done

1. We performed a load test, trying to understand the limitations of the BLE sensor of the board when multiple devices are detected, and the capability of the board of storing data that begins to grow in size. We used the same device to connect to the board within a short period of time before it sends the list of devices to the cloud and empties the list. The results that we obtained were pretty good because the board could send an MQTT message with an average of 14 session IDs with the current parameters.

2. We have done a load test with a python script program that performs a simulation of 20 BLE devices in a single section. If the board can handle this load, looking a the space available in each section we can be happy about that. Otherwise the computation will be done using the computational power of the cloud.

    Eventually we have tuned the time of the data collection to make the system efficient enough for our purposes. Our target remains to manage 15 devices per room.

    We discovered that saving data to the DB, is an important bottleneck, so we have decided to collect the data from the board at least every 30 seconds after the previous data collection.

    The graph below shows the tuning that we have done, starting from a high number of execution per minute and fixing this to 2 for minute as we have said.

    ![testcloud](Evaluation/Images/testing_cloud.jpg)

3. We have tested the feature that aim to calculate the distance between two visitor, as we expected is not too precise and this is due to the fact that every vendor use different bluetooth sensor on their smartphone, so the RSSI at one meter that is used to estimate the distance is not rigorous.

We had a lot of false positives during our test, becuase the apllication often claimed that  we were within 1 meter distance from another smartphone, but this was not true in every case. We decided to introduce a threshold, if we detect that two people are too near to each other for more than three times we would notice to them. In this way we find out that the system works better, but there are still to many case in which one person is keeping the distance between another but the system will notify them that they are too close.

We could try to improve our relevation system using some kind of triangulation if the we will place the board in some fixed position near the statue, but for the moment we are not expecting to do that.

## What we would like to implement in the future

* Improve the user experience of our application adding a map that shows the users current position and the position of the section/room suggested by the system
* Implement a curators dashboard to monitor the amount of people in each section and to better handle the people flow in the museum 
* Improve the accuracy of the estimated distance via Bluetooth adding other parameters than the RSSI

