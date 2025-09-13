# ValtANNA iGarden ESP32 Project

This project runs on an **ESP32** and monitors your garden conditions, including **temperature, humidity, and soil moisture**. It hosts a simple web server displaying live readings as vertical progress bars.

---

## Features

- Measures **temperature** (°C) and **humidity** (%) with a **DHT11 sensor**  
- Measures **soil moisture** (%) with a **capacitive soil moisture sensor v1.2**  
- Displays live readings on a **mobile-friendly web page**  
- Uses **ESP32 Wi-Fi** to serve the web interface  
- Fully implemented in **MicroPython**

---

## Hardware Required

- ESP32 development board  
- DHT11 temperature & humidity sensor  
- Capacitive soil moisture sensor v1.2  
- Jumper wires  

---

## Wiring

### DHT11
| Pin | ESP32 Connection |
|-----|-----------------|
| VCC | 3.3V            |
| GND | GND             |
| DATA| GPIO 14         |

### Soil Moisture Sensor
| Pin | ESP32 Connection |
|-----|-----------------|
| VCC | 3.3V            |
| GND | GND             |
| A0  | GPIO 34 (ADC)   |

> **Note:** Use 3.3V for safe operation on the ESP32 ADC pins.

---

## Software Setup

1. Install **MicroPython** on your ESP32  
2. Install **Thonny** or any compatible IDE  
3. Save `main.py` and `config.py` to your ESP32  
4. Edit `config.py` with your Wi-Fi credentials:

```python
WLAN_SSID = "your_wifi_name"
WLAN_PASSWORD = "your_wifi_password"
```

5. Run `main.py` on the ESP32

---

## Web Interface

- Access the ESP32 web server by entering its **IP address** in a browser  
- Displays:
  - Temperature (°C)
  - Humidity (%)
  - Soil moisture (%)
- Vertical progress bars indicate the level of each parameter

---

## File Structure

```
ESP32-iGarden/
│
├─ main.py          # Main MicroPython script
├─ config.py        # Wi-Fi credentials
├─ README.md        # Project documentation
```

---

## License

This project is released under the **MIT License**. Feel free to use and modify for personal projects.
