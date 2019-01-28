#include <Python.h>
#include <pigpio.h>

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
  uint8_t cs_pin, reg, value;
  static char *keywords[] = {"cs", "reg", "value", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bbb", keywords, &cs_pin, &reg, &value)) {
    return NULL;
  }
  char command[] = {reg & ~0x80, value};
  unsigned char input_buffer[2];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 2);
  if (count != 2) {
    return NULL;
  }
  Py_RETURN_NONE;
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }
  char command[] = {reg | 0x80, 0};
  unsigned char input_buffer[2];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 2);
  if (count != 2) {
    return NULL;
  }
  return PyLong_FromUnsignedLong((unsigned long)input_buffer[1]);
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }
  char command[] = {reg | 0x80, 0, 0};
  unsigned char input_buffer[3];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 3);
  if (count != 3) {
    return NULL;
  }
  return PyLong_FromUnsignedLong((unsigned long)((input_buffer[1] << 8) | input_buffer[2]));
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }
  char command[] = {reg | 0x80, 0, 0};
  unsigned char input_buffer[3];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 3);
  if (count != 3) {
    return NULL;
  }
  return PyLong_FromUnsignedLong((unsigned long)((input_buffer[2] << 8) | input_buffer[1]));
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }

  char command[] = {reg | 0x80, 0, 0};
  unsigned char input_buffer[3];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 3);
  if (count != 3) {
    return NULL;
  }
  return PyLong_FromLong((long)((input_buffer[1] << 8) | input_buffer[2]));
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }

  char command[] = {reg | 0x80, 0, 0};
  unsigned char input_buffer[3];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 3);
  if (count != 3) {
    return NULL;
  }
  return PyLong_FromLong((long)((input_buffer[2] << 8) | input_buffer[1]));
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
  uint8_t cs_pin, reg;
  static char *keywords[] = {"cs", "reg", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keyword_dict, "bb", keywords, &cs_pin, &reg)) {
    return NULL;
  }

  char command[] = {reg | 0x80, 0, 0, 0};
  unsigned char input_buffer[4];
  int count = bbSPIXfer(cs_pin, command, (char *)input_buffer, 4);
  if (count != 4) {
    return NULL;
  }
  uint32_t value = input_buffer[1];
  value <<= 8;
  value |= input_buffer[2];
  value <<= 8;
  value |= input_buffer[3];
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
  Py_RETURN_NONE;
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
  Py_RETURN_NONE;
}


static PyMethodDef bbspi_methods[] = {
  {"write8", (PyCFunction)bbspi_write8, METH_VARARGS | METH_KEYWORDS, "Write an unsigned 8-bit value."},
  {"read8", (PyCFunction)bbspi_read8, METH_VARARGS | METH_KEYWORDS, "Read an unsigned 8-bit value."},
  {"read16", (PyCFunction)bbspi_read16, METH_VARARGS | METH_KEYWORDS, "Read an unsigned 16-bit value."},
  {"read16_LE", (PyCFunction)bbspi_read16_LE, METH_VARARGS | METH_KEYWORDS, "Read an unsigned 16-bit value, little endian."},
  {"readS16", (PyCFunction)bbspi_readS16, METH_VARARGS | METH_KEYWORDS, "Read a signed 16-bit value."},
  {"readS16_LE", (PyCFunction)bbspi_readS16_LE, METH_VARARGS | METH_KEYWORDS, "Read a signed 16-bit value, little endian."},
  {"read24", (PyCFunction)bbspi_read24, METH_VARARGS | METH_KEYWORDS, "Read an unsigned 24-bit value."},
  {"open", (PyCFunction)bbspi_open, METH_VARARGS | METH_KEYWORDS, "Open a bitbanged SPI interface."},
  {"close", (PyCFunction)bbspi_close, METH_VARARGS | METH_KEYWORDS, "Close a bitbanged SPI interface."},
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef bbspi_module = {
  PyModuleDef_HEAD_INIT,
  "bbspi",
  NULL,
  -1,
  bbspi_methods
};


PyMODINIT_FUNC
PyInit_bbspi(void)
{
  PyObject *m;

  m = PyModule_Create(&bbspi_module);
  if (m == NULL) {
    return NULL;
  }

  if (gpioInitialise() < 0) {
    return NULL;
  }

  return m;
}
