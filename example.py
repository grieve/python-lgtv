from lg import Remote

if __name__ == "__main__":
    address = Remote.find_tvs(first_only=True)
    remote = Remote(address)

    key = raw_input('Enter pairing key: ')
    remote.set_pairing_key(key)

    remote.send_command(Remote.VOLUME_UP)
