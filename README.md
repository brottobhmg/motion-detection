# motion-detection
Using ESP32-CAM combined with a Python script to detect movement and send an alert via Telegram.
An alert will be sent only if the device with the specified macs is not in range of the device on which the python script is running (I use the Raspberry and the ESP in the same room, so this allows me to avoid false positives).

## Configuration

1. Arduino code:
    - replace the placeholder with your wifi credential on `const char* ssid = "YOUR_SSID";` and `const char* password = "YOUR_PASSWORD";`.
2. Python code:
    - `main.py`: replace with your bot credential on `TELEGRAM_TOKEN = 'YOUR_TOKEN'` and `CHAT_ID = 'YOUR_CHATID'`.
    - `find_device.py`: replace with the mac's device target on `target_mac_bt = "YOUR_MAC_DEVICE_BLUETOOTH"` and `target_mac = "YOUR_MAC_DEVICE_WIFI"`.

## Device used

- AI Thinker ESP32 CAM
- Raspberry Pi 4B

