#include "MyMQTT.h"

MyMQTT::MyMQTT(ISM43362Interface& wifi): m_wifi(wifi), m_network(&wifi), m_mqttNetwork(m_network), m_client(m_mqttNetwork), m_version(0.6){
        m_topic = "devices/simulated/messages/events/"; 
        connect_to_mqtt();
    }

void MyMQTT::messageArrived(MQTT::MessageData& md)
    {
        MQTT::Message &message = md.message;
        logMessage("Message arrived: qos %d, retained %d, dup %d, packetid %d\r\n", message.qos, message.retained, message.dup, message.id);
        logMessage("Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
    }

int MyMQTT::subscribe(){
    int rc;
    if ((rc = m_client.subscribe(m_topic, MQTT::QOS2, messageArrived) != 0))
        logMessage("rc from MQTT subscribe is %d\r\n", rc);
    else
        return 1;
    
    return 0;
}

void MyMQTT::connect_to_mqtt(){
    printf("HelloMQTT: version is %.2f\r\n", m_version);

    const char* hostname = "192.168.1.180";
    int port = 1883;
    printf("Connecting to %s:%d\r\n", hostname, port);
    int rc = m_mqttNetwork.connect(hostname, port);
    if (rc != 0)
        printf("rc from TCP connect is %d\r\n", rc);
    
    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
    data.clientID.cstring = DEVICE_NAME;
    
    
    data.username.cstring = DEVICE_NAME;
    if ((rc = m_client.connect(data)) != 0) {
        printf("rc from MQTT connect is %d\r\n", rc);
    }
    printf("connesso\n");
}

void MyMQTT::set_topic(char* topic){
        m_topic = topic;
        subscribe();
    }

void MyMQTT::sendMessages(){
        MQTT::Message message;

        while(1) {
            /*/////////////////////////////////
            Detect data with BLE
            //////////////////////////////////*/
            //Get current timestamp
            time_t rawtime;
            struct tm * timeinfo;
            char timestamp[80];

            time (&rawtime);
            timeinfo = localtime(&rawtime);

            strftime(timestamp,sizeof(timestamp),"%m-%d-%Y %H:%M:%S",timeinfo);
            char buf[500];
            int n = snprintf(buf, sizeof(buf), "{'room1':{'timestamp':'10-28-2009 11:53:32','list_devices':{'s10':'20','iphone':'20'}}}");
            message.payload = reinterpret_cast<void*>(buf);
            message.payloadlen = n;
            message.qos = MQTT::QOS0;
            int rc = m_client.publish(m_topic, message);
            printf("publish exited with code %d\n", rc);
            printf("Published message: %s\n", message.payload);

            wait(30);


            n = snprintf(buf, sizeof(buf), "{'room1':{'timestamp':'10-28-2009 11:53:32','list_devices':{'s10':'20','iphone':'70'}},'room2':{'timestamp':'10-28-2009 11:57:32','list_devices':{'s10': '58','iphone':'20'}}}");
            message.payload = reinterpret_cast<void*>(buf);
            message.payloadlen = n;
            message.qos = MQTT::QOS0;
            rc = m_client.publish(m_topic, message);
            printf("publish exited with code %d\n", rc);
            printf("Published message: %s\n", message.payload);

            wait(30);


            n = snprintf(buf, sizeof(buf), "{'room1':{'timestamp':'10-28-2009 11:53:32','list_devices':{'s10':'20','iphone':'70'}},'room2':{'timestamp':'10-28-2009 11:57:32','list_devices':{'s10': '58','iphone':'80'}}, 'room3':{'timestamp':'10-28-2009 12:17:32','list_devices':{'s10': '100','iphone':'20'}}}");
            message.payload = reinterpret_cast<void*>(buf);
            message.payloadlen = n;
            message.qos = MQTT::QOS0;
            rc = m_client.publish(m_topic, message);
            printf("publish exited with code %d\n", rc);
            printf("Published message: %s\n", message.payload);

            wait(30);
        }

        m_mqttNetwork.disconnect();
    }