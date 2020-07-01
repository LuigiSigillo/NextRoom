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

For this project we decided to gather data, in an anonimous way, from user application on how much time they spend in each section and how much time they visited all parts in the museum.

For example:

![chart](Images/chart.png)

![chart](Images/chart2.png)

We thought that in a real scenario we could use these data, and create a score based on how much time a user spends in the suggested section of the museum. But due to the current lockdown, and to our difficulty on testing the application in a real scenario, this evaluation becomes complex.
So we will evaluate the user experience using mockups, and after every demo of these prototypes we will collect people's opinions asking for feedbacks and offering the possibility to interact with us through some forms to be compiled , trying to improve UX and to make our application more and more interactive.
The questions will be mainly on the User interface and to test the services that the application will provide.

## Technical point of view

The evaluation of the technical part is fundamental for the evaluation of the entire system, because its main goal is to understand the behaviour of the system under real use cases. From these data it is possible to understand if the project is feasible in a real-world scenario. In our case this evaluation will be carried on to understand if it is possible for the system to handle a sufficent number of users present at the same time in the Sapienza "Museo dell'Arte Classica".

### How we will evaluate the technical part

To evaluate the system from a technical point of view the main thing that we can do is to do tests on the maximum load that it can handle. This operation, to better understand the performances of the single parts of the system, can be carried on each of them. So in an ideal situation we would have done some load tests on:

* **BLE** IoT device-Smartphone interation: how many smartphones a single device can handle?
  * For this part of the system we have to take into account the possible noise that there could be into sections due to the presence of different IoT devices in the range of each other.  
  * Due to this noise we could have some missclassifications that could influence the suggestions and the responsiveness of our application.
  * To provide a solution to these noisy data, the boards in our plans have to communicate with each other to reach a consensus about the final list of devices in each section, moreover they have to send this list to the cloud, so, since we have only one available board, we plan to do a load test with an ad hoc MBED OS program that performs a simulation of 20 BLE devices in a single section. If the board can handle this load, looking a the sapce available in each section we can be happy about that.
* **Cloud** IoT device-Cloud interation: what is the message rate with which the device can send messages to Azure IoT hub?
We have to test whether our cloud architecture is efficient enough for our purposes, our target remains to manage 20 devices per room. So we will perform a simulation, through a Python script, sending data to the cloud and analyzing the behaviour of our algorithm, taking into account that saving data to the DB, from what we have experienced so far, is an important bottleneck.
* **Responsiveness** Cloud-Smartphone interation: how fast the smartphone receives the advice on where to go, does it depend from the number of connected devices?

We will create some controlled scenarios with few devices per section, and test the above features. For now we can only perform these opereations on the single components of our system (using simulations) and identify the bottleneck. Once the bottleneck is identified we will have an estimation of the number of devices that the system can handle at the same time. We think that, to begin, 20 devices could be a good number.

### Pricing evaluation

The first cost to take into account is the board one; we know that it's necessary to place at least one board for each section of the museum. Looking at the [map](Images/planimetry.jpg) of the musem we see clearly twenty rooms. The board that we will use is the [B-L475E-IOT01A Discovery kit](https://www.st.com/en/evaluation-tools/b-l475e-iot01a.html) that has a retail price of about 50€. Altough the museum could have twenty rooms, but only ten sections or less; considering at least two rooms per section, the estimated cost will be around 500€.

For what concerns the cloud architecture these are the estimated costs:
![pricing](Images/pricing.jpg)

* Azure Function: the first 400,000 GB/s of execution and 1,000,000 executions are free. Then you pay what you consume (serverless)

* App service: The basic plan cost around 60€, for testing purpose we will use the free one.

* Azure SQL Database: We choose to use the serverless option also in the DB, we use the maximum size of 15GB but it is possible to use more space.

So the expected monthly cost is around 60€, with the one time cost of the board purchase.

Below a graph explaining the power,in term of saving money, of the serverless choice:
![serverless](Images/serverless-billing.png)
