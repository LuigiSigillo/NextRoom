#ifndef __BLE_LED_SERVICE_H__
#define __BLE_LED_SERVICE_H__

#include <iostream>

class AddressService {
public:
    const static uint16_t LED_SERVICE_UUID              = 0xA000;
    const static uint16_t LED_STATE_CHARACTERISTIC_UUID = 0xA001;

    AddressService(BLEDevice &_ble, std::uint8_t* initialString) :
        ble(_ble), addressReadService(LED_STATE_CHARACTERISTIC_UUID, initialString)
    {
        GattCharacteristic *charTable[] = {&addressReadService};
        GattService         ledService(LED_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));

        ble.gattServer().addService(ledService);
    }

    GattAttribute::Handle_t getValueHandle() const
    {
        return addressReadService.getValueHandle();
    }

    void updateAddress(uint8_t* newAddress)
    {
        int i = 0;
        while(newAddress[i] != NULL)
        {
            currentAddress[i] = newAddress[i];
            i++;
        }
        ble.gattServer().write(
            addressReadService.getValueHandle(),
            currentAddress,
            5
        );
    }


private:
    BLEDevice                         &ble;
    uint8_t currentAddress[5];
    ReadOnlyArrayGattCharacteristic<uint8_t, 5> addressReadService;
};

#endif /* #ifndef __BLE_LED_SERVICE_H__ */
