from .base import *

SECRET_KEY = "xH8C6GEsGiYZXRb9NjKFfysi1jNhAUKpuBnj2nABsGjPhCChM2"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Email Backend

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Google ReCaptcha

RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"

# Twitter API

PUBLIC_API_KEY = "7V4vHQHWm9CK1T4hC1byZJJzp"

PRIVATE_KEY_KEY = "G2ahiH1i1bbocGc6QYqUNB4pwh1jBO0KKBP7uhXsAVaziYaW6G"

PUBLIC_ACCESS_TOKEN = "1065652779857965057-iJ9wtbWwmLjRlgW3G8fbGJsvjYfKSa"

PRIVATE_ACCESS_TOKEN = "qcpfz4QQmiM2DaKjd7DTTwJ1ponJz4J3OTy4XZJCJXSNb"

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
print("Server Started...")

while True:
    client_socket, ip_address = s.accept()
    print(f"connection from {ip_address} has been established")
    client_socket.send(bytes("Welcome to the server!", "utf-8"
    ))
