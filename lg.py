from __future__ import unicode_literals

import re
import socket
import httplib

from xml.etree import ElementTree


class Remote():

    def __init__(self, pair_key=None):
        self.pair_key = pair_key
        self.ip_address = self.find_tv()
        if not self.ip_address:
            raise Remote.NoTVFound

        if self.pair_key:
            self.get_session()
        else:
            self.request_pair()
            raise Remote.NoPairingKey

    def find_tv(self, retries=10):
        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST: 239.255.255.250:1900\r\n' \
                  'MAN: "ssdp:discover"\r\n' \
                  'MX: 2\r\n' \
                  'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)

        while retries > 0:
            sock.sendto(request, ('239.255.255.250', 1900))
            try:
                response, address = sock.recvfrom(512)
            except:
                retries -= 1
                continue

            if re.search('LG', response):
                sock.close()
                return address[0]

            retries -= 1

        sock.close()
        return None

    def make_request(self, endpoint, content, extra_headers={}):
        http = httplib.HTTPConnection(self.ip_address, port=8080)
        headers = {'Content-Type': 'application/atom+xml'}
        headers.update(extra_headers)
        http.request("POST", endpoint, content, headers=headers)
        response = http.getresponse()
        tree = ElementTree.XML(response.read())
        return tree

    def request_pair(self):
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <auth>
            <type>AuthKeyReq</type>
        </auth>
        """
        self.make_request('/roap/api/auth', content)

    def get_session(self):
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <auth>
            <type>AuthReq</type>
            <value>{0}</value>
        </auth>
        """.format(self.pair_key)
        response = self.make_request('/roap/api/auth', content)
        return response.find('session').text

    def send_command(self, code):
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <command>
            <name>HandleKeyInput</name>
            <value>{0}</value>
        </command>
        """.format(code)
        self.make_request('/roap/api/command', content)

    # exceptions

    class NoPairingKey(Exception):
        pass

    class NoTVFound(Exception):
        pass

    # command codes

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
