#define logMessage printf
#include "TCPSocket.h"
#include "VL53L1X.h"
#include <string> 

#if (defined(TARGET_DISCO_L475VG_IOT01A))
#include "ISM43362Interface.h"
#endif

class MyWiFi
{
    private:
    ISM43362Interface& m_wifi;

    public:
    MyWiFi(ISM43362Interface& wifi);
    private:

    const char *sec2str(nsapi_security_t sec);
    int scanner(WiFiInterface *wifi);

    public:
    int connect_to_wifi();
};
