#define logMessage printf
#include "mbed.h"
#include "MyWiFi.h"
#include "MyMQTT.h"
#include "ble/BLE.h"


#if (defined(TARGET_DISCO_L475VG_IOT01A))
ISM43362Interface wifi(MBED_CONF_APP_WIFI_SPI_MOSI, MBED_CONF_APP_WIFI_SPI_MISO, MBED_CONF_APP_WIFI_SPI_SCLK, MBED_CONF_APP_WIFI_SPI_NSS, MBED_CONF_APP_WIFI_RESET, MBED_CONF_APP_WIFI_DATAREADY, MBED_CONF_APP_WIFI_WAKEUP, false);
#endif

#define DEVICE_NAME "Room1"


int main()
{
    MyWiFi myWifi(wifi);

    if(myWifi.connect_to_wifi() == 0)
        logMessage("Success\n");
    else
        logMessage("Something went wrong\n");

    set_time(1256729737);  // Set RTC time to Wed, 28 Oct 2009 11:35:37
   
    MyMQTT myMqtt(wifi);
    myMqtt.sendMessages();
}
