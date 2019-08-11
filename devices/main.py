from shared.controller_esp32 import ESP32Controller
from shared.sx127x import SX127x

device_type = 'hub'  # hub | node


def main():
    controller = ESP32Controller()
    lora = controller.add_transceiver(SX127x(name='LoRa'),
                                      pin_id_ss=ESP32Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone=ESP32Controller.PIN_ID_FOR_LORA_DIO0)
    if device_type == 'hub':
        # do hubby things
        print('initiating device type: hub')
    elif device_type == 'node':
        # do nodey things
        print('initiating device type: hub')
    else:
        raise Exception('device type must be set and be one of: (hub or node)')


if __name__ == '__main__':
    main()
