from dumbdisplay import *


_dd: DumbDisplay = None
_enable_sound = False

_button_sound_file = "button.ogg"
_coin_sound_file = "coin.ogg"
_toilet_sound_file = "toilet.ogg"

_sound_files = [_button_sound_file, _coin_sound_file, _toilet_sound_file]

def get_sound_names() -> list[str]:
    return _sound_files

def setup_sounds(dd: DumbDisplay, enable_sound: bool):
    global _dd, _enable_sound
    _dd = dd
    _enable_sound = enable_sound

def play_button_sound():
    if _enable_sound:
        _dd.playSound(_button_sound_file)

def play_coin_sound():
    if _enable_sound:
        _dd.playSound(_coin_sound_file)

def play_toilet_sound():
    if _enable_sound:
        _dd.playSound(_toilet_sound_file)
