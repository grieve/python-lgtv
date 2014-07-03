from lg import Remote

if __name__ == "__main__":
    try:
        Remote()
    except Remote.NoPairingKey:
        key = raw_input('Enter pairing key: ')
        remote = Remote(key)

    remote.send_command(Remote.VOLUME_UP)
