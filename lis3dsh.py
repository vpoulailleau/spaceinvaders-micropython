"""LIS3DSH driver."""
from spi_register import SPIRegister


class LIS3DSH:
    WHO_AM_I = SPIRegister(address=0x0F)
    CTRL_REG4 = SPIRegister(address=0x20, write=True)
    OUT_X_L = SPIRegister(address=0x28)
    OUT_X_H = SPIRegister(address=0x29)
    OUT_Y_L = SPIRegister(address=0x2A)
    OUT_Y_H = SPIRegister(address=0x2B)
    OUT_Z_L = SPIRegister(address=0x2C)
    OUT_Z_H = SPIRegister(address=0x2D)

    SENSITIVITY_2G_RANGE = 0.06  # mg/digit

    def __init__(self, spi, chip_select):
        self.spi = spi  # pyb.SPI
        self.chip_select = chip_select  # pyb.Pin
        self.chip_select.high()
        # X, Y, Z enabled, 400Hz output datarate
        self.CTRL_REG4 = 0x77

    def _convert_value(self, high, low):
        value = (high << 8) | low
        if value & (1 << 15):
            # negative number
            value = value - (1 << 16)
        return value * self.SENSITIVITY_2G_RANGE

    @property
    def x(self):
        return self._convert_value(self.OUT_X_H, self.OUT_X_L)

    @property
    def y(self):
        return self._convert_value(self.OUT_Y_H, self.OUT_Y_L)

    @property
    def z(self):
        return self._convert_value(self.OUT_Z_H, self.OUT_Z_L)
