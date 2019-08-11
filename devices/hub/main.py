def main():
    controller = ESP32Controller()
    lora = controller.add_transceiver(SX127x(name='LoRa'),
                                      pin_id_ss=ESP32Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone=ESP32Controller.PIN_ID_FOR_LORA_DIO0)


if __name__ == '__main__':
    main()
