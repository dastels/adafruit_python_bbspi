import bbspi
from bme280_bbspi import BME280

print("Testing BME280 BBSPI interface")

# cs = 26
spi = bbspi.BBSpi(clock=16, MOSI=21, MISO=20)
sensor = BME280(spi)
sensor.begin()

print('Temperature: {0:.2f}\nHumidity: {1:.2f}\nPressure: {2:.2f}\n'.format(sensor.temperature, sensor.humidity, sensor.pressure))
