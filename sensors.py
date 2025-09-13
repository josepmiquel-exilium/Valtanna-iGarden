from machine import Pin
from machine import ADC
import dht


sensor = dht.DHT11(Pin(14))

# initialize soil sensor on GPIO 34
soil_sensor = ADC(Pin(34))
soil_sensor.atten(ADC.ATTN_11DB)  # full range 0-3.3V
soil_sensor.width(ADC.WIDTH_10BIT)  # 10-bit resolution (0-1023)

# Soil sensor calibration
wet_value = 293   # Adjust after testing
dry_value = 646   # Adjust after testing

def read_soil():
    value = soil_sensor.read()
    print("Raw soil value:", value)  # DEBUG
    
    # Clamp value between dry and wet
    value = min(max(value, wet_value), dry_value)
    
    # Map to percentage (100% = wet, 0% = dry)
    percentage = (value - dry_value) / (wet_value - dry_value) * 100
    percentage = round(percentage, 2)
    
    return value, percentage

def read():
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
