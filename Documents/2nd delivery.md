# 2nd Delivery

## Comments received during the 1st presentation

We have presented our idea to our IoT class and the main critiques were:

1. We did not start from a problem to solve. We started with an IoT architecture that, does not completely solve a real problem
2. An advice that professors gave us is to take into account the current pandemic as a problem to solve for our application
3. We used Bluetooth beacons, like the majority of the class, so the class did already a discussion about this technology. The main problems are about the noise that the Bluetooth could introduce, putting many BLE devices close to each other.

## Our solution

Taking into account these useful advices and critiques, we came out with the following solutions:

1. We defined the problem of personalized tours in a better way than we did in the firts delivery, and asked to some friends of ours if this is percieved as a real problem. We know that this cannot be used as a good quality data for our purposes, but at least it is a beginning. The outcome of this little poll was quite positive, but we think that in a museum like the Sapienza "Museo dell'arte classica", because of its structure it is difficult to not see every section. This takes us to point 2.
2. We really appreciated the advice that professors gave us, in fact we decided to include some features to address the problem of guided visits in these times in which sections cannot be overcrowded. So we included a dashboard for the curators of the museum to monitor the people flow in the museum, and added features to try to equalize the number of people in each section.
3. Our application uses Bluetooth beacons to monitor the tours that people makes in the museum, so it is inevitable that our system has to face noisy data problems and false positives. In particular it could be that a board placed in section A recognizes a smartphone that actually is in section B, so also the board B detects the smartphone. Our idea is to make the boards communicate through MQTT before sending the final list of the current devices in each section to the cloud.

## Changes from the 1st delivery

The main changes from the first delivery are:

1. We faced the problem of the COVID-19 and limited accesses to the museum in our system and redifined our solution taking into account this factor.
2. After some tests we decided to discard the option to implement the communication between each board and Azure IoT Hub using LoRa. The test we have done to make this decision will be later described.
3. Since we have the possibility to test on a physical board we have changed our plans to evaluate our system. Indeed now we can do better evaluation tests, and discarded the possibility to use Fit IoT Lab mobile robots.

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
