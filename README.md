# ES8311 MicroPython Audio Codec Driver (ESP32)

A lightweight **MicroPython driver for the ES8311 low-power audio codec**, focused on reliable **DAC audio playback** on ESP32-class microcontrollers using I2C, I2S, and a software-generated MCLK.

This project is intentionally minimal and stable, providing the core functionality required to play audio cleanly without pops, lockups, or clocking issues.

---

## Features

* ES8311 DAC playback initialization
* Safe power-on and power-off sequencing
* Software-generated **MCLK via PWM** (no external crystal required)
* I2C register-level control
* Volume control (0–100%)
* External speaker amplifier enable pin
* Designed for WAV playback and tone generation
* Compatible with common MicroPython I2S players

---

## Not Implemented (Yet)

This driver currently exposes **only a subset** of the ES8311 feature set.

The following are **not implemented**:

* Microphone input path
* ADC configuration
* Microphone / line-in gain control
* AGC / ALC
* Mixer routing
* DSP and noise suppression features

The code structure allows these features to be added later by extending the register interface.

---

## Target Platforms

* ESP32
* ESP32-S2
* ESP32-S3

**Language:** MicroPython
**Interfaces:** I2C, I2S, PWM (MCLK)

---

## Hardware Requirements

* ESP32-family microcontroller
* ES8311 audio codec module
* External speaker amplifier (if required by your board)
* Speaker or headphones

---

## Wiring

### ES8311 Connections

| ES8311 Pin | ESP32 Pin | Description        |
| ---------- | --------- | ------------------ |
| SDA        | GPIO 5    | I2C data           |
| SCL        | GPIO 4    | I2C clock          |
| MCLK       | GPIO 6    | Master clock (PWM) |
| BCLK       | GPIO 14   | I2S bit clock      |
| LRCK       | GPIO 12   | I2S word select    |
| DIN        | GPIO 11   | I2S data           |
| AMP_EN     | GPIO 9    | Speaker amp enable |

> Adjust GPIO numbers in the code if your board differs.

---

## Software Requirements

* MicroPython firmware with:

  * `machine.I2C`
  * `machine.PWM`
  * `machine.I2S`
* ESP32 firmware build with I2S enabled
* WAV files stored on the device filesystem

---

## Installation

1. Copy `es8311.py` to your device:

   ```
   /lib/es8311.py
   ```

2. (Optional) Copy your WAV player module:

   ```
   /lib/wavplayer.py
   ```

3. Reboot the device.

---
## ES8311 Initialization Example
```python
from es8311 import ES8311
# ==================================================
# ES8311 CODEC CONFIGURATION
# ==================================================
codec = ES8311(scl=4, sda=5, mck=6, rate=32000)
codec.power_on()
codec.set_volume(70)

```
## Basic Usage Example

```python
from es8311 import ES8311
# ==================================================
# ES8311 CODEC CONFIGURATION
# ==================================================
codec = ES8311(scl=4, sda=5, mck=6, rate=32000)
codec.power_on()
codec.set_volume(70)

    # ======= I2S CONFIGURATION =======
SCK_PIN = 14
WS_PIN = 12
SD_PIN = 11
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 40000

import time
from machine import Pin
from wavplayer import WavPlayer
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
```

---

## Volume Control

```python
codec.set_volume(50)   # 0–100%
```

Volume is mapped linearly to the ES8311 DAC volume register.

---

## Power Management

The driver ensures:

* Codec is powered down **before** clocks stop
* PWM MCLK is disabled safely
* I2C is released after shutdown

This prevents:

* Audible pops
* I2C lockups
* Codec reset failures on next boot

---

## Known Limitations

* Playback only (DAC path)
* Requires software-generated MCLK
* No automatic WAV format validation
* Sample rate must match codec configuration

---

## Troubleshooting

### No Sound

* Verify `AMP_EN` is high
* Confirm MCLK pin is connected
* Check WAV format (mono, 16-bit recommended)

### Distorted Audio

* Ensure WAV sample rate matches `rate`
* Reduce I2S buffer size if memory constrained
* Avoid blocking operations during playback

### Codec Locks Up After Playback

* Ensure `power_off()` is called
* Do not disable PWM before codec shutdown
