import os
import time
from machine import Pin
from wavplayer import WavPlayer
from es8311 import ES8311
    # ======= ES8311 CONFIGURATION =======
codec = ES8311(scl=4, sda=5, mck=6, rate=32000)
codec.power_on()
codec.set_volume(70)

    # ======= I2S CONFIGURATION =======
SCK_PIN = 14
WS_PIN = 12
SD_PIN = 11
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 40000
    # ======= I2S CONFIGURATION =======

wp = WavPlayer(
    id=I2S_ID,
    sck_pin=Pin(SCK_PIN),
    ws_pin=Pin(WS_PIN),
    sd_pin=Pin(SD_PIN),
    ibuf=BUFFER_LENGTH_IN_BYTES,
)


wp.play("music-16k-16bits-mono.wav", loop=False)
time.sleep(10)  # play for 10 seconds
 # continue playing to the end of the WAV file
codec.power_off()
from machine import SPI, Pin, PWM, ADC, RTC, deepsleep
deepsleep()
