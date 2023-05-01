from machine import Pin
import RGB1602
import utime
import network
import urequests
import math
def load():
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.printout('Loading...')
    lcd.setCursor(0,1)
    lcd.printout('Please wait.')
def speak(x, y):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.printout(x)
    lcd.setCursor(0,1)
    lcd.printout(y)
def switch():
    global index
    if index < 6:
        index += 1
    elif index == 6:
        index = 0
def convertDay(x):
    if x == 0:
        response = 'Sunday'
        return response
    elif x == 1:
        response = 'Monday'
        return response
    elif x == 2:
        response = 'Tuesday'
        return response
    elif x == 3:
        response = 'Wednesday'
        return response
    elif x == 4:
        response = 'Thursday'
        return response
    elif x == 5:
        response = 'Friday'
        return response
    elif x == 6:
        response = 'Saturday'
        return response
t=0        
colorR = 64
colorG = 128
colorB = 64
index = 0
lcd=RGB1602.RGB1602(16,2)
lcd.clear()
ssid = 'Wifi SSID'
password = 'Wifi Password'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
connectCount = 0
max_wait = 10
load()
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    speak('Connecting to', 'the internet...')
    utime.sleep(1)
if wlan.status() != 3:
    speak('Connection', 'failed!')
    raise RuntimeError('network connection failed')
else:
    speak('Connected!','')
while True:
    api_key = "OpenWeatherMap API Key"
    location = "Province"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(location, api_key)
    response = urequests.get(url)
    data = response.json()
    temperature_k = data["main"]["temp"]
    temperature_f = (temperature_k - 273.15) * 1.8 + 32
    feels_like_k = data["main"]["feels_like"]
    feels_like_f = (feels_like_k - 273.15) * 1.8 + 32
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]
    r = int((abs(math.sin(3.14*t/180)))*255)
    g = int((abs(math.sin(3.14*(t+60)/180)))*255)
    b = int((abs(math.sin(3.14*(t+120)/180)))*255)
    t = t + 12
    lcd.setRGB(r,g,b)
    r = urequests.get('http://worldtimeapi.org/api/ip')
    result = str(r.content)
    startTime = result[int(result.find("datetime")) + 11:30 + result.find("datetime")]
    dayRaw = result[int(result.find("day_of_week"))+13]
    dayRaw = int(dayRaw)
    hours = startTime[11:13]
    realTime = int(startTime[11:13])
    hours = int(hours)
    signature = 'AM'
    newTime = startTime[11:16]
    if hours > 12 and hours != 0:
        hours -= 12
        newTime = newTime.replace(startTime[11:13],str(hours),1)
        signature = 'PM'
    elif hours == 0:
        hours += 12
        newTime = newTime.replace(startTime[11:13],str(hours),1)
    if index == 0:
        speak('Today is', str(convertDay(dayRaw)))
    elif index == 1:
        if realTime <= 6:
            speak('Good (Early)', 'Morning!')
        elif realTime <= 10:
            speak('Good Morning!','')
        elif realTime <= 16:
            speak('Good Afternoon!','')
        elif realTime <= 19:
            speak('Good Evening!','')
        else:
            speak('Good Night.','')
    elif index == 2:
        speak(str(startTime[0:10]), f'{str(newTime)} {signature}')
    elif index == 3:
        speak("Temperature:", "{:.2f} F".format(temperature_f))
    elif index == 4:
        speak("Feels like:", "{:.2f} F".format(feels_like_f))
    elif index == 5:
        speak("Humidity:", "{} %".format(humidity))
    elif index == 6:
        speak("Weather:", "{}".format(weather_description))
    utime.sleep(10)
    switch()
