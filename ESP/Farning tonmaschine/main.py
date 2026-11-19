from machine import Pin, PWM
import asyncio
import time

from bohemian_rhapsody import SONG, BEAT   # made by midi2song.py

PINS = [33, 35, 37, 39]
BUTTON = 3                   # button module OUT: reads 0 while pressed; internal pullup
LEGATO = 0.9                 # fraction of each note that sounds
VOLUME = 1                   # 1.0 = loudest (50% duty)
TRANSPOSE = [0, 0, 0, 0]     # octaves to shift each voice, e.g. 1 to raise a bass line

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

active = []                  # live PWM object for each voice, or None
for pin in PINS:
    active.append(None)


def freq(name, octaves):
    """'C#5' -> Hz, shifted by a number of octaves."""
    pitch = name[:-1]                            # 'C#'
    octave = int(name[-1]) + octaves             # 5, plus any transpose
    step = NAMES.index(pitch)                    # 1: semitones above C
    midi_note = 12 * (octave + 1) + step         # 73 (MIDI 0 is C-1, so +1 octave)

    ref_note = 69                                # MIDI number of A4
    ref_hz = 440                                 # A4's frequency
    steps_from_ref = midi_note - ref_note        # 4
    hz = ref_hz * 2 ** (steps_from_ref / 12)     # each step is a factor of 2^(1/12)
    return round(hz)                             # 554


def silence(pin):
    Pin(pin, Pin.OUT, value=0)   # hold the pin low so the transistor stays off


def play_note(pin, hz):
    """Start a square wave on pin at hz. Returns the PWM; deinit() it to stop."""
    return PWM(Pin(pin), freq=hz, duty_u16=int(32768 * VOLUME))


def stop(i):
    """Stop voice i: release its PWM timer, then drive its pin low."""
    pwm = active[i]
    active[i] = None
    if pwm is not None:
        pwm.deinit()
    silence(PINS[i])


def stop_all():
    for i in range(len(PINS)):
        try:
            stop(i)
        except Exception:
            pass             # one bad pin shouldn't keep the others sounding


async def wait_until(start, beats):
    """Sleep until a position (in beats) measured from the shared start time."""
    target = time.ticks_add(start, int(beats * BEAT * 1000))
    delay = time.ticks_diff(target, time.ticks_ms())
    if delay > 0:
        await asyncio.sleep_ms(delay)


async def play_voice(i, text, pin, octaves, start):
    t = 0.0   # where this voice is in the piece, in beats
    await wait_until(start, 0)   # don't sound anything before the shared start time
    for token in text.split():
        name, beats = token.split(':')
        length = float(beats)
        if name != 'R':
            active[i] = play_note(pin, freq(name, octaves))
            stop_beat = t + length * LEGATO   # when this note goes silent
            await wait_until(start, stop_beat)
            stop(i)          # rebuild the timer for each note
        t += length
        await wait_until(start, t)


async def main():
    for pin in PINS:
        silence(pin)
    button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)
    print("starting")
    while True:
        while button.value():               # wait for a press
            await asyncio.sleep_ms(20)

        start = time.ticks_add(time.ticks_ms(), 100)   # every voice counts from here
        voices = []
        for i in range(len(PINS)):
            voices.append(play_voice(i, SONG[i], PINS[i], TRANSPOSE[i], start))
        await asyncio.gather(*voices)


try:
    asyncio.run(main())
finally:
    stop_all()               # runs on Ctrl-C / Thonny Stop and on any exception

