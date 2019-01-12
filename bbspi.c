#include <Python.h>
#include <pigpio.h>

const unsigned SPI_CS = 26;
const unsigned SPI_MISO = 20;
const unsigned SPI_MOSI = 21;
const unsigned SPI_SCLK = 16;
const unsigned SPI_BAUD = 115200;
const unsigned SPI_MODE = 0; // or 1, 2, 3

/**************************************************************************/
/*!
    @brief  Writes an 8 bit value over I2C or SPI
    @param reg the register address to write to
    @param value the value to write to the register
*/
/**************************************************************************/
static PyObject *
bbspi_write8(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg, byte value
{
  uint8_t cs, reg, value;
  static char *keywords = {"cs", "reg", "value", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bbb", keywords, &cs, &reg, &value)) {
    return NULL;
  }
  char cmd[] = {reg & ~0x80, value};
  unsigned char inBuf[2]
  int count = bbSPIXfer(cs, cmd, (char *)inBuffer, 2);
  Py_RETURN_NONE
}


/**************************************************************************/
/*!
    @brief  Reads an 8 bit value over I2C or SPI
    @param reg the register address to read from
    @returns the data byte read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_read8(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }
  char cmd[] = {reg | 0x80, 0};
  unsigned char inBuf[2]
  int count = bbSPIXfer(cs, cmd, (char *)inBuffer, 2);
  return PyLong_FromUnsignedLong((unsigned long)inBuf[1]);
}


/**************************************************************************/
/*!
    @brief  Reads a 16 bit value over SPI
    @param reg the register address to read from
    @returns the 16 bit data value read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_read16(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }
  char cmd[] = {reg | 0x80, 0, 0};
  unsigned char inBuf[3]
  int count = bbSPIXfer(cs, cmd, (char *)inBuffer, 3);
  return PyLong_FromUnsignedLong((unsigned long)((inBuf[1] << 8) | inBuf[2]));
}


/**************************************************************************/
/*!
    @brief  Reads an unsigned 16 bit little endian value over SPI
    @param reg the register address to read from
    @returns the 16 bit data value read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_read16_LE(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }
  char cmd[] = {reg | 0x80, 0, 0};
  unsigned char inBuf[3]
  int count = bbSPIXfer(SPI_CS, cmd, (char *)inBuffer, 3);
  return PyLong_FromUnsignedLong((unsigned long)((inBuf[2] << 8) | inBuf[1]));
}


/**************************************************************************/
/*!
    @brief  Reads a signed 16 bit value over SPI
    @param reg the register address to read from
    @returns the 16 bit data value read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_readS16(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }

  char cmd[] = {reg | 0x80, 0, 0};
  unsigned char inBuf[3]
  int count = bbSPIXfer(SPI_CS, cmd, (char *)inBuffer, 3);
  return PyLong_FromLong((long)((inBuf[1] << 8) | inBuf[2]));
}


/**************************************************************************/
/*!
    @brief  Reads a signed little endian 16 bit value over SPI
    @param reg the register address to read from
    @returns the 16 bit data value read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_readS16_LE(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }

  char cmd[] = {reg | 0x80, 0, 0};
  unsigned char inBuf[3]
  int count = bbSPIXfer(SPI_CS, cmd, (char *)inBuffer, 3);
  return PyLong_FromLong((long)((inBuf[2] << 8) | inBuf[1]));
}



/**************************************************************************/
/*!
    @brief  Reads a 24 bit value over SPI
    @param reg the register address to read from
    @returns the 24 bit data value read from the device
*/
/**************************************************************************/
static PyObject *
bbspi_read24(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte reg
{
  uint8_t cs, reg;
  static char *keywords = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs, &reg)) {
    return NULL;
  }

  char cmd[] = {reg | 0x80, 0, 0, 0};
  unsigned char inBuf[4]
  int count = bbSPIXfer(SPI_CS, cmd, (char *)inBuffer, 4);
  uint32_t value = inBuf[1];
  value <<= 8;
  value |= inBuf[2];
  value <<= 8;
  value |= inBuf[3];
  return PyLong_FromUnsignedLong((unsigned long)value);
}



static PyObject *
bbspi_open(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte cs_pin, byte miso_pin, byte mosi_pin, byte sclk_pin, int baud,  int flags
{
  uint8_t cs_pin, miso_pin, mosi_pin, sclk_pin;
  unsigned baud, flags;
  static char *keywords[] = {"cs", "miso", "mosi", "sclk", "baud", "flags", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bbbbII", keywords, &cs_pin, &miso_pin, &mosi_pin, &sclk_pin, &baud, &flags)) {
    return NULL;
  }

  int error = bbSPIOpen(cs_pin, miso_pin, mosi_pin, sclk_pin, baud, flags);
  if (error) {
    switch (error) {
    case PI_BAD_USER_GPIO:
      PyErr_SetString(PyExc_ValueError, "Bad user GPIO\n");
      break;
    case PI_BAD_SPI_BAUD:
      PyErr_SetString(PyExc_ValueError, "Bad SPI baud\n");
      break;
    case PI_GPIO_IN_USE:
      PyErr_SetString(PyExc_ValueError, "GPIO in use\n");
      break;
    }
    return NULL;
  }
}


static PyObject *
bbspi_close(PyObject *self, PyObject *args, PyObject *keyword_dict)  //byte cs_pin
{
  uint8_t cs_pin;
  static char *keywords[] = {"cs", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "b", keywords, &cs_pin)) {
    return NULL;
  }

  int error = bbSPIClose(cs_pin);
  if (error) {
    switch (error) {
    case PI_BAD_USER_GPIO:
      PyErr_SetString(PyExc_ValueError, "Bad user GPIO\n");
      break;
    case PI_NOT_SPI_GPIO:
      PyErr_SetString(PyExc_ValueError, "Bad SPI GPIO\n");
      break;
    }
    return NULL;
  }
}


static PyMethodDef bbspiMethods[] = {
  "write8", bbspi_write8, METH_VARARGS | METH_KEYWORDS,
  "read8", bbspi_read8, METH_VARARGS | METH_KEYWORDS,
  "read16", bbspi_read16, METH_VARARGS | METH_KEYWORDS,
  "read16_LE", bbspi_read16_LE, METH_VARARGS | METH_KEYWORDS,
  "readS16", bbspi_readS16, METH_VARARGS | METH_KEYWORDS,
  "readS16_LE", bbspi_readS16_LE, METH_VARARGS | METH_KEYWORDS,
  "read24", bbspi_read24, METH_VARARGS | METH_KEYWORDS,
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef bbspimodule = {
  PyModuleDef_HEAD_INT,
  "bbspi",
  NULL,
  -1
  bbspiMethods
};


PyMODINIT_FUNC
PyInit_bbspi(void)
{
  PyObject *m;

  m = PyModule_Create(&bbspimodule);
  if (m == NULL) {
    return NULL;
  }

  if (gpioInitialise() < 0) {
    return NULL;
  }

  return m;
}
