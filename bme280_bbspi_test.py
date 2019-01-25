import bbspi
from bme280_bbspi import BME280

print("Testing BME280 BBSPI interface")

bbspi.open(cs=26, miso=20, mosi=21, sclk=16, baud=115200, flags=0)
sensor = BME280(26)
sensor.begin()

print('Temperature: {0}\nHumidity: {1}\nPressure: {2}\n'.format(sensor.temperature, sensor.humidity, sensor.pressure))

bbspi.close(cs=26)
