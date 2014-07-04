from __future__ import unicode_literals

import re
import time
import socket
import httplib

from xml.etree import ElementTree


class Remote():
    """
    Class for initialising communication with, and sending remote
    commands to a 2012+ LG TV.
    """

    def __init__(self, ip_address, pair_key=None):
        """
        Initialise class with IP and optional pair key. If not pair key
        provided, then the pair request will be sent to the TV and
        `.set_pairing_key()` must be called before use.
        """

        self.pair_key = pair_key
        self.ip_address = ip_address

        if not self.ip_address:
            raise Remote.NoTVFound

        if self.pair_key:
            self.get_session()
        else:
            self.request_pair()

    @classmethod
    def find_tvs(cls, attempts=10, first_only=False):
        """
        Create a broadcast socket and listen for LG TVs responding.
        Returns list of IPs unless `first_only` is true, in which case it
        will return the first TV found.
        """

        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST: 239.255.255.250:1900\r\n' \
                  'MAN: "ssdp:discover"\r\n' \
                  'MX: 2\r\n' \
                  'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        addresses = []
        while attempts > 0:
            sock.sendto(request, ('239.255.255.250', 1900))
            try:
                response, address = sock.recvfrom(512)
            except:
                attempts -= 1
                continue

            if re.search('LG', response):
                if first_only:
                    sock.close()
                    return address[0]
                else:
                    addresses.append(address[0])

            attempts -= 1

        sock.close()
        if first_only:
            raise Remote.NoTVFound
        else:
            if len(addresses) == 0:
                raise Remote.NoTVFound
            else:
                return addresses

    def set_pairing_key(self, pair_key):
        """
        Set the pairing key and initialise the session with the TV
        """

        self.pair_key = pair_key
        self.get_session()

    def make_request(self, endpoint, content, extra_headers={}):
        """
        POST the XML request to the configured TV and parse the response
        """

        http = httplib.HTTPConnection(self.ip_address, port=8080)
        headers = {'Content-Type': 'application/atom+xml'}
        headers.update(extra_headers)
        http.request("POST", endpoint, content, headers=headers)
        response = http.getresponse()
        tree = ElementTree.XML(response.read())
        return tree

    def request_pair(self):
        """
        Request for the TV to display the pairing key on-screen
        """

        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <auth>
            <type>AuthKeyReq</type>
        </auth>
        """
        self.make_request('/roap/api/auth', content)

    def get_session(self):
        """
        Request to pair with the TV and return the session ID
        """

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
        """
        Send a remote control key command. Ignores response for now.
        """

        if self.pair_key is None:
            raise Remote.NoPairingKey
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <command>
            <name>HandleKeyInput</name>
            <value>{0}</value>
        </command>
        """.format(code)
        self.make_request('/roap/api/command', content)

    def send_multiple(self, codes, delay=0.2):
        """
        Send multiple remote control commands with a delay in between. The
        delay is required as multiple commands can be ignored if too close
        together.
        """

        for code in codes:
            self.send_command(code)
            time.sleep(delay)

    # exceptions

    class NoPairingKey(Exception):
        """
        Exception raised when no pairing key is present and action requring one
        is attempted.
        """

        pass

    class NoTVFound(Exception):
        """
        Exception raised when unable to find any LG TVs on the network
        """

        pass

    # command code shortcuts

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
