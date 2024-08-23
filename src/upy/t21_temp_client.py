# https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/examples/temp_client.py
import sys

# ruff: noqa: E402
sys.path.append("")

from micropython import const

import asyncio
import aioble
import bluetooth

import random
import struct

# GR
import wifi
import urequests
# GR end

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)


# Helper to decode the temperature characteristic encoding (sint16, hundredths of a degree).
def _decode_temperature(data):
    return struct.unpack("<h", data)[0] / 100


async def find_temp_sensor():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # See if it matches our name and the environmental sensing service.
            if result.name() == "mpy-temp" and _ENV_SENSE_UUID in result.services():
                return result.device
    return None


async def main():
    # GR
    wifi.connect()

    device = None
    
    while not device:
        device = await find_temp_sensor()
        if not device:
            print("Temperature sensor not found")
            #return

    try:
        print("Connecting to", device)
        connection = await device.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return

    async with connection:
        try:
            temp_service = await connection.service(_ENV_SENSE_UUID)
            temp_characteristic = await temp_service.characteristic(_ENV_SENSE_TEMP_UUID)
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

        while connection.is_connected():
            temp_deg_c = _decode_temperature(await temp_characteristic.read())
            print("Temperature: {:.2f}".format(temp_deg_c))
            #GR
            url = "http://192.168.2.2:8000"
            data = {
                'text': str(temp_deg_c)+" your name <id>",
                'color': 'cyan' #'#FFFF00'
                }
            print('about to post to', url, 'with data', data)
            # Post the data to the server
            response = urequests.post(url, json=data)
            # Print the server's response
            print("response", response.text)
            #GR end

            await asyncio.sleep_ms(1000)


asyncio.run(main())
