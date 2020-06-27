#if (defined(TARGET_DISCO_L475VG_IOT01A))
#include "ISM43362Interface.h"
#endif

static ISM43362Interface wifi(false);

class MyWiFi
{
private:
    const char *sec2str(nsapi_security_t sec)
    {
        switch (sec) {
            case NSAPI_SECURITY_NONE:
                return "None";
            case NSAPI_SECURITY_WEP:
                return "WEP";
            case NSAPI_SECURITY_WPA:
                return "WPA";
            case NSAPI_SECURITY_WPA2:
                return "WPA2";
            case NSAPI_SECURITY_WPA_WPA2:
                return "WPA/WPA2";
            case NSAPI_SECURITY_UNKNOWN:
            default:
                return "Unknown";
        }
    }

    int scanner(ISM43362Interface& wifi)
    {
        WiFiAccessPoint *ap;

        printf("Scan:\n");

        int count = wifi.scan(NULL,0);

        if (count <= 0) {
            printf("scan() failed with return value: %d\n", count);
            return 0;
        }

        /* Limit number of network arbitrary to 15 */
        count = count < 15 ? count : 15;

        ap = new WiFiAccessPoint[count];
        count = wifi.scan(ap, count);

        if (count <= 0) {
            printf("scan() failed with return value: %d\n", count);
            return 0;
        }

        for (int i = 0; i < count; i++) {
            printf("Network: %s secured: %s BSSID: %hhX:%hhX:%hhX:%hhx:%hhx:%hhx RSSI: %hhd Ch: %hhd\n", ap[i].get_ssid(),
                sec2str(ap[i].get_security()), ap[i].get_bssid()[0], ap[i].get_bssid()[1], ap[i].get_bssid()[2],
                ap[i].get_bssid()[3], ap[i].get_bssid()[4], ap[i].get_bssid()[5], ap[i].get_rssi(), ap[i].get_channel());
        }
        printf("%d networks available.\n", count);

        delete[] ap;
        return count;
    }

public:
    int connect_to_wifi(){
        int count = scanner(wifi);
        if (count == 0) {
            printf("No WIFI APs found - can't continue further.\n");
            return -1;
        }

        printf("\nConnecting to %s...\n", MBED_CONF_APP_WIFI_SSID);
        int ret = wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
        if (ret != 0) {
            printf("\nConnection error: %d\n", ret);
            return -1;
        }

        printf("Success\n\n");
        return 0;
    }
};