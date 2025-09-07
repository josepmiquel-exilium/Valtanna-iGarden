from machine import Pin, SoftI2C, RTC
import ssd1306
import utime

# Initialize I2C and OLED
i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize RTC
rtc = RTC()
# Optionally set the time: rtc.datetime((year, month, day, weekday, hour, minute, second, subsecond))
# Example: rtc.datetime((2025, 9, 7, 0, 14, 30, 0, 0))  # Only if RTC isn't set yet

def update_display():
    lcd.fill(0)  # Clear display
    lcd.text("ValtAnna", 30, 10)
    lcd.text("Garden <3", 30, 25)
    
    # Get current time
    dt = rtc.datetime()
    time_str = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    date_str = "{:04d}-{:02d}-{:02d}".format(dt[0], dt[1], dt[2])
    
    lcd.text(date_str, 10, 40)
    lcd.text(time_str, 10, 52)
    lcd.show()

try:
    while True:
        update_display()
        utime.sleep(1)  # Update every second
except KeyboardInterrupt:
    lcd.fill(0)
    lcd.show()
    print("Display cleared")
