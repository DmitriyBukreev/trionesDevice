import asyncio
from dataclasses import dataclass

from bleak import BleakClient, BLEDevice, BaseBleakClient, BleakGATTCharacteristic
from typing import Final, Callable


def validate_color(color: int):
    if color > 255:
        return 255
    if color < 0:
        return 0
    return color


def get_future() -> asyncio.Future:
    return asyncio.get_event_loop().create_future()


@dataclass
class TrionesDeviceStatus:
    power: bool
    red: int
    green: int
    blue: int

    @staticmethod
    def fromBytearray(data: bytearray):
        return TrionesDeviceStatus(
            power=(data[2:3] == POWER.ON),
            red=data[6],
            green=data[7],
            blue=data[8]
        )


class CHARACTERISTICS:
    WRITE: Final[str] = "0000ffd9-0000-1000-8000-00805f9b34fb"
    NOTIFY: Final[str] = "0000ffd4-0000-1000-8000-00805f9b34fb"


class POWER:
    ON: Final[bytes] = b'\x23'
    OFF: Final[bytes] = b'\x24'


class TrionesDevice:
    _status_awaitable: asyncio.Future
    _timeout: float

    def __init__(self, address_or_device: BLEDevice | str, timeout: float = None,
                 winrt=None, backend: BaseBleakClient = None,
                 disconnected_callback: Callable[[BleakClient], None] = None):
        if winrt is None:
            winrt = {}
        self._timeout = timeout
        self.client = BleakClient(address_or_device,
                                  timeout=timeout,
                                  winrt=winrt,
                                  backend=backend,
                                  disconnected_callback=disconnected_callback)

    async def connect(self) -> None:
        await self.client.connect()
        # Register callback to receive status updates
        await self.client.start_notify(CHARACTERISTICS.NOTIFY, self.statusCallback)

    async def disconnect(self) -> None:
        await self.client.disconnect()

    async def power(self, on=True) -> None:
        power_byte = POWER.ON if on else POWER.OFF
        payload = b'\xcc%(power)s\x33' % {b'power': power_byte}
        await self.client.write_gatt_char(CHARACTERISTICS.WRITE, payload)

    async def setRGB(self, r: int, g: int, b: int) -> None:
        red = validate_color(r)
        green = validate_color(g)
        blue = validate_color(b)
        payload = b'\x56%(red)c%(green)c%(blue)c\x00\xF0\xAA' % {b'red': red, b'green': green, b'blue': blue}
        await self.client.write_gatt_char(CHARACTERISTICS.WRITE, payload)

    async def getStatus(self) -> TrionesDeviceStatus:
        # Prepare future to await for
        self._status_awaitable = get_future()
        # Sending request for data
        await self.client.write_gatt_char(CHARACTERISTICS.WRITE, b'\xEF\x01\x77', True)
        # Returning result
        result = await asyncio.wait_for(self._status_awaitable, timeout=self._timeout)
        return TrionesDeviceStatus.fromBytearray(result)

    def statusCallback(self, sender: BleakGATTCharacteristic, data: bytearray):
        self._status_awaitable.set_result(data)

