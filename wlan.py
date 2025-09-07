import network
import time
import config

# Replace with your Wi-Fi credentials
SSID = config.SSID
PASSWORD = config.PASSWORD

# Create a WLAN station interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Enable the interface

# Connect to Wi-Fi
wlan.connect(SSID, PASSWORD)

# Wait for connection
timeout = 10  # seconds
for i in range(timeout):
    if wlan.isconnected():
        break
    print("Connecting...")
    time.sleep(1)

if wlan.isconnected():
    print("Connected!")
    print("IP address:", wlan.ifconfig()[0])
else:
    print("Failed to connect")