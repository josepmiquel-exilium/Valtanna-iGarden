import network
import webrepl
import dht
import time
from machine import Pin
from machine import ADC
import config


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
sensor = dht.DHT11(Pin(14))

# initialize soil sensor on GPIO 34
soil_sensor = ADC(Pin(34))
soil_sensor.atten(ADC.ATTN_11DB)  # full range 0-3.3V
soil_sensor.width(ADC.WIDTH_10BIT)  # 10-bit resolution (0-1023)

def read_soil():
    value = soil_sensor.read()  # 0-1023
    # Convert to percentage (0=dry, 100=wet)
    percentage = (value / 1023) * 100
    percentage = round(percentage, 2)
    return value, percentage

def read_sensor():
    global temp, temp_percentage, hum, soil, soil_percentage
    temp = temp_percentage = hum = soil = soil_percentage = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        soil, soil_percentage = read_soil()
        
        if (isinstance(temp, (int, float)) and isinstance(hum, (int, float))):
            msg = (b'{0:3.1f},{1:3.1f},{2:3.1f}'.format(temp, hum, soil_percentage))
            temp_percentage = (temp + 6) / (40 + 6) * 100
            hum = round(hum, 2)
            return msg
        else:
            return 'Invalid sensor readings.'
    except OSError as e:
        return 'Failed to read sensor.'

def web_page():
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{padding: 20px; margin: auto; width: 50%; text-align: center;}}
    .progress{{background-color: #F5F5F5;}}
    .progress.vertical{{position: relative; width: 25%; height: 60%; display: inline-block; margin: 20px;}}
    .progress.vertical > .progress-bar{{width: 100% !important;position: absolute;bottom: 0;}}
    .progress-bar{{background: linear-gradient(to top, #f5af19 0%, #f12711 100%);}}
    .progress-bar-hum{{background: linear-gradient(to top, #9CECFB 0%, #65C7F7 50%, #0052D4 100%);}}
    .progress-bar-soil{{background: linear-gradient(to top, #00FF00 0%, #007700 100%);}}
    p{{position: absolute; font-size: 1.5rem; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 5;}}
    </style></head>
    <body>
    <h1>ValtANNA iGarden Temp</h1>

    <div class="progress vertical">
        <p>{temp}C</p>
        <div role="progressbar" style="height: {temp_percentage}%;" class="progress-bar"></div>
    </div>

    <div class="progress vertical">
        <p>{hum}%</p>
        <div role="progressbar" style="height: {hum}%;" class="progress-bar progress-bar-hum"></div>
    </div>

    <div class="progress vertical">
        <p>{soil_percentage}%</p>
        <div role="progressbar" style="height: {soil_percentage}%;" class="progress-bar progress-bar-soil"></div>
    </div>

    </body></html>
    """
    return html

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address
    s.bind(('', 80))
    s.listen(5)

    print("Server running on port 80...")
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        sensor_readings = read_sensor()
        print(sensor_readings)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

app()
