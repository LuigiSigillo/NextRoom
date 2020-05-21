# Evaluation

This document defines how the evaluation of this project will be carried out. We will do considerations for both the technical point of view, and the user experience part.

## User point of view

### User experience evaluation

Reveals how user feels about your design choices.

User experience:

* How a person feels about using a system 
* Beyond pragmatic utility and usability 
* Subjective, holistic, emotional, long-term

### How we will evaluate user experience

 There are a lot of methods to evaluate user experience; techniques that help to collect experiential data such as:

* questionnaires
* self-reporting during visiting
* observing
* etc...

For this project we decided to gather data, in an anonimous way, from user application on how much time they spend in each section and how much time they visited all parts in the museum.

For example:

![chart](Images/chart.png)

![chart](Images/chart2.png)

We thought that in a real scenario we could use these data, and create a score based on how much time a user spends in the suggested section of the museum. But due to the current lockdown, and to our difficulty on testing the application in a real scenario, this evaluation becomes complex.
So we will evaluate the user experience using mockups, and after every demo of these prototypes we will collect people's opinions asking for feedbacks and offering the possibility to provide advices through some forms to be compiled , trying to improve UX and to make our application more and more interactive.
The questions will be mainly on the User interface and on the services that the application will provide. If we will add some new features to the application we will ask the users if this could be useless or if it could be an interesting thing to add.

## Technical point of view

The evaluation of the technical part is fundamental for the evaluation of the entire system, because its main goal is to understand the behaviour of the system under real use cases. From these data it is possible to understand if the project is feasible in a real-world scenario. In our case this evaluation will be carried on to understand if it is possible for the system to handle a sufficent number of users present at the same time in the Sapienza "Museo dell'Arte Classica".

### How we will evaluate the technical part

To evaluate the system from a technical point of view the main thing that we can do is to do tests on the maximum load that it can handle. This operation, to better understand the performances of the single parts of the system, can be carried on each of them. So in an ideal situation we would have done some load tests on:

* **BLE** IoT device-Smartphone interation: how many smartphones a single device can handle?
    * For this part of the system we have to take into account the possible noise that there could be into sections due to the presence of different IoT devices in the range of each other.  
    * Due to this noise we could have some missclassifications that could influence the suggestions and the responsiveness of our application.
    * So it is very important to test how annoying this noise can be in our context, so due to our lockdown situation and the unavailability of a real test in the museum we will try to use some mobile robots available in Fit IoT lab as described [here](https://www.iot-lab.info/tutorials/robots-circuit-m3/), simulating the IoT sensor and the user with his smartphone, and will collect data to compare with the average square area of the section in the museum in order to get some feedbacks about this.
* **Cloud** IoT device-Cloud interation: what is the message rate with which the device can send messages to Azure IoT hub?
* **Responsiveness** Cloud-Smartphone interation: how fast the smatphone receives the advice on where to go, does it depend from the number of connected devices?

The evaluation of the technical part, due to the current situation is something that is not very simple. On a real test we could imagine to create some controlled scenarios with few devices per section, and test the above features. For now we can only perform these opereations on the single components of our system (using simulations) and identify the bottleneck. Once the bottleneck is identified we will have an estimation of the number of devices that the system can handle at the same time. We think that, to begin, 15 devices could be a good number.
