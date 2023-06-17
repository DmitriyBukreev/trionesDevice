import os

from trionesDevice import TrionesDevice
import logging
import unittest
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADDRESS = os.environ.get('ADDRESS')


async def reconnect(device):
    try:
        logger.info('Connecting...')
        await device.connect()
        logger.info('Connected!')
    except Exception as e:
        logger.error(f'Failed to connect: {e}')
        await asyncio.sleep(5)
        await reconnect(device)


class TestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.device = TrionesDevice(ADDRESS, timeout=10)
        await reconnect(self.device)

    async def asyncTearDown(self) -> None:
        await self.device.disconnect()

    async def test_powerOn(self):
        await self.device.power(True)
        status = await self.device.getStatus()
        self.assertTrue(status.power)

    async def test_powerOff(self):
        await self.device.power(False)
        status = await self.device.getStatus()
        self.assertFalse(status.power)

    async def assertRGB(self, r, g, b):
        await self.device.setRGB(r, g, b)
        status = await self.device.getStatus()
        self.assertEqual(status.red, r)
        self.assertEqual(status.green, g)
        self.assertEqual(status.blue, b)

    async def test_setRGB(self):
        await self.assertRGB(255, 0, 0)
        await self.assertRGB(0, 100, 0)
        await self.assertRGB(50, 50, 50)


if __name__ == '__main__':
    unittest.main()
