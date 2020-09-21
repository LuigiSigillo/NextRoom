#define logMessage printf
#define MQTTCLIENT_QOS2 1

#include "MQTTNetwork.h"
#include "../MQTTmbed.h"
#include "../MQTTClient.h"

#include <ctime>
#include <iostream>

#if (defined(TARGET_DISCO_L475VG_IOT01A))
#include "ISM43362Interface.h"
#endif
#define DEVICE_NAME "Room1"

class MyMQTT
{
    private:
    char* m_topic;
    ISM43362Interface& m_wifi;
    NetworkInterface* m_network;
    MQTTNetwork m_mqttNetwork;
    MQTT::Client<MQTTNetwork, Countdown> m_client;
    float m_version;
    public:
    MyMQTT(ISM43362Interface& wifi): m_wifi(wifi), m_network(&wifi), m_mqttNetwork(m_network), m_client(m_mqttNetwork), m_version(0.6){
        m_topic = "devices/simulated/messages/events/"; 
        connect_to_mqtt();
    }
    
    private:
    static void messageArrived(MQTT::MessageData& md)
    {
        MQTT::Message &message = md.message;
        logMessage("Message arrived: qos %d, retained %d, dup %d, packetid %d\r\n", message.qos, message.retained, message.dup, message.id);
        logMessage("Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
    }

    int subscribe(){
        int rc;
        if ((rc = m_client.subscribe(m_topic, MQTT::QOS2, messageArrived) != 0))
            logMessage("rc from MQTT subscribe is %d\r\n", rc);
        else
            return 1;
        
        return 0;
    }

    void connect_to_mqtt(){
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
    
    public:
    void set_topic(char* topic){
        m_topic = topic;
        subscribe();
    }

    void sendMessage(dictionary_t* collected_devices){

        MQTT::Message message;

        //Get current timestamp
        time_t rawtime;
        struct tm * timeinfo;
        char timestamp[80];
        time (&rawtime);
        timeinfo = localtime(&rawtime);
        strftime(timestamp,sizeof(timestamp),"%m-%d-%Y %H:%M:%S",timeinfo);

        //Build message string
        char buf[500];
        int n = snprintf(buf, sizeof(buf), "{'%s':{'timestamp':'%s','list_devices':{", DEVICE_NAME, timestamp);
        int i = 0;
        while(i < collected_devices->size)
        {
            if(i != 0)
            {
                strcat(buf, ",");
                n++;
            }
            char new_device[30];
            int j = snprintf(new_device,sizeof(new_device), "'%s':'%d'", collected_devices->dict[i].key, collected_devices->dict[i].value);
            strcat(buf, new_device);
            n = n + j; 
            i++;
        }
        strcat(buf,"}}}");
        n = n + 3;

        //send message
        message.payload = reinterpret_cast<void*>(buf);
        message.payloadlen = n;
        message.qos = MQTT::QOS0;
        int rc = m_client.publish(m_topic, message);

        //reset the dictionary
        for(int i = 0; i<(collected_devices->size); i++)
        {
            collected_devices->dict[i].key = NULL;
            collected_devices->dict[i].value = NULL;
        }
        collected_devices->size = 0;


        printf("publish exited with code %d\n", rc);
        printf("Published message: %s\n", message.payload);
    }
};