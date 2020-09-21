#include <events/mbed_events.h>
#include <mbed.h>
#include "ble/BLE.h"
#include "AddressService.h"
#include "pretty_printer.h"
#include <iostream>
#include "string.h"
#include "dictionary.h"

#define DEVICE_NAME "Room1"


static EventQueue event_queue(10 * EVENTS_EVENT_SIZE);

class MyBLE : ble::Gap::EventHandler {
public:
    MyBLE(BLE &ble, events::EventQueue &event_queue) :
        _ble(ble),
        _event_queue(event_queue),
        _led(LED1, 0),
        _led_uuid(AddressService::LED_SERVICE_UUID),
        _led_service(NULL),
        _adv_data_builder(_adv_buffer),
        _counter(0)
        {
            m_present_devices = (dictionary_t*)malloc(sizeof(dictionary_t));
            m_present_devices->size = 0;
        }

    ~MyBLE() {
        delete _led_service;
    }

    void start() {
        _ble.gap().setEventHandler(this);

        _ble.init(this, &MyBLE::on_init_complete);

        _event_queue.dispatch_forever();
    }

    dictionary_t* present_devices()
    {
        return m_present_devices;
    }

private:
    /** Callback triggered when the ble initialization process has finished */
    void on_init_complete(BLE::InitializationCompleteCallbackContext *params) {
        if (params->error != BLE_ERROR_NONE) {
            printf("Ble initialization failed.");
            return;
        }
        uint8_t initialString[5] = "";
        _led_service = new AddressService(_ble, initialString);

        _ble.gattServer().onDataWritten(this, &MyBLE::on_data_written);

        print_mac_address();

        start_advertising();
    }

    void start_advertising() {
        /* Create advertising parameters and payload */
        ble::AdvertisingParameters adv_parameters(
            ble::advertising_type_t::CONNECTABLE_UNDIRECTED,
            ble::adv_interval_t(ble::millisecond_t(1000))
        );

        _adv_data_builder.setFlags();
        _adv_data_builder.setLocalServiceList(mbed::make_Span(&_led_uuid, 1));
        _adv_data_builder.setName(DEVICE_NAME);

        /* Setup advertising */

        ble_error_t error = _ble.gap().setAdvertisingParameters(
            ble::LEGACY_ADVERTISING_HANDLE,
            adv_parameters
        );

        if (error) {
            printf("_ble.gap().setAdvertisingParameters() failed\r\n");
            return;
        }

        error = _ble.gap().setAdvertisingPayload(
            ble::LEGACY_ADVERTISING_HANDLE,
            _adv_data_builder.getAdvertisingData()
        );

        if (error) {
            printf("_ble.gap().setAdvertisingPayload() failed\r\n");
            return;
        }

        /* Start advertising */

        error = _ble.gap().startAdvertising(ble::LEGACY_ADVERTISING_HANDLE);

        if (error) {
            printf("_ble.gap().startAdvertising() failed\r\n");
            return;
        }
    }


    /**
     * This callback allows the LEDService to receive updates to the ledState Characteristic.
     *
     * @param[in] params Information about the characterisitc being updated.
     */
    void on_data_written(const GattWriteCallbackParams *params) {
        cout << "ciao" << endl;
        int i = 0;
        while((params->data[i]) != NULL)
        {
            cout << unsigned((params->data)[i]);
            i++;
        }
        cout << endl;
    }


private:
    /* Event handler */
    void onConnectionComplete(const ble::ConnectionCompleteEvent& event) {
        uint8_t address[5];
        std::copy(event.getPeerAddress().data(), event.getPeerAddress().data()+event.getPeerAddress().size(), address);
        _led_service->updateAddress((uint8_t*)address);
        char* mac_address = address_to_string(address);
        int i = m_present_devices -> size;
        m_present_devices -> dict[i].key = mac_address;
        m_present_devices -> dict[i].value = event.getConnectionInterval().value();
        m_present_devices -> size++;
    }

    char* address_to_string(uint8_t* address)
    {
        char* string = (char*)malloc(50 * sizeof(char));
        sprintf(string, "%u:%u:%u:%u:%u",address[0],address[1],address[2],address[3],address[4]);

        return string;
    }



    void onDisconnectionComplete(const ble::DisconnectionCompleteEvent&) {
        _ble.gap().startAdvertising(ble::LEGACY_ADVERTISING_HANDLE);
    }

private:
    BLE &_ble;
    events::EventQueue &_event_queue;
    DigitalOut _led;

    UUID _led_uuid;
    AddressService *_led_service;

    uint8_t _adv_buffer[ble::LEGACY_ADVERTISING_MAX_SIZE];
    ble::AdvertisingDataBuilder _adv_data_builder;
    dictionary_t* m_present_devices;

    int _counter;
};

/** Schedule processing of events from the BLE middleware in the event queue. */
void schedule_ble_events(BLE::OnEventsToProcessCallbackContext *context) {
    event_queue.call(Callback<void()>(&context->ble, &BLE::processEvents));
}