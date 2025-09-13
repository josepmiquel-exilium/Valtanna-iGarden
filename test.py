import network
import webrepl
import time
from machine import ADC
import config
import webpage
import sensors
import forecast


try:
  import usocket as socket
except:
  import socket

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = config.WLAN_SSID
PASSWORD = config.WLAN_PASSWORD


def do_connect(ssid, psw, timeout=20000):
    import network, time
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    print("Connecting to Wi-Fi:", ssid)
    wlan.connect(ssid, psw)
    start = time.ticks_ms()
    
    while not wlan.isconnected():
        try:
            time.sleep(1)
        except OSError as e:
            print("Wi-Fi error:", e)
            wlan.active(False)
            time.sleep(1)
            wlan.active(True)
            wlan.connect(ssid, psw)
        if time.ticks_ms() - start > timeout:
            raise OSError("Wi-Fi connection timeout")
    
    print("Connected, network config:", wlan.ifconfig())
    return wlan

def connect():
 do_connect(SSID,PASSWORD)

def app():
    connect()
    sensors.read()  # dummy read to stabilize sensors
    time.sleep(1)   # optional small delay
    forecast.check()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)

    print("Server running on port 80...")

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))

            request = conn.recv(1024)  # Read client request
            print('Request = %s' % str(request))

            # Read sensor data
            sensor_readings = sensors.read()
            
            if isinstance(sensor_readings, bytes):
                temp, hum, soil_percentage = [float(x) for x in sensor_readings.decode().split(',')]
            else:
                # fallback in case of error
                temp = hum = soil_percentage = 0

            print(f"Sensor readings - Temp: {temp}, Hum: {hum}, Soil: {soil_percentage}")
            
                        # Get rain forecast
            rain_today, rain_tomorrow = forecast.check()

            # Generate the HTML page with sensor data + rain info
            response = webpage.view(temp, hum, soil_percentage, rain_today, rain_tomorrow)


            # Send HTTP response
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response.encode('utf-8'))

        except Exception as e:
            print('Error:', e)
        finally:
            conn.close()

app()