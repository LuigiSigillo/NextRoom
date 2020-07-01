/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
