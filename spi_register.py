"""Descriptor for a register."""


class SPIRegister:
    """Descriptor for a register."""

    def __init__(self, address=0, read=True, write=False, size=1):
        """Initializer."""
        self.address = address
        self.read = read
        self.write = write
        self.size = size

    def __get__(self, instance, owner):
        """Getter."""
        if instance:
            instance.chip_select.low()
            instance.spi.send(self.address | 0x80)
            # TODO self.size != 1
            value = instance.spi.recv(1)
            instance.chip_select.high()
            return value[0]
        else:
            return self

    def __set__(self, instance, value):
        """Setter."""
        if self.write:
            instance.chip_select.low()
            instance.spi.send(self.address & 0x7F)
            instance.spi.send(value)
            instance.chip_select.high()

    def __delete__(self, instance):
        """Deleter. Does nothing."""
        pass
