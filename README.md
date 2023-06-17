# trionesDevice

The module inspired by [trionesControl](https://github.com/Aritzherrero4/python-trionesControl) module from [Aritz Herrero](https://github.com/Aritzherrero4). 
It provides API to control LED devices using [triones protocol](https://github.com/madhead/saberlight/blob/master/protocols/Triones/protocol.md).
The motivation to build this module was to make it cross-platform using BLEAK module instead of pygatt.

## Requirments
Using BLEAK client this module is supposed to support every platform that BLEAK supports:
+ Windows 10, version 16299 (Fall Creators Update) or greater
+ Linux distributions with BlueZ >= 5.43
+ OS X/macOS support via Core Bluetooth API, from at least OS X version 10.11

## Installation
Install `trionesControl` with pip from PyPI:
```
pip install trionesControl
```
Or clone this repository and use `build` module to generate wheel:
```
python -m build
```
Then install it using pip:
```shell
pip install dist/%GENERATED_WHEEL_FILE%
```

## Usage

Initialize in a similar way to BleakClient using TrionesDevice class:
```
TrionesDevice(address_or_device: BLEDevice | str, timeout: float = 10,
                 winrt=None, backend: BaseBleakClient = None,
                 disconnected_callback: Callable[[BleakClient], None] = None)
```

Example:

```python
from trionesDevice import TrionesDevice

# Initializing using MAC address
device = TrionesDevice('00:00:00:00:00:00')
```

### Connection
+ `connect()` make connection to device specified during initialization.
+ `disconnect()` disconnect from previously connected device.

### Contol
+ `power(on: bool=True)` turn the device on or off depending on boolean used as a parameter.
+ `setRGB(r: int, g: int, b: int)` set color.
+ `getStatus() -> TrionesDeviceStatus` returns instance of TrionesDeviceStatus which contains such fields as:
  + `power: bool`
  + `red: int`
  + `green: int`
  + `blue: int`

## Licence
MIT Licence - Copyright 2023 Bukreev Dmitriy

For more information, check [LICENCE](https://github.com/DmitriyBukreev/trionesDevice/blob/main/LICENSE) file.