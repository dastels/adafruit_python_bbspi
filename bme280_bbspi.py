import time
import bbspi

# Registers

BME280_REGISTER_DIG_T1 = 0x88
BME280_REGISTER_DIG_T2 = 0x8A
BME280_REGISTER_DIG_T3 = 0x8C

BME280_REGISTER_DIG_P1 = 0x8E
BME280_REGISTER_DIG_P2 = 0x90
BME280_REGISTER_DIG_P3 = 0x92
BME280_REGISTER_DIG_P4 = 0x94
BME280_REGISTER_DIG_P5 = 0x96
BME280_REGISTER_DIG_P6 = 0x98
BME280_REGISTER_DIG_P7 = 0x9A
BME280_REGISTER_DIG_P8 = 0x9C
BME280_REGISTER_DIG_P9 = 0x9E

BME280_REGISTER_DIG_H1 = 0xA1
BME280_REGISTER_DIG_H2 = 0xE1
BME280_REGISTER_DIG_H3 = 0xE3
BME280_REGISTER_DIG_H4 = 0xE4
BME280_REGISTER_DIG_H5 = 0xE5
BME280_REGISTER_DIG_H6 = 0xE7

BME280_REGISTER_CHIPID = 0xD0
BME280_REGISTER_VERSION = 0xD1
BME280_REGISTER_SOFTRESET = 0xE0

BME280_REGISTER_CAL26 = 0xE1  # R calibration stored in 0xE1-0xF0

BME280_REGISTER_CONTROLHUMID = 0xF2
BME280_REGISTER_STATUS = 0XF3
BME280_REGISTER_CONTROL = 0xF4
BME280_REGISTER_CONFIG = 0xF5
BME280_REGISTER_PRESSUREDATA = 0xF7
BME280_REGISTER_TEMPDATA = 0xFA
BME280_REGISTER_HUMIDDATA = 0xFD

# Sampling rates

SAMPLING_NONE = 0b000
SAMPLING_X1   = 0b001
SAMPLING_X2   = 0b010
SAMPLING_X4   = 0b011
SAMPLING_X8   = 0b100
SAMPLING_X16  = 0b101

# Power modes

MODE_SLEEP  = 0b00
MODE_FORCED = 0b01
MODE_NORMAL = 0b11

# filter values

FILTER_OFF = 0b000
FILTER_X2  = 0b001
FILTER_X4  = 0b010
FILTER_X8  = 0b011
FILTER_X16 = 0b100

# Standby duration in ms

STANDBY_MS_0_5  = 0b000
STANDBY_MS_10   = 0b110
STANDBY_MS_20   = 0b111
STANDBY_MS_62_5 = 0b001
STANDBY_MS_125  = 0b010
STANDBY_MS_250  = 0b011
STANDBY_MS_500  = 0b100
STANDBY_MS_1000 = 0b101


class BME280(object):

    def __init__(self, spi):
        self._spi = spi
        self._calibration = {}
        self._meas_reg = {}
        self._hum_reg = {}
        self._config_reg = {}
        self._t_fine = 0

    def read8(self):
        buffer = [0]
        self_spi.read(buffer)
    def begin(self):
        # check if sensor, i.e. the chip ID is correct
        if bbspi.read8(self._cs, BME280_REGISTER_CHIPID) != 0x60:
            return False

        # reset the device using soft-reset
        # this makes sure the IIR is off, etc.
        bbspi.write8(self._cs, BME280_REGISTER_SOFTRESET, 0xB6)

        # wait for chip to wake up.
        time.sleep(0.300)

        # if chip is still reading calibration, delay
        while self._is_reading_calibration:
          time.sleep(0.100)

        self._read_coefficients() # read trimming parameters, see DS 4.2.2

        self.set_sampling() # use defaults

        time.sleep(0.100)

        return True


    def set_sampling(self, mode=MODE_NORMAL, temp_sampling=SAMPLING_X16, press_sampling=SAMPLING_X16, hum_sampling=SAMPLING_X16, filter_mode=FILTER_OFF, duration=STANDBY_MS_0_5):
        """Setup sensor with given parameters / settings

        mode -- the power mode to use for the sensor
        temp_sampling -- the temp samping rate to use
        press_sampling -- the pressure sampling rate to use
        hum_sampling -- the humidity sampling rate to use
        filter_mode -- the filter mode to use
        duration -- the standby duration to use
        """
        self._meas_reg['mode'] = mode
        self._meas_reg['osrs_t'] = temp_sampling
        self._meas_reg['osrs_p'] = press_sampling

        self._hum_reg['osrs_h'] = hum_sampling

        self._config_reg['filter'] = filter_mode
        self._config_reg['t_sb'] = duration
        self._config_reg['spi3w_en'] = 0


        # you must make sure to also set REGISTER_CONTROL after setting the
        # CONTROLHUMID register, otherwise the values won't be applied (see DS 5.4.3)
        bbspi.write8(self._cs, BME280_REGISTER_CONTROLHUMID, self._hum_reg['osrs_h'])
        bbspi.write8(self._cs, BME280_REGISTER_CONFIG, (self._config_reg['t_sb'] << 5) | (self._config_reg['filter'] << 3) | self._config_reg['spi3w_en'])
        bbspi.write8(self._cs, BME280_REGISTER_CONTROL, (self._meas_reg['osrs_t'] << 5) | (self._meas_reg['osrs_p'] << 3) | self._meas_reg['mode'])



    def _read_coefficients(self):
        """Reads the factory-set coefficients"""
        self._calibration['dig_T1'] = bbspi.read16_LE(self._cs, BME280_REGISTER_DIG_T1)
        self._calibration['dig_T2'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_T2)
        self._calibration['dig_T3'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_T3)

        self._calibration['dig_P1'] = bbspi.read16_LE(self._cs, BME280_REGISTER_DIG_P1)
        self._calibration['dig_P2'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P2)
        self._calibration['dig_P3'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P3)
        self._calibration['dig_P4'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P4)
        self._calibration['dig_P5'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P5)
        self._calibration['dig_P6'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P6)
        self._calibration['dig_P7'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P7)
        self._calibration['dig_P8'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P8)
        self._calibration['dig_P9'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_P9)

        self._calibration['dig_H1'] = bbspi.read8(self._cs, BME280_REGISTER_DIG_H1)
        self._calibration['dig_H2'] = bbspi.readS16_LE(self._cs, BME280_REGISTER_DIG_H2)
        self._calibration['dig_H3'] = bbspi.read8(self._cs, BME280_REGISTER_DIG_H3)
        self._calibration['dig_H4'] = (bbspi.read8(self._cs, BME280_REGISTER_DIG_H4) << 4) | (bbspi.read8(self._cs, BME280_REGISTER_DIG_H4+1) & 0xF)
        self._calibration['dig_H5'] = (bbspi.read8(self._cs, BME280_REGISTER_DIG_H5+1) << 4) | (bbspi.read8(self._cs, BME280_REGISTER_DIG_H5) >> 4)
        self._calibration['dig_H6'] = bbspi.read8(self._cs, BME280_REGISTER_DIG_H6)


    @property
    def _is_reading_calibration(self):
        """
        Return whether chip is busy reading cal data.
        """
        status = bbspi.read8(self._cs, BME280_REGISTER_STATUS)
        return (status & 1) != 0


    @property
    def temperature(self):
        """
        Returns the temperature from the sensor
        """

        adc_T = bbspi.read24(self._cs, BME280_REGISTER_TEMPDATA)
        if adc_T == 0x800000: # value in case temp measurement was disabled
            return None
        adc_T >>= 4

        var1 = ((((adc_T>>3) - (self._calibration['dig_T1'] <<1))) * (self._calibration['dig_T2'])) >> 11

        var2 = (((((adc_T>>4) - self._calibration['dig_T1']) * ((adc_T>>4) - self._calibration['dig_T1'])) >> 12) * self._calibration['dig_T3']) >> 14

        self._t_fine = var1 + var2

        T = (self._t_fine * 5 + 128) >> 8
        return T / 100


    @property
    def pressure(self):
        """Returns the pressure (in Pascals) from the sensor"""
        self.temperature # must be done first to get _t_fine

        adc_P = bbspi.read24(self._cs, BME280_REGISTER_PRESSUREDATA)
        if adc_P == 0x800000: # value in case pressure measurement was disabled
            return None
        adc_P >>= 4

        var1 = self._t_fine - 128000
        var2 = var1 * var1 * self._calibration['dig_P6']
        var2 = var2 + ((var1 * self._calibration['dig_P5']) << 17)
        var2 = var2 + (self._calibration['dig_P4'] << 35)
        var1 = ((var1 * var1 * self._calibration['dig_P3']) >> 8) + ((var1 * self._calibration['dig_P2']) << 12)
        var1 = ((1 << 47) + var1) * self._calibration['dig_P1'] >> 33

        if var1 == 0:
            return 0 # avoid exception caused by division by zero

        p = 1048576 - adc_P
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self._calibration['dig_P9'] * (p >> 13) * (p >> 13)) >> 25
        var2 = (self._calibration['dig_P8'] * p) >> 19

        p = ((p + var1 + var2) >> 8) + (self._calibration['dig_P7'] << 4)
        return p / 256


    @property
    def humidity(self):
        """Returns the humidity from the sensor"""
        self.temperature # must be done first to get _t_fine

        adc_H = bbspi.read16(self._cs, BME280_REGISTER_HUMIDDATA)
        if adc_H == 0x8000: # value in case humidity measurement was disabled
            return None

        v_x1_u32r = (self._t_fine - 76800)

        v_x1_u32r = (((((adc_H << 14) - (self._calibration['dig_H4'] << 20) -
                        (self._calibration['dig_H5'] * v_x1_u32r)) + 16384) >> 15) *
                    (((((((v_x1_u32r * self._calibration['dig_H6']) >> 10) *
                        (((v_x1_u32r * self._calibration['dig_H3']) >> 11) + 32768)) >> 10) +
                        2097152) * self._calibration['dig_H2'] + 8192) >> 14))

        v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * self._calibration['dig_H1']) >> 4))

        if v_x1_u32r < 0:
            v_x1_u32r = 0
        if v_x1_u32r > 419430400:
            v_x1_u32r = 419430400

        h = v_x1_u32r >> 12
        return  h / 1024.0


    @property
    def altitude(self, seaLevel):
        """Calculates the altitude (in meters) from the specified atmospheric pressure (in hPa), and sea-level pressure (in hPa).
        seaLevel-- sea-level pressure in hPa
        """
        # Equation taken from BMP180 datasheet (page 16):
        #  http://www.adafruit.com/datasheets/BST-BMP180-DS000-09.pdf
        # Note that using the equation from wikipedia can give bad results
        # at high altitude. See this thread for more information:
        #  http://forums.adafruit.com/viewtopic.php?f=22&t=58064

        atmospheric = self.pressure / 100.0
        return 44330.0 * (1.0 - pow(atmospheric / seaLevel, 0.1903))

    def sea_level_for_altitude(self, altitude, atmospheric):
        """Calculates the pressure at sea level (in hPa) from the specified altitude
        (in meters), and atmospheric pressure (in hPa).
        altitude    --  altitude in meters
        atmospheric --  atmospheric pressure in hPa
        """
        # Equation taken from BMP180 datasheet (page 17):
        #  http://www.adafruit.com/datasheets/BST-BMP180-DS000-09.pdf
        # Note that using the equation from wikipedia can give bad results
        # at high altitude. See this thread for more information:
        #  http://forums.adafruit.com/viewtopic.php?f=22&t=58064

        return atmospheric / pow(1.0 - (altitude/44330.0), 5.255)
