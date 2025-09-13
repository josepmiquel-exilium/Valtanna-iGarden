from machine import ADC, Pin
import time

soil_sensor = ADC(Pin(34))
soil_sensor.atten(ADC.ATTN_11DB)
soil_sensor.width(ADC.WIDTH_10BIT)

while True:
    print(soil_sensor.read())
    time.sleep(1)