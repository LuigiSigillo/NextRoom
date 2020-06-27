#include "mbed.h"
#include "MyBLE.h"
#include "MyMQTT.h"
#include "MyWiFi.h"
#include <iostream>
#include <ctime>


static void ble_callback(MyBLE* _my_ble)
{
    _my_ble->start();
}

int main()
{

    #ifdef MBED_MAJOR_VERSION
        printf("Mbed OS version %d.%d.%d\n\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
    #endif

    MyWiFi my_wifi;
    if(my_wifi.connect_to_wifi() != 0) return -1;

    Thread thread1;

    BLE &ble = BLE::Instance();
    ble.onEventsToProcess(schedule_ble_events);
    MyBLE _my_ble(ble, event_queue);

    thread1.start(callback(ble_callback, &_my_ble));

    MyMQTT myMqtt(wifi);

    int wait_time = 20;
    while(1)
    {
        wait(wait_time);
        myMqtt.sendMessage(_my_ble.present_devices());
    }

    printf("\nDone\n");
}
