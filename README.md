python-lgtv
===========

Simple class for pairing with and controlling your 2012+ LG TV with python.

You can find all TVs on the network using the `find_tvs` class method.

```
from lg import Remote

addresses = Remote.find_tvs()
```
If you have only one, it'll be faster to use the `first_only` parameter.

```
address = Remote.find_tvs(first_only=True)
```

You will need a pairing key, if you already know it you can pass it to the `Remote` class' `__init__` otherwise you can create your remote control instance and it'll ask the TV to display it onscreen. You can then provide this pairing key using the `set_pairing_key` method.

```
remote = Remote(address)
# Pairing key will appear on screen
key = raw_input('Please enter pairing key: ')
remote.set_pairing_key(key)
```

After this you can send single or multiple commands using `send_command` and `send_multiple`.

```
remote.send_command(Remote.VOLUME_UP)

commands = [Remote.HOME, Remote.EXIT, Remote.MENU]
remote.send_multiple(commands)
```

An optional `delay` parameter can be provided to `send_multiple`; this will the amount of seconds the control will wait between commands. N.B. Sending commands too fast can cause some of them to be ignored.

A reference of all the shortcut commands available are below, you are free to send any integer with `send_command` but be careful if you don't know what your are doing, as some commands can force the TV in service modes that can be tricky to get back out of.

```
    POWER = 1
    NUM_0 = 2
    NUM_1 = 3
    NUM_2 = 4
    NUM_3 = 5
    NUM_4 = 6
    NUM_5 = 7
    NUM_6 = 8
    NUM_7 = 9
    NUM_8 = 10
    NUM_9 = 11
    UP = 12
    DOWN = 13
    LEFT = 14
    RIGHT = 15
    OK = 20
    HOME = 21
    MENU = 22
    BACK = 23
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    MUTE = 26
    CHANNEL_UP = 27
    CHANNEL_DOWN = 28
    BLUE = 29
    GREEN = 30
    RED = 31
    YELLOW = 32
    PLAY = 33
    PAUSE = 34
    STOP = 35
    FF = 36
    REW = 37
    SKIP_FF = 38
    SKIP_REW = 39
    REC = 40
    REC_LIST = 41
    LIVE = 43
    EPG = 44
    INFO = 45
    ASPECT = 46
    EXT = 47
    PIP = 48
    SUBTITLE = 49
    PROGRAM_LIST = 50
    TEXT = 51
    MARK = 52
    _3D = 400
    _3D_LR = 401
    DASH = 402
    PREV = 403
    FAV = 404
    QUICK_MENU = 405
    TEXT_OPTION = 406
    AUDIO_DESC = 407
    NETCAST = 408
    ENERGY_SAVE = 409
    AV = 410
    SIMPLINK = 411
    EXIT = 412
    RESERVE = 413
    PIP_CHANNEL_UP = 414
    PIP_CHANNEL_DOWN = 415
    PIP_SWITCH = 416
    APPS = 417
```
