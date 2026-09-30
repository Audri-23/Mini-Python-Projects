import subprocess
import sys

# Installing required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode", "pillow"])

import qrcode

ssid = input("Enter WiFi Name: ")
password = input("Enter WiFi Password: ")

qr_string = f"WIFI:T:WPA;S:{ssid};P:{password};;"

image = qrcode.make(qr_string)
image.save("wifi_qr.png")

print("WiFi QR code generated successfully and saved as wifi_qr.png")