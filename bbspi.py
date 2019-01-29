import digitalio

class BBSpi(object):

    def __init__(self, clock=None, MOSI=None, MISO=None):
        if clock is None or MOSI is None or MISO is None:
            return None
        self._clock_pin = digitalio.DigitalInOut(clock)
        self._clock_pin.direction = digitalio.Direction.OUTPUT
        self._mosi_pin = digitalio.DigitalInOut(MOSI)
        self._mosi_pin.direction = digitalio.Direction.OUTPUT
        self._miso_pin = digitalio.DigitalInOut(MISO)
        self._miso_pin.direction = digitalio.Direction.INPUT
        self._miso_pin.pull = digitalio.Pull.UP
        self.configure()


    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        """Configures the SPI bus. The SPI object must be locked.

        :param int baudrate: the desired clock rate in Hertz. The actual clock rate may be higher or lower
                             due to the granularity of available clock settings.
                            Check the `frequency` attribute for the actual clock rate.
        :param int polarity: the base state of the clock line (0 or 1)
        :param int phase: the edge of the clock that data is captured. First (0)
                          or second (1). Rising or falling depends on clock polarity.
        :param int bits: the number of bits per word
        """
        self._baudrate = baudrate
        self._polarity = polarity
        self._phase = phase
        self._bits = bits


    def try_lock(self):
        """Attempts to grab the SPI lock. Returns True on success.

        :return: True when lock has been grabbed
        """
        pass


    def unlock(self):
        """Releases the SPI lock."""
        pass


    def _transfer_byte(tx_byte):
        rx_byte = 0
        bit = 0x80
        for _ in range(0,8):
            self._mosi_pin.value = (tx_byte & bit) != 0
            time.sleep(SPI_SCLK_LOW_TIME)
            self._clock_pin.value = True
            if self._miso_pin.value:
                rx_byte |= bit
            time.sleep(SPI_SCLK_HIGH_TIME)
            self._clock_pin.value = False
            bit >>= 1
        return rx_byte


    def _transfer(self, buffer_out, buffer_in, out_start=0, out_end=len(buffer_out), in_start=0, in_end=len(buffer_in):
        out_index = out_start
        in_index = in_start
        for _ = range(start, end):
            buffer_in[in_index] = self._transfer_byte(buffer_out[out_index])


    def write(self, buffer, start=0, end=len(buffer)):
        """Write the data contained in ``buffer``. The SPI object must be locked.
        If the buffer is empty, nothing happens.

        :param bytearray buffer: Write out the data in this buffer
        :param int start: Start of the slice of ``buffer`` to write out: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included
        """
        dummy_buffer = [0] * (end - start)
        self._transfer(buffer, dummy_buffer, start, end)


    def readinto(self, buffer, start=0, end=len(buffer), write_value=0):
        """Read into ``buffer`` while writing ``write_value`` for each byte read.
        The SPI object must be locked.
        If the number of bytes to read is 0, nothing happens.

        :param bytearray buffer: Read data into this buffer
        :param int start: Start of the slice of ``buffer`` to read into: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included
        :param int write_value: Value to write while reading. (Usually ignored.)
        """
        dummy_buffer = [write_value] * (end - start)
        self._transfer(dummy_buffer, buffer, start, end)


    def write_readinto(self, buffer_out, buffer_in, out_start=0, out_end=len(buffer_out), in_start=0, in_end=len(buffer_in)):
        """Write out the data in ``buffer_out`` while simultaneously reading data into ``buffer_in``.
        The SPI object must be locked.
        The lengths of the slices defined by ``buffer_out[out_start:out_end]`` and ``buffer_in[in_start:in_end]``
        must be equal.
        If buffer slice lengths are both 0, nothing happens.

        :param bytearray buffer_out: Write out the data in this buffer
        :param bytearray buffer_in: Read data into this buffer
        :param int out_start: Start of the slice of buffer_out to write out: ``buffer_out[out_start:out_end]``
        :param int out_end: End of the slice; this index is not included
        :param int in_start: Start of the slice of ``buffer_in`` to read into: ``buffer_in[in_start:in_end]``
        :param int in_end: End of the slice; this index is not included
        """
        self._transfer(buffer_out, buffer_in, out_start, out_end, in_start, in_end)


    @property
    def frequency(self):
        """The actual SPI bus frequency. This may not match the frequency requested
           due to internal limitations.
        """
        pass


class SPIDevice(object):

    def __init__(self, spi, cs, baudrate=100000, polarity=0, phase=0):
        """
        :param BBSpi spi: The bit banged spi bus object
        :param digitalio.DigitalInOut cs: The chip select pin for this device
        """
        self._spi = spi
        self._cs = cs
        spi.configure(baudrate=baudrate, polarity=polarity, phase=phase)


    def write(self, buffer, start=0, end=len(buffer)):
        """Write the data contained in ``buffer``. The SPI object must be locked.
        If the buffer is empty, nothing happens.

        :param bytearray buffer: Write out the data in this buffer
        :param int start: Start of the slice of ``buffer`` to write out: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included
        """
        # enable CS
        self._spi.write(buffer, start=start, end=end)
        #disable CS


    def readinto(self, buffer, start=0, end=len(buffer), write_value=0):
        """Read into ``buffer`` while writing ``write_value`` for each byte read.
        The SPI object must be locked.
        If the number of bytes to read is 0, nothing happens.

        :param bytearray buffer: Read data into this buffer
        :param int start: Start of the slice of ``buffer`` to read into: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included
        :param int write_value: Value to write while reading. (Usually ignored.)
        """
        # enable CS
        self._spi.writreadinto(buffer, start=start, end=end, write_value=write_value)
        #disable CS


    def write_readinto(self, buffer_out, buffer_in, out_start=0, out_end=len(buffer_out), in_start=0, in_end=len(buffer_in)):
        """Write out the data in ``buffer_out`` while simultaneously reading data into ``buffer_in``.
        The SPI object must be locked.
        The lengths of the slices defined by ``buffer_out[out_start:out_end]`` and ``buffer_in[in_start:in_end]``
        must be equal.
        If buffer slice lengths are both 0, nothing happens.

        :param bytearray buffer_out: Write out the data in this buffer
        :param bytearray buffer_in: Read data into this buffer
        :param int out_start: Start of the slice of buffer_out to write out: ``buffer_out[out_start:out_end]``
        :param int out_end: End of the slice; this index is not included
        :param int in_start: Start of the slice of ``buffer_in`` to read into: ``buffer_in[in_start:in_end]``
        :param int in_end: End of the slice; this index is not included
        """
        # enable CS
        self._spi.write_readinto(buffer_out, buffer_in, out_start=out_start, out_end=out_end, in_start=in_start, in_end=in_end)
        #disable CS
