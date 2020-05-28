#define logMessage printf
#define MQTTCLIENT_QOS2 1

#include "MQTTNetwork.h"
#include "MQTTmbed.h"
#include "MQTTClient.h"

#include <ctime>

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
    MyMQTT(ISM43362Interface& wifi);
    
    private:
    static void messageArrived(MQTT::MessageData& md);
    int subscribe();
    void connect_to_mqtt();
    
    public:
    void set_topic(char* topic);
    void sendMessages();
};