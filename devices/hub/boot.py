from shared import network

# setup wifi to network
WIFI_SSID = ""  # WiFi SSID
WIFI_PASS = ""  # Wifi Password

network.connect_to_wifi(ssid=WIFI_SSID, password=WIFI_PASS)
