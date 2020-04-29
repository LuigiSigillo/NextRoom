# Evaluation

This document defines how the evaluation of this project will be carried out. We will do considerations for both the technical point of view, and the user experience part.
 
## Why we must evaluate our system?
  
* To  determine its quality 
* To  find out improvement areas
 
## User point of view
    
### User experience evaluation:

Reveals how user feels about your design choices.
   
User experience:
   
* How a person feels about using a system 
* Beyond pragmatic utility and usability 
* Subjective, holistic, emotional, long-term
  
User Experience Evaluation Methods: 
  
* Understanding real users behaviors/needs evaluating their feedback
* Focus is to create a great user experience that allows the biggest number of people to use the application
* Feedbacks from a user experience evaluation can be used as input for the next phase of improvement of the application
      
 #### How to evaluate user experience?
 
 There are a lot of methods to evaluate user experince Also techniques that help to collect experiential data such as 
 
* questionnaires
* self-reporting during visiting
* observing
* etc

For this project we decided to gather data, in an anonimously way, from user application on how much time they spend in each section and how much time they visited all part in the museum.

For example:

![chart](Images/chart.png)

![chart](Images/chart2.png)

We thought that in a real scenario we could use these data, and create a score based on how much time a user spends in the suggested section of the museum. But due to the current lockdown, and to our difficulty on testing the application in a real scenario, this evaluation becomes complex.
So we will evaluate the user experience using mockups, and after every demo of these prototypes we will collect people's opinions asking for feedbacks, trying to improve UX and to make our application more and more interactive.
The questions will be mainly on the User interface and on the services that the application will provide. If we will add some new feature to the application we will ask the user if this could be used or if it could be an interesting thing to add.

## Technical point of view
 
### We first have to know which product we will provide to the end user and understand on what scale the project is feasible
      
The evaluation of the technical part is fundamental for the evaluation of the entire system, because its main goal is to understand the behaviour of the system under real use cases. From these data it is possible to understand if the project is feasible in a real-world scenario. In our case this evaluation will be carried on to understand if it is possible for the system to handle a sufficent number of users to be installed in the Sapienza Museum.

### How to evaluate the technical part?

To evaluate the system from a technical point of view the main thing that we can do is to do tests on the maximum load that it can handle. This operation, to better understand the performances of the single parts of the system, can be carried on each of them. So in an ideal situation we would have done some load tests on:
* **BLE** IoT device-Smartphone interation: how many smartphones a single device can handle?
* **Cloud** IoT device-Cloud interation: what is the message rate with which the device can send messages to Azure IoT hub?
* **Responsiveness** Cloud-Smartphone interation: how fast the smatphone receives the advice on where to go, does it depend from the number of connected devices?

The evaluation of the technical part, due to the current situation is something that is not very simple. On a real test we could imagine to create some controlled scenarios with few devices per section, and test the above features. For now we can only perform these opereations on the single components of our system (using simulations) and identify the bottleneck. Once the bottleneck is identified we will have an estimation of the number of devices that the system can handle at the same time. We think that, to begin, 15 devices could be a good number.
