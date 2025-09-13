import urequests
import ujson
import time
import config

def check():
    url = config.FORESTCAST_API
    try:
        response = urequests.get(url)
        data = ujson.loads(response.text)
        response.close()
    except Exception as e:
        print("Error fetching weather:", e)
        return False, False  # default to no rain if request fails

    daily = data.get('daily', {})
    dates = daily.get('time', [])
    precipitation = daily.get('precipitation_sum', [])

    if not dates or not precipitation:
        print("No precipitation data available")
        return False, False

    # Today's and tomorrow's date
    t = time.localtime()
    today_str = "{:04}-{:02}-{:02}".format(t[0], t[1], t[2])
    tomorrow_day = t[2] + 1
    # handle month-end simplistically (ESP32 may not have full datetime library)
    if tomorrow_day > 31:
        tomorrow_day = 1
    tomorrow_str = "{:04}-{:02}-{:02}".format(t[0], t[1], tomorrow_day)

    rain_today = False
    rain_tomorrow = False

    for i, date in enumerate(dates):
        if date == today_str and precipitation[i] > 0:
            rain_today = True
        if date == tomorrow_str and precipitation[i] > 0:
            rain_tomorrow = True
    
    return rain_today, rain_tomorrow